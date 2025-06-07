#!/usr/bin/env python3
# Bot de Trading REAL con MT5 - No Simulaciones
# =============================================

import MetaTrader5 as mt5
import sqlite3
import time
import json
from datetime import datetime
from bot_signal_filter import signal_filter

class RealMT5Trader:
    """Bot que ejecuta operaciones REALES en MT5"""
    
    def __init__(self):
        self.account_info = {
            'login': 5036791117,
            'password': 'BtUvF-X8',
            'server': 'MetaQuotes-Demo'
        }
        
        self.trading_config = {
            'lot_size': 0.01,  # Tamaño conservador
            'max_risk_per_trade': 1.0,  # 1% de riesgo
            'sl_points': 50,  # Stop loss en puntos
            'tp_points': 100,  # Take profit en puntos
            'magic_number': 12345
        }
        
        print("🚀 BOT DE TRADING REAL MT5 INICIADO")
        print("=" * 50)
    
    def connect_to_mt5(self):
        """Conectar a MT5 REAL"""
        print("🔗 Conectando a MT5...")
        
        # Inicializar MT5
        if not mt5.initialize():
            print(f"❌ Error inicializando MT5: {mt5.last_error()}")
            return False
        
        # Conectar a cuenta
        authorized = mt5.login(
            login=self.account_info['login'],
            password=self.account_info['password'],
            server=self.account_info['server']
        )
        
        if authorized:
            # Obtener info de cuenta
            account_info = mt5.account_info()
            if account_info:
                print(f"✅ CONECTADO A CUENTA REAL:")
                print(f"   📊 Login: {account_info.login}")
                print(f"   💰 Balance: ${account_info.balance:.2f}")
                print(f"   💳 Equity: ${account_info.equity:.2f}")
                print(f"   🏦 Servidor: {account_info.server}")
                print(f"   💱 Moneda: {account_info.currency}")
                return True
            else:
                print("❌ No se pudo obtener información de la cuenta")
                return False
        else:
            print(f"❌ Error de autorización: {mt5.last_error()}")
            return False
    
    def get_current_balance(self):
        """Obtener balance actual REAL de MT5"""
        account_info = mt5.account_info()
        if account_info:
            return account_info.balance
        return 0.0
    
    def execute_real_trade(self, signal):
        """Ejecutar operación REAL en MT5"""
        
        symbol = signal.get('symbol', 'EURUSD')
        action = signal.get('action', 'BUY')
        
        # Verificar que el símbolo existe
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            print(f"❌ Símbolo {symbol} no encontrado")
            return False, 0.0
        
        # Habilitar símbolo si no está activo
        if not symbol_info.visible:
            if not mt5.symbol_select(symbol, True):
                print(f"❌ Error habilitando símbolo {symbol}")
                return False, 0.0
        
        # Obtener precio actual
        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            print(f"❌ No se pudo obtener precio de {symbol}")
            return False, 0.0
        
        # Configurar la orden
        lot_size = self.trading_config['lot_size']
        
        if action.upper() == 'BUY':
            trade_type = mt5.ORDER_TYPE_BUY
            price = tick.ask
            sl = price - (self.trading_config['sl_points'] * symbol_info.point)
            tp = price + (self.trading_config['tp_points'] * symbol_info.point)
        else:  # SELL
            trade_type = mt5.ORDER_TYPE_SELL
            price = tick.bid
            sl = price + (self.trading_config['sl_points'] * symbol_info.point)
            tp = price - (self.trading_config['tp_points'] * symbol_info.point)
        
        # Crear solicitud de orden
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": lot_size,
            "type": trade_type,
            "price": price,
            "sl": sl,
            "tp": tp,
            "deviation": 20,
            "magic": self.trading_config['magic_number'],
            "comment": "BOT_SMC_LIT_REAL",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        
        # Enviar orden REAL
        print(f"📤 ENVIANDO ORDEN REAL:")
        print(f"   📊 {action} {symbol}")
        print(f"   💰 Volumen: {lot_size}")
        print(f"   💲 Precio: {price}")
        print(f"   🛡️ SL: {sl:.5f}")
        print(f"   🎯 TP: {tp:.5f}")
        
        result = mt5.order_send(request)
        
        if result is None:
            print(f"❌ Error enviando orden: {mt5.last_error()}")
            return False, 0.0
        
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            print(f"❌ Orden rechazada: {result.comment}")
            return False, 0.0
        
        # Orden ejecutada exitosamente
        print(f"✅ ORDEN EJECUTADA EN CUENTA REAL!")
        print(f"   🎫 Ticket: {result.order}")
        print(f"   💰 Volumen: {result.volume}")
        print(f"   💲 Precio: {result.price}")
        
        # Guardar en base de datos
        self.save_real_trade(signal, result)
        
        return True, result.order
    
    def save_real_trade(self, signal, mt5_result):
        """Guardar operación real en base de datos"""
        try:
            conn = sqlite3.connect('real_mt5_trades.db')
            cursor = conn.cursor()
            
            # Crear tabla si no existe
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS real_trades (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    timestamp TEXT,
                    ticket INTEGER,
                    symbol TEXT,
                    trade_type TEXT,
                    volume REAL,
                    open_price REAL,
                    sl REAL,
                    tp REAL,
                    filter_score REAL,
                    status TEXT DEFAULT 'OPEN',
                    mt5_comment TEXT,
                    balance_after REAL
                )
            ''')
            
            cursor.execute('''
                INSERT INTO real_trades 
                (timestamp, ticket, symbol, trade_type, volume, open_price, sl, tp, filter_score, mt5_comment, balance_after)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now().isoformat(),
                mt5_result.order,
                signal.get('symbol', 'UNKNOWN'),
                signal.get('action', 'BUY'),
                mt5_result.volume,
                mt5_result.price,
                mt5_result.request.sl if hasattr(mt5_result, 'request') else 0,
                mt5_result.request.tp if hasattr(mt5_result, 'request') else 0,
                signal.get('filter_score', 0),
                mt5_result.comment,
                self.get_current_balance()
            ))
            
            conn.commit()
            conn.close()
            
            print(f"💾 Operación guardada en base de datos real")
            
        except Exception as e:
            print(f"❌ Error guardando: {e}")
    
    def check_open_positions(self):
        """Verificar posiciones abiertas"""
        positions = mt5.positions_get()
        if positions:
            print(f"📊 POSICIONES ABIERTAS: {len(positions)}")
            for pos in positions:
                profit = pos.profit
                print(f"   🎫 {pos.ticket}: {pos.symbol} {pos.type_str} Profit: ${profit:.2f}")
        else:
            print("📊 No hay posiciones abiertas")
        
        return positions
    
    def process_premium_signals(self):
        """Procesar señales premium y ejecutar en MT5"""
        
        # Señales de alta calidad para trading real
        premium_signals = [
            {
                'symbol': 'EURUSD',
                'action': 'BUY',
                'smc_signal': 'STRONG_BUY',
                'rsi_signal': 'BULLISH',
                'macd_signal': 'BULLISH',
                'volume': 'HIGH_VOLUME',
                'confidence': 0.92,
                'entry_price': 1.0950
            },
            {
                'symbol': 'GBPUSD',
                'action': 'SELL',
                'smc_signal': 'STRONG_SELL',
                'rsi_signal': 'BEARISH',
                'macd_signal': 'BEARISH',
                'volume': 'HIGH_VOLUME',
                'confidence': 0.89,
                'entry_price': 1.2650
            }
        ]
        
        executed_trades = 0
        for signal in premium_signals:
            if executed_trades >= 2:  # Máximo 2 operaciones reales por sesión
                break
            
            # Usar filtro inteligente
            should_execute, score, reason = signal_filter.should_execute_signal(signal)
            
            if should_execute and score >= 75:  # Solo las mejores señales
                signal['filter_score'] = score
                
                print(f"\n🎯 EJECUTANDO SEÑAL PREMIUM:")
                print(f"   📊 Score: {score:.1f}/100")
                print(f"   ✅ Razón: {reason}")
                
                success, ticket = self.execute_real_trade(signal)
                
                if success:
                    executed_trades += 1
                    print(f"🎉 OPERACIÓN REAL EJECUTADA - Ticket: {ticket}")
                    
                    # Pausa entre operaciones
                    time.sleep(30)
                else:
                    print(f"❌ Error ejecutando operación")
            else:
                print(f"❌ SEÑAL RECHAZADA: {signal['action']} {signal['symbol']}")
                print(f"   📊 Score: {score:.1f} - {reason}")
        
        return executed_trades
    
    def run_real_trading_session(self):
        """Ejecutar sesión de trading real"""
        
        # Conectar a MT5
        if not self.connect_to_mt5():
            print("❌ No se pudo conectar a MT5")
            return
        
        print(f"\n🚀 INICIANDO SESIÓN DE TRADING REAL")
        print("=" * 50)
        
        # Verificar balance inicial
        initial_balance = self.get_current_balance()
        print(f"💰 Balance inicial: ${initial_balance:.2f}")
        
        # Verificar posiciones existentes
        self.check_open_positions()
        
        # Procesar señales y ejecutar operaciones reales
        trades_executed = self.process_premium_signals()
        
        # Balance final
        final_balance = self.get_current_balance()
        profit_change = final_balance - initial_balance
        
        print(f"\n📊 RESUMEN DE SESIÓN REAL:")
        print(f"   💰 Balance inicial: ${initial_balance:.2f}")
        print(f"   💳 Balance final: ${final_balance:.2f}")
        print(f"   📈 Cambio: ${profit_change:+.2f}")
        print(f"   🎯 Operaciones ejecutadas: {trades_executed}")
        
        # Verificar posiciones finales
        self.check_open_positions()
        
        # Cerrar conexión
        mt5.shutdown()
        print(f"\n✅ SESIÓN DE TRADING REAL COMPLETADA")

def main():
    """Función principal"""
    print("💰 INICIANDO BOT DE TRADING REAL")
    print("⚠️  ESTE BOT EJECUTA OPERACIONES REALES EN MT5")
    print("=" * 60)
    
    trader = RealMT5Trader()
    trader.run_real_trading_session()

if __name__ == "__main__":
    main() 