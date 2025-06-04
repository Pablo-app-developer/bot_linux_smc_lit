"""
mt5_trader.py - Ejecutor de operaciones en MetaTrader 5 basado en SMC-LIT

Este módulo implementa el bucle principal de trading que:
- Procesa las señales generadas por el modelo SMC-LIT
- Calcula tamaños de posición adecuados según gestión de riesgo
- Ejecuta órdenes en MetaTrader 5
- Gestiona posiciones abiertas (trailing stop, break-even)
- Mantiene registro de operaciones y resultados
"""

import os
import time
import logging
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import threading
from dotenv import load_dotenv

from .mt5_connector import MT5Connector
from src.features import SMCFeatureExtractor
from src.strategy import SMCStrategy
from src.agent import SMCAgent

# Configurar logging
logger = logging.getLogger('mt5_trader')

# Cargar variables de entorno
load_dotenv()

class MT5Trader:
    """
    Trader automático que utiliza el modelo SMC-LIT para operar en MT5.
    """
    
    def __init__(self, 
                 model=None,
                 symbol="EURUSD",
                 timeframe="M5",
                 risk_percent=1.0,
                 max_trades=5,
                 update_interval=60,
                 use_ai=True,
                 use_trailing=True):
        """
        Inicializa el trader.
        
        Args:
            model: Modelo IA pre-entrenado (opcional)
            symbol: Símbolo a operar
            timeframe: Timeframe para análisis
            risk_percent: Porcentaje de riesgo por operación
            max_trades: Número máximo de operaciones simultáneas
            update_interval: Intervalo de actualización en segundos
            use_ai: Usar modelo IA para filtrar señales
            use_trailing: Usar trailing stop para gestión de operaciones
        """
        self.symbol = symbol
        self.timeframe = timeframe
        self.risk_percent = float(os.getenv('RISK_PERCENT', risk_percent))
        self.max_trades = max_trades
        self.update_interval = update_interval
        self.use_ai = use_ai
        self.use_trailing = use_trailing
        
        # Inicializar conector MT5
        self.connector = MT5Connector(symbol=symbol, timeframe=timeframe)
        
        # Configuración para análisis
        self.candles_count = 1000  # Velas para análisis
        
        # Modelo IA pre-entrenado
        self.model = model
        
        # Control de ejecución
        self.running = False
        self.trade_thread = None
        
        # Registro de operaciones
        self.trades_history = []
        self.signals_history = []
        
        # Diccionario para tracking de posiciones con trailing
        self.tracked_positions = {}  # ticket -> info
    
    def initialize(self):
        """
        Inicializa el trader y verifica la conexión con MT5.
        
        Returns:
            bool: True si inicializado correctamente
        """
        logger.info(f"Inicializando trader para {self.symbol} en {self.timeframe}")
        
        if not self.connector._connected:
            if not self.connector.connect():
                logger.error("No se pudo conectar a MT5")
                return False
        
        # Verificar símbolo
        symbol_info = self.connector.get_symbol_info(self.symbol)
        if not symbol_info:
            logger.error(f"El símbolo {self.symbol} no está disponible")
            return False
        
        logger.info(f"Trader inicializado para {self.symbol}")
        return True
    
    def get_latest_data(self):
        """
        Obtiene los datos más recientes y aplica análisis SMC-LIT.
        
        Returns:
            tuple: (df_raw, df_features, signals)
        """
        try:
            logger.debug("Iniciando get_latest_data...")
            
            # Obtener datos OHLC
            logger.debug("Obteniendo datos OHLC...")
            df = self.connector.fetch_ohlc_data(
                symbol=self.symbol,
                timeframe=self.timeframe,
                num_candles=self.candles_count
            )
            
            if df is None or len(df) < 100:
                logger.error("No se pudieron obtener suficientes datos para análisis")
                return None, None, None
            
            logger.debug(f"Datos OHLC obtenidos: {len(df)} filas")
            logger.debug(f"Columnas en df: {list(df.columns)}")
            
            # Extraer features SMC-LIT
            logger.debug("Extrayendo features SMC-LIT...")
            features_extractor = SMCFeatureExtractor(df)
            df_features = features_extractor.extract_all()
            
            logger.debug(f"Features SMC extraídas: {list(df_features.columns)}")
            
            # Generar señales basadas en estrategia
            logger.debug("Generando señales de estrategia...")
            strategy = SMCStrategy(df_features)
            df_signals = strategy.run()
            
            logger.debug(f"Señales generadas: {list(df_signals.columns)}")
            
            # Aplicar filtro de IA si está habilitado
            if self.use_ai and self.model:
                logger.debug("Aplicando filtro de IA...")
                agent = SMCAgent(self.model, df_features)
                ai_df = agent.act()
                df_signals['ai_signal'] = ai_df['ai_signal']
                
                # Combinación: usar señal SMC solo si IA la confirma
                df_signals['final_signal'] = df_signals['signal'] * (df_signals['ai_signal'] > 0).astype(int)
            else:
                logger.debug("Sin filtro de IA, usando señales SMC directas")
                df_signals['final_signal'] = df_signals['signal']
            
            logger.debug("get_latest_data completado exitosamente")
            return df, df_features, df_signals
            
        except Exception as e:
            logger.error(f"Error en get_latest_data: {str(e)}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            return None, None, None
    
    def process_signals(self, df_signals):
        """
        Procesa las señales y ejecuta operaciones si es necesario.
        
        Args:
            df_signals: DataFrame con señales
        """
        if df_signals is None or len(df_signals) == 0:
            return
        
        # Obtener última vela con señal
        latest_candle = df_signals.iloc[-1]
        latest_signal = latest_candle['final_signal']
        
        # DEBUG: Imprimir tipo y valor de latest_candle
        logger.debug(f"latest_candle type: {type(latest_candle)}")
        logger.debug(f"latest_candle columns: {list(latest_candle.index) if hasattr(latest_candle, 'index') else 'No index'}")
        
        # Registrar señal
        self.signals_history.append({
            'timestamp': datetime.now(),
            'symbol': self.symbol,
            'signal': latest_signal,
            'price': latest_candle['close']
        })
        
        # Notificar señal detectada usando el sistema de notificaciones
        try:
            from .notifications import notifier
            if latest_signal != 0:
                signal_type = "BUY" if latest_signal > 0 else "SELL"
                confidence = abs(latest_candle.get('signal_strength', 0.5))
                price = float(latest_candle['close'])
                
                # Determinar razón de la señal
                reasons = []
                if latest_candle.get('choch', False):
                    reasons.append("CHoCH detectado")
                if latest_candle.get('order_block', False):
                    reasons.append("Order Block")
                if latest_candle.get('liquidity_trap', False):
                    reasons.append("Trampa de liquidez")
                
                reason = " + ".join(reasons) if reasons else "Análisis SMC"
                
                notifier.trade_signal(self.symbol, signal_type, confidence, price, reason)
        except ImportError:
            pass  # Continuar sin notificaciones si no está disponible
        
        # Si no hay señal, salir
        if latest_signal == 0:
            return
        
        # Verificar límite de operaciones simultáneas
        open_positions = self.connector.get_open_positions(self.symbol)
        if len(open_positions) >= self.max_trades:
            logger.info(f"Límite de operaciones alcanzado ({self.max_trades})")
            return
        
        # Calcular stop loss en puntos
        try:
            # DEBUG: Imprimir cada valor antes de la conversión
            logger.debug(f"latest_candle['close']: {latest_candle['close']} (type: {type(latest_candle['close'])})")
            logger.debug(f"latest_candle['low']: {latest_candle['low']} (type: {type(latest_candle['low'])})")
            logger.debug(f"latest_candle['high']: {latest_candle['high']} (type: {type(latest_candle['high'])})")
            logger.debug(f"latest_candle['atr_14']: {latest_candle['atr_14']} (type: {type(latest_candle['atr_14'])})")
            
            close_price = float(latest_candle['close'])
            low_price = float(latest_candle['low']) 
            high_price = float(latest_candle['high'])
            atr_value = float(latest_candle['atr_14'])
            
            logger.debug(f"Converted values - close: {close_price}, low: {low_price}, high: {high_price}, atr: {atr_value}")
            
        except (TypeError, ValueError, KeyError) as e:
            logger.error(f"Error obteniendo precios para SL/TP: {e}")
            logger.error(f"Detalles del error en latest_candle: {latest_candle}")
            return
            
        if latest_signal > 0:  # Compra
            sl_price = low_price - atr_value * 1.5
            try:
                sl_points = max(int(abs(close_price - sl_price) * 100000), 50)  # Convertir a puntos
                logger.debug(f"BUY sl_points calculation: abs({close_price} - {sl_price}) * 100000 = {sl_points}")
            except Exception as e:
                logger.error(f"Error calculando sl_points para BUY: {e}")
                return
        else:  # Venta
            sl_price = high_price + atr_value * 1.5
            try:
                sl_points = max(int(abs(sl_price - close_price) * 100000), 50)  # Convertir a puntos
                logger.debug(f"SELL sl_points calculation: abs({sl_price} - {close_price}) * 100000 = {sl_points}")
            except Exception as e:
                logger.error(f"Error calculando sl_points para SELL: {e}")
                return
        
        # Calcular TP en puntos (2:1 risk:reward por defecto)
        tp_points = sl_points * 2
        
        # Calcular tamaño de lote
        lot_size = self.connector.calculate_lot_size(
            risk_percent=self.risk_percent,
            sl_points=sl_points,
            symbol=self.symbol
        )
        
        # Ejecutar orden
        order_type = 'BUY' if latest_signal > 0 else 'SELL'
        result = self.connector.place_market_order(
            order_type=order_type,
            lot_size=lot_size,
            symbol=self.symbol,
            sl_points=sl_points,
            tp_points=tp_points,
            comment="SMC-LIT"
        )
        
        # Registrar operación
        if result:
            logger.info(f"Orden ejecutada: {order_type} {lot_size} {self.symbol} @ {latest_candle['close']}")
            self.trades_history.append({
                'timestamp': datetime.now(),
                'ticket': result['ticket'],
                'symbol': self.symbol,
                'type': order_type,
                'price': result['price'],
                'volume': lot_size,
                'sl': result['sl'],
                'tp': result['tp']
            })
            
            # Añadir a posiciones en seguimiento si se usa trailing stop
            if self.use_trailing:
                self.tracked_positions[result['ticket']] = {
                    'ticket': result['ticket'],
                    'type': order_type,
                    'entry_price': result['price'],
                    'sl': result['sl'],
                    'tp': result['tp'],
                    'atr': latest_candle['atr_14'],
                    'moved_to_be': False  # Movido a break-even
                }
    
    def manage_positions(self):
        """
        Gestiona posiciones abiertas (trailing stop, break-even).
        """
        if not self.use_trailing or not self.tracked_positions:
            return
        
        # Obtener posiciones abiertas
        open_positions = self.connector.get_open_positions(self.symbol)
        if not open_positions:
            return
        
        # Obtener precio actual
        symbol_info = self.connector.get_symbol_info(self.symbol)
        if not symbol_info:
            return
        
        # Actualizar cada posición
        for pos in open_positions:
            ticket = pos['ticket']
            
            # Verificar si estamos haciendo seguimiento
            if ticket not in self.tracked_positions:
                continue
            
            track_info = self.tracked_positions[ticket]
            pos_type = pos['type']
            current_price = pos['current_price']
            entry_price = pos['open_price']
            sl = pos['sl']
            tp = pos['tp']
            atr = track_info['atr']
            
            # Lógica para BUY
            if pos_type == 'BUY':
                # Calcular distancia en ATR
                profit_distance = (current_price - entry_price) / atr
                
                # Break-even cuando el beneficio es > 1 ATR
                if profit_distance >= 1.0 and not track_info['moved_to_be']:
                    new_sl = entry_price + 0.1 * atr  # Pequeño buffer
                    if self.connector.modify_position(ticket, sl=new_sl):
                        track_info['moved_to_be'] = True
                        track_info['sl'] = new_sl
                        logger.info(f"Posición {ticket} movida a break-even: SL={new_sl}")
                
                # Trailing stop cuando el beneficio es > 1.5 ATR
                elif profit_distance >= 1.5:
                    trailing_sl = current_price - 1.2 * atr
                    if trailing_sl > sl:
                        if self.connector.modify_position(ticket, sl=trailing_sl):
                            track_info['sl'] = trailing_sl
                            logger.info(f"Trailing stop actualizado: {ticket} SL={trailing_sl}")
            
            # Lógica para SELL
            elif pos_type == 'SELL':
                # Calcular distancia en ATR
                profit_distance = (entry_price - current_price) / atr
                
                # Break-even cuando el beneficio es > 1 ATR
                if profit_distance >= 1.0 and not track_info['moved_to_be']:
                    new_sl = entry_price - 0.1 * atr  # Pequeño buffer
                    if self.connector.modify_position(ticket, sl=new_sl):
                        track_info['moved_to_be'] = True
                        track_info['sl'] = new_sl
                        logger.info(f"Posición {ticket} movida a break-even: SL={new_sl}")
                
                # Trailing stop cuando el beneficio es > 1.5 ATR
                elif profit_distance >= 1.5:
                    trailing_sl = current_price + 1.2 * atr
                    if trailing_sl < sl or sl == 0:
                        if self.connector.modify_position(ticket, sl=trailing_sl):
                            track_info['sl'] = trailing_sl
                            logger.info(f"Trailing stop actualizado: {ticket} SL={trailing_sl}")
    
    def clean_closed_positions(self):
        """
        Limpia las posiciones cerradas del diccionario de seguimiento.
        """
        if not self.tracked_positions:
            return
        
        # Obtener posiciones abiertas
        open_positions = self.connector.get_open_positions(self.symbol)
        open_tickets = [pos['ticket'] for pos in open_positions]
        
        # Eliminar posiciones cerradas
        to_remove = []
        for ticket in self.tracked_positions:
            if ticket not in open_tickets:
                to_remove.append(ticket)
        
        for ticket in to_remove:
            del self.tracked_positions[ticket]
            logger.info(f"Posición {ticket} cerrada, eliminada del seguimiento")
    
    def trading_loop(self):
        """
        Bucle principal de trading.
        """
        logger.info(f"Iniciando bucle de trading para {self.symbol}")
        
        while self.running:
            try:
                # Verificar conexión
                if not self.connector.reconnect_if_needed():
                    logger.error("Conexión a MT5 perdida")
                    time.sleep(30)  # Esperar antes de reintentar
                    continue
                
                # 1. Obtener datos y señales
                df_raw, df_features, df_signals = self.get_latest_data()
                
                # 2. Procesar señales y ejecutar operaciones
                if df_signals is not None:
                    self.process_signals(df_signals)
                
                # 3. Gestionar posiciones abiertas
                self.manage_positions()
                
                # 4. Limpiar posiciones cerradas
                self.clean_closed_positions()
                
                # 5. Esperar para próxima actualización
                time.sleep(self.update_interval)
                
            except Exception as e:
                logger.error(f"Error en bucle de trading: {str(e)}")
                time.sleep(30)  # Esperar antes de reintentar
    
    def start(self):
        """
        Inicia el trader en un hilo separado.
        
        Returns:
            bool: True si iniciado correctamente
        """
        if self.running:
            logger.warning("El trader ya está en ejecución")
            return False
        
        if not self.initialize():
            logger.error("No se pudo inicializar el trader")
            return False
        
        self.running = True
        self.trade_thread = threading.Thread(target=self.trading_loop)
        self.trade_thread.daemon = True
        self.trade_thread.start()
        
        logger.info(f"Trader iniciado para {self.symbol} en {self.timeframe}")
        return True
    
    def stop(self):
        """
        Detiene el trader.
        
        Returns:
            bool: True si detenido correctamente
        """
        if not self.running:
            logger.warning("El trader no está en ejecución")
            return False
        
        self.running = False
        if self.trade_thread:
            self.trade_thread.join(timeout=10)
        
        # Desconectar MT5
        self.connector.disconnect()
        
        logger.info(f"Trader detenido para {self.symbol}")
        return True
    
    def get_stats(self):
        """
        Devuelve estadísticas del trader.
        
        Returns:
            dict: Estadísticas
        """
        open_positions = self.connector.get_open_positions(self.symbol)
        account_info = self.connector.get_account_info()
        
        return {
            'symbol': self.symbol,
            'timeframe': self.timeframe,
            'running': self.running,
            'open_positions': len(open_positions),
            'tracked_positions': len(self.tracked_positions),
            'signals_count': len(self.signals_history),
            'trades_count': len(self.trades_history),
            'account_balance': account_info['balance'] if account_info else None,
            'account_equity': account_info['equity'] if account_info else None
        }

# Ejemplo de uso
if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Crear trader
    trader = MT5Trader(
        symbol="EURUSD",
        timeframe="M5",
        risk_percent=1.0,
        update_interval=60  # 60 segundos
    )
    
    # Iniciar trader
    if trader.start():
        try:
            # Mantener vivo por 1 hora
            time.sleep(3600)
        except KeyboardInterrupt:
            logger.info("Interrumpido por usuario")
        finally:
            # Detener trader
            trader.stop() 