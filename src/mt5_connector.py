"""
mt5_connector.py - Módulo para la conexión y operaciones con MetaTrader 5

Este módulo gestiona toda la comunicación con MetaTrader 5, incluyendo:
- Inicialización y autenticación
- Descarga de datos históricos
- Ejecución de órdenes
- Gestión de posiciones abiertas
- Monitoreo de cuenta
"""

import os
import time
import logging
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import pytz
from dotenv import load_dotenv

# Importar MetaTrader5 con manejo de errores
try:
    import MetaTrader5 as mt5
    print("MetaTrader5 real importado exitosamente")
except ImportError:
    print("MetaTrader5 no disponible, usando simulador...")
    try:
        from . import mt5_simulator as mt5
    except ImportError:
        import mt5_simulator as mt5
    print("Simulador de MT5 cargado para desarrollo en Linux")

# Configurar logging
logger = logging.getLogger('mt5_connector')

# Cargar variables de entorno
load_dotenv()

class MT5Connector:
    """
    Clase para gestionar conexiones y operaciones con MetaTrader 5.
    Implementa funcionalidades para trading algorítmico profesional.
    """
    
    def __init__(self, 
                 login=None, 
                 password=None, 
                 server=None,
                 symbol="EURUSD",
                 timeframe="M5",
                 max_retries=3,
                 retry_wait=5):
        """
        Inicializa el conector de MT5.
        
        Args:
            login: ID de cuenta MT5 (int)
            password: Contraseña (str)
            server: Servidor MT5 (str)
            symbol: Símbolo a operar (str)
            timeframe: Timeframe para análisis (str)
            max_retries: Intentos máximos de conexión (int)
            retry_wait: Espera entre intentos (int)
        """
        # Obtener credenciales de variables de entorno si no se especifican
        self.login = login or int(os.getenv('MT5_LOGIN'))
        self.password = password or os.getenv('MT5_PASSWORD')
        self.server = server or os.getenv('MT5_SERVER')
        
        # Parámetros de trading
        self.symbol = symbol or os.getenv('SYMBOL', 'EURUSD')
        self.timeframe_str = timeframe or os.getenv('TIMEFRAME', 'M5')
        
        # Mapeo de timeframes
        self.timeframes = {
            'M1': mt5.TIMEFRAME_M1,
            'M5': mt5.TIMEFRAME_M5,
            'M15': mt5.TIMEFRAME_M15,
            'M30': mt5.TIMEFRAME_M30,
            'H1': mt5.TIMEFRAME_H1,
            'H4': mt5.TIMEFRAME_H4,
            'D1': mt5.TIMEFRAME_D1,
            'W1': mt5.TIMEFRAME_W1,
            'MN1': mt5.TIMEFRAME_MN1
        }
        self.timeframe = self.timeframes.get(self.timeframe_str, mt5.TIMEFRAME_M5)
        
        # Parámetros de reconexión
        self.max_retries = max_retries
        self.retry_wait = retry_wait
        self._connected = False
        
        # Inicialización y conexión
        self.connect()
        
    def connect(self):
        """
        Inicializa MT5 y establece conexión con la cuenta.
        """
        logger.info("Inicializando conexión con MetaTrader 5...")
        
        # Intentar inicializar MT5 con reintentos
        for attempt in range(self.max_retries):
            if mt5.initialize():
                break
            else:
                logger.warning(f"Intento {attempt+1}/{self.max_retries} fallido: {mt5.last_error()}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_wait)
        
        # Verificar inicialización
        if not mt5.initialize():
            logger.error(f"Error inicializando MT5: {mt5.last_error()}")
            self._connected = False
            return False
        
        # Intentar login con reintentos
        for attempt in range(self.max_retries):
            if mt5.login(login=self.login, password=self.password, server=self.server):
                logger.info(f"Conectado a MT5: {mt5.account_info().server}, cuenta #{mt5.account_info().login}")
                self._connected = True
                return True
            else:
                logger.warning(f"Intento de login {attempt+1}/{self.max_retries} fallido: {mt5.last_error()}")
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_wait)
        
        logger.error(f"Error de login en MT5: {mt5.last_error()}")
        self._connected = False
        return False
    
    def reconnect_if_needed(self):
        """
        Verifica la conexión y reconecta si es necesario.
        
        Returns:
            bool: True si está conectado, False en caso contrario
        """
        if not self._connected or not mt5.terminal_info():
            logger.warning("Conexión perdida. Intentando reconectar...")
            return self.connect()
        return True
    
    def disconnect(self):
        """
        Cierra la conexión con MT5.
        """
        if self._connected:
            mt5.shutdown()
            self._connected = False
            logger.info("Desconectado de MT5")
    
    def get_account_info(self):
        """
        Obtiene información de la cuenta.
        
        Returns:
            dict: Información de la cuenta
        """
        if not self.reconnect_if_needed():
            return None
        
        account = mt5.account_info()
        if account is None:
            logger.error(f"Error obteniendo información de cuenta: {mt5.last_error()}")
            return None
        
        # Convertir a diccionario
        return {
            'login': account.login,
            'server': account.server,
            'balance': account.balance,
            'equity': account.equity,
            'margin': account.margin,
            'free_margin': account.margin_free,
            'margin_level': account.margin_level,
            'leverage': account.leverage
        }
    
    def get_symbol_info(self, symbol=None):
        """
        Obtiene información del símbolo.
        
        Args:
            symbol: Símbolo (str), si None usa el predeterminado
            
        Returns:
            dict: Información del símbolo
        """
        if not self.reconnect_if_needed():
            return None
        
        symbol = symbol or self.symbol
        mt5.symbol_select(symbol, True)
        info = mt5.symbol_info(symbol)
        
        if info is None:
            logger.error(f"Error obteniendo información de {symbol}: {mt5.last_error()}")
            return None
        
        # Convertir a diccionario
        return {
            'symbol': info.name,
            'bid': info.bid,
            'ask': info.ask,
            'spread': info.spread,
            'tick_value': info.trade_tick_value,
            'tick_size': info.trade_tick_size,
            'contract_size': info.trade_contract_size,
            'volume_min': info.volume_min,
            'volume_step': info.volume_step
        }
    
    def fetch_ohlc_data(self, symbol=None, timeframe=None, num_candles=1000, start_date=None, end_date=None):
        """
        Descarga datos OHLC históricos.
        
        Args:
            symbol: Símbolo (str)
            timeframe: Timeframe (str)
            num_candles: Número de velas a descargar (int)
            start_date: Fecha inicio (datetime)
            end_date: Fecha fin (datetime)
            
        Returns:
            pd.DataFrame: Datos OHLC
        """
        if not self.reconnect_if_needed():
            return None
        
        symbol = symbol or self.symbol
        tf = timeframe or self.timeframe
        
        if isinstance(tf, str):
            tf = self.timeframes.get(tf, self.timeframe)
        
        # Seleccionar símbolo
        mt5.symbol_select(symbol, True)
        
        # Obtener datos
        if start_date and end_date:
            # Convertir a timestamp UTC
            if not isinstance(start_date, datetime):
                start_date = datetime.fromisoformat(start_date)
            if not isinstance(end_date, datetime):
                end_date = datetime.fromisoformat(end_date)
                
            timezone = pytz.timezone("UTC")
            start_date = timezone.localize(start_date) if start_date.tzinfo is None else start_date
            end_date = timezone.localize(end_date) if end_date.tzinfo is None else end_date
            
            rates = mt5.copy_rates_range(symbol, tf, start_date, end_date)
        else:
            # Obtener n velas desde la posición 0 (actual)
            rates = mt5.copy_rates_from_pos(symbol, tf, 0, num_candles)
        
        if rates is None or len(rates) == 0:
            logger.error(f"Error descargando datos de {symbol}: {mt5.last_error()}")
            return None
        
        # Convertir a DataFrame
        df = pd.DataFrame(rates)
        df['time'] = pd.to_datetime(df['time'], unit='s')
        df.rename(columns={
            'time': 'datetime',
            'open': 'open',
            'high': 'high',
            'low': 'low',
            'close': 'close',
            'tick_volume': 'volume',
            'spread': 'spread',
            'real_volume': 'real_volume'
        }, inplace=True)
        
        # Añadir símbolo
        df['symbol'] = symbol
        
        logger.info(f"Descargadas {len(df)} velas de {symbol} {self.timeframe_str}")
        return df
    
    def calculate_lot_size(self, risk_percent, sl_points, symbol=None):
        """
        Calcula el tamaño de lote basado en el riesgo y stop loss.
        
        Args:
            risk_percent: Porcentaje de riesgo (float)
            sl_points: Distancia en puntos al stop loss (float)
            symbol: Símbolo (str)
            
        Returns:
            float: Tamaño de lote
        """
        if not self.reconnect_if_needed():
            return 0.01  # Valor mínimo por defecto
        
        symbol = symbol or self.symbol
        account_info = self.get_account_info()
        symbol_info = self.get_symbol_info(symbol)
        
        if not account_info or not symbol_info:
            return 0.01
        
        # Calcular valor monetario por pip
        tick_size = symbol_info['tick_size']
        tick_value = symbol_info['tick_value']
        
        # Riesgo monetario
        risk_money = account_info['equity'] * (risk_percent / 100)
        
        # Calcular tamaño de lote
        pip_value = tick_value / tick_size
        sl_value = sl_points * pip_value
        
        if sl_value == 0:
            logger.warning("Stop loss demasiado pequeño, usando valor por defecto")
            return 0.01
        
        lot_size = risk_money / sl_value
        
        # Ajustar a los límites del broker
        min_volume = symbol_info['volume_min']
        volume_step = symbol_info['volume_step']
        
        # Redondear al volumen_step más cercano
        lot_size = max(min_volume, round(lot_size / volume_step) * volume_step)
        
        logger.info(f"Lot size calculado: {lot_size} para {risk_percent}% de riesgo y SL de {sl_points} puntos")
        return lot_size
    
    def place_market_order(self, order_type, lot_size, symbol=None, sl_points=None, tp_points=None, comment="SMC-LIT"):
        """
        Coloca una orden de mercado.
        
        Args:
            order_type: Tipo de orden ('BUY' o 'SELL')
            lot_size: Tamaño del lote (float)
            symbol: Símbolo (str)
            sl_points: Stop Loss en puntos (int)
            tp_points: Take Profit en puntos (int)
            comment: Comentario (str)
            
        Returns:
            dict: Resultado de la orden
        """
        if not self.reconnect_if_needed():
            return None
        
        symbol = symbol or self.symbol
        
        # Seleccionar símbolo
        mt5.symbol_select(symbol, True)
        
        # Obtener precios actuales
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            logger.error(f"Error obteniendo información de {symbol}: {mt5.last_error()}")
            return None
        
        # Determinar tipo de orden
        if order_type.upper() == 'BUY':
            order_type = mt5.ORDER_TYPE_BUY
            price = symbol_info.ask
            sl = price - sl_points * symbol_info.point if sl_points else 0
            tp = price + tp_points * symbol_info.point if tp_points else 0
        elif order_type.upper() == 'SELL':
            order_type = mt5.ORDER_TYPE_SELL
            price = symbol_info.bid
            sl = price + sl_points * symbol_info.point if sl_points else 0
            tp = price - tp_points * symbol_info.point if tp_points else 0
        else:
            logger.error(f"Tipo de orden inválido: {order_type}")
            return None
        
        # Preparar solicitud de orden
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": float(lot_size),
            "type": order_type,
            "price": price,
            "sl": sl,
            "tp": tp,
            "deviation": 20,
            "magic": 123456,  # Identificador único para este bot
            "comment": comment,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_FOK,
        }
        
        # Enviar orden
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logger.error(f"Error colocando orden: {result.retcode}, {result.comment}")
            return None
        
        logger.info(f"Orden {order_type} ejecutada: {lot_size} lotes de {symbol} a {price}")
        
        # Devolver información de la orden
        return {
            'ticket': result.order,
            'symbol': symbol,
            'type': 'BUY' if order_type == mt5.ORDER_TYPE_BUY else 'SELL',
            'volume': lot_size,
            'price': price,
            'sl': sl,
            'tp': tp
        }
    
    def get_open_positions(self, symbol=None):
        """
        Obtiene las posiciones abiertas.
        
        Args:
            symbol: Símbolo (str)
            
        Returns:
            list: Posiciones abiertas
        """
        if not self.reconnect_if_needed():
            return []
        
        symbol = symbol or self.symbol
        
        # Obtener posiciones
        if symbol:
            positions = mt5.positions_get(symbol=symbol)
        else:
            positions = mt5.positions_get()
            
        if positions is None:
            logger.error(f"Error obteniendo posiciones: {mt5.last_error()}")
            return []
        
        # Convertir a lista de diccionarios
        positions_list = []
        for pos in positions:
            positions_list.append({
                'ticket': pos.ticket,
                'symbol': pos.symbol,
                'type': 'BUY' if pos.type == mt5.POSITION_TYPE_BUY else 'SELL',
                'volume': pos.volume,
                'open_price': pos.price_open,
                'current_price': pos.price_current,
                'sl': pos.sl,
                'tp': pos.tp,
                'profit': pos.profit,
                'swap': pos.swap,
                'comment': pos.comment,
                'magic': pos.magic
            })
        
        return positions_list
    
    def modify_position(self, ticket, sl=None, tp=None):
        """
        Modifica una posición abierta.
        
        Args:
            ticket: Número de ticket (int)
            sl: Nuevo Stop Loss (float)
            tp: Nuevo Take Profit (float)
            
        Returns:
            bool: True si éxito, False en caso contrario
        """
        if not self.reconnect_if_needed():
            return False
        
        # Obtener la posición
        position = mt5.positions_get(ticket=ticket)
        if not position:
            logger.error(f"Posición {ticket} no encontrada")
            return False
        
        position = position[0]
        
        # Preparar solicitud de modificación
        request = {
            "action": mt5.TRADE_ACTION_SLTP,
            "symbol": position.symbol,
            "position": ticket,
            "sl": sl if sl is not None else position.sl,
            "tp": tp if tp is not None else position.tp
        }
        
        # Enviar solicitud
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logger.error(f"Error modificando posición: {result.retcode}, {result.comment}")
            return False
        
        logger.info(f"Posición {ticket} modificada: SL={sl}, TP={tp}")
        return True
    
    def close_position(self, ticket):
        """
        Cierra una posición abierta.
        
        Args:
            ticket: Número de ticket (int)
            
        Returns:
            bool: True si éxito, False en caso contrario
        """
        if not self.reconnect_if_needed():
            return False
        
        # Obtener la posición
        position = mt5.positions_get(ticket=ticket)
        if not position:
            logger.error(f"Posición {ticket} no encontrada")
            return False
        
        position = position[0]
        
        # Determinar el tipo de orden para cerrar
        close_type = mt5.ORDER_TYPE_SELL if position.type == mt5.POSITION_TYPE_BUY else mt5.ORDER_TYPE_BUY
        price = mt5.symbol_info_tick(position.symbol).bid if position.type == mt5.POSITION_TYPE_BUY else mt5.symbol_info_tick(position.symbol).ask
        
        # Preparar solicitud de cierre
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": position.symbol,
            "volume": position.volume,
            "type": close_type,
            "position": ticket,
            "price": price,
            "deviation": 20,
            "magic": 123456,
            "comment": "Cierre SMC-LIT",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_FOK,
        }
        
        # Enviar solicitud
        result = mt5.order_send(request)
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            logger.error(f"Error cerrando posición: {result.retcode}, {result.comment}")
            return False
        
        logger.info(f"Posición {ticket} cerrada")
        return True
    
    def close_all_positions(self, symbol=None):
        """
        Cierra todas las posiciones abiertas.
        
        Args:
            symbol: Símbolo (str)
            
        Returns:
            int: Número de posiciones cerradas
        """
        positions = self.get_open_positions(symbol)
        closed = 0
        
        for pos in positions:
            if self.close_position(pos['ticket']):
                closed += 1
        
        logger.info(f"Cerradas {closed} de {len(positions)} posiciones")
        return closed

# Ejemplo de uso
if __name__ == "__main__":
    # Configurar logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    
    # Crear conector
    connector = MT5Connector()
    
    # Obtener información de cuenta
    account_info = connector.get_account_info()
    print(f"Cuenta: {account_info}")
    
    # Obtener datos OHLC
    data = connector.fetch_ohlc_data(num_candles=100)
    print(f"Datos: {len(data)} filas")
    print(data.head())
    
    # Desconectar
    connector.disconnect() 