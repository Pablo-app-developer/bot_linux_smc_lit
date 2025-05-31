"""
mt5_simulator.py - Simulador de MetaTrader5 para Linux

Este módulo simula las funciones básicas de MetaTrader5 cuando no está disponible,
permitiendo que el bot funcione en modo demo/simulación.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import random

class MT5Simulator:
    """Simulador básico de MetaTrader5 para desarrollo y testing"""
    
    # Constantes simuladas
    TIMEFRAME_M1 = 1
    TIMEFRAME_M5 = 5
    TIMEFRAME_M15 = 15
    TIMEFRAME_M30 = 30
    TIMEFRAME_H1 = 60
    TIMEFRAME_H4 = 240
    TIMEFRAME_D1 = 1440
    TIMEFRAME_W1 = 10080
    TIMEFRAME_MN1 = 43200
    
    ORDER_TYPE_BUY = 0
    ORDER_TYPE_SELL = 1
    
    POSITION_TYPE_BUY = 0
    POSITION_TYPE_SELL = 1
    
    TRADE_ACTION_DEAL = 1
    TRADE_ACTION_SLTP = 2
    
    TRADE_RETCODE_DONE = 10009
    
    ORDER_TIME_GTC = 0
    ORDER_FILLING_FOK = 2
    
    def __init__(self):
        self.initialized = False
        self.logged_in = False
        self.positions = []
        self.orders = []
        self.ticket_counter = 1000
        
        # Simulación de precios EUR/USD
        self.current_price = 1.0900
        self.spread = 0.00015  # 1.5 pips
        
        # Información de cuenta simulada
        self.account = {
            'login': 164675960,
            'server': 'MetaQuotes-Demo',
            'balance': 10000.0,
            'equity': 10000.0,
            'margin': 0.0,
            'margin_free': 10000.0,
            'margin_level': 0.0,
            'leverage': 100
        }
        
        # Información de símbolo simulada
        self.symbol_info_data = {
            'name': 'EURUSD',
            'bid': self.current_price,
            'ask': self.current_price + self.spread,
            'spread': int(self.spread * 100000),
            'trade_tick_value': 1.0,
            'trade_tick_size': 0.00001,
            'trade_contract_size': 100000.0,
            'volume_min': 0.01,
            'volume_step': 0.01,
            'point': 0.00001
        }
    
    def initialize(self):
        """Simula la inicialización de MT5"""
        self.initialized = True
        return True
    
    def login(self, login, password, server):
        """Simula el login a MT5"""
        if self.initialized:
            self.logged_in = True
            return True
        return False
    
    def shutdown(self):
        """Simula el cierre de MT5"""
        self.initialized = False
        self.logged_in = False
    
    def last_error(self):
        """Simula obtener el último error"""
        return (0, "No error")
    
    def terminal_info(self):
        """Simula obtener información del terminal"""
        if self.initialized and self.logged_in:
            return type('TerminalInfo', (), {'connected': True})()
        return None
    
    def account_info(self):
        """Simula obtener información de la cuenta"""
        if not self.logged_in:
            return None
        
        return type('AccountInfo', (), self.account)()
    
    def symbol_select(self, symbol, enable):
        """Simula seleccionar un símbolo"""
        return True
    
    def symbol_info(self, symbol):
        """Simula obtener información del símbolo"""
        if not self.logged_in:
            return None
        
        # Simular fluctuación de precios
        change = random.uniform(-0.0005, 0.0005)
        self.current_price += change
        self.symbol_info_data['bid'] = self.current_price
        self.symbol_info_data['ask'] = self.current_price + self.spread
        
        return type('SymbolInfo', (), self.symbol_info_data)()
    
    def symbol_info_tick(self, symbol):
        """Simula obtener tick actual del símbolo"""
        if not self.logged_in:
            return None
        
        return type('Tick', (), {
            'bid': self.current_price,
            'ask': self.current_price + self.spread
        })()
    
    def copy_rates_from_pos(self, symbol, timeframe, start_pos, count):
        """Simula obtener datos históricos"""
        if not self.logged_in:
            return None
        
        # Generar datos sintéticos realistas
        rates = []
        base_time = int(time.time()) - (count * timeframe * 60)
        
        for i in range(count):
            timestamp = base_time + (i * timeframe * 60)
            
            # Generar OHLC sintético con tendencia y volatilidad realista
            open_price = self.current_price + random.uniform(-0.01, 0.01)
            high_price = open_price + random.uniform(0, 0.005)
            low_price = open_price - random.uniform(0, 0.005)
            close_price = open_price + random.uniform(-0.003, 0.003)
            
            rates.append({
                'time': timestamp,
                'open': round(open_price, 5),
                'high': round(high_price, 5),
                'low': round(low_price, 5),
                'close': round(close_price, 5),
                'tick_volume': random.randint(100, 1000),
                'spread': int(self.spread * 100000),
                'real_volume': 0
            })
        
        return np.array(rates, dtype=[
            ('time', 'i8'), ('open', 'f8'), ('high', 'f8'), 
            ('low', 'f8'), ('close', 'f8'), ('tick_volume', 'i8'),
            ('spread', 'i4'), ('real_volume', 'i8')
        ])
    
    def copy_rates_range(self, symbol, timeframe, date_from, date_to):
        """Simula obtener datos históricos por rango de fechas"""
        if not self.logged_in:
            return None
        
        # Calcular número de velas aproximado
        time_diff = date_to - date_from
        count = int(time_diff.total_seconds() / (timeframe * 60))
        
        return self.copy_rates_from_pos(symbol, timeframe, 0, min(count, 5000))
    
    def order_send(self, request):
        """Simula enviar una orden"""
        if not self.logged_in:
            return type('OrderResult', (), {'retcode': 10018, 'comment': 'Not connected'})()
        
        ticket = self.ticket_counter
        self.ticket_counter += 1
        
        # Simular ejecución exitosa
        if request['action'] == self.TRADE_ACTION_DEAL:
            # Nueva posición
            position = {
                'ticket': ticket,
                'symbol': request['symbol'],
                'type': request['type'],
                'volume': request['volume'],
                'price_open': request['price'],
                'price_current': request['price'],
                'sl': request.get('sl', 0),
                'tp': request.get('tp', 0),
                'profit': 0.0,
                'swap': 0.0,
                'comment': request.get('comment', ''),
                'magic': request.get('magic', 0)
            }
            self.positions.append(position)
            
        elif request['action'] == self.TRADE_ACTION_SLTP:
            # Modificar posición existente
            for pos in self.positions:
                if pos['ticket'] == request['position']:
                    pos['sl'] = request.get('sl', pos['sl'])
                    pos['tp'] = request.get('tp', pos['tp'])
                    break
        
        return type('OrderResult', (), {
            'retcode': self.TRADE_RETCODE_DONE,
            'order': ticket,
            'comment': 'Request executed'
        })()
    
    def positions_get(self, symbol=None, ticket=None):
        """Simula obtener posiciones abiertas"""
        if not self.logged_in:
            return None
        
        filtered_positions = []
        
        for pos in self.positions:
            # Actualizar precio actual y profit
            pos['price_current'] = self.current_price
            if pos['type'] == self.POSITION_TYPE_BUY:
                pos['profit'] = (pos['price_current'] - pos['price_open']) * pos['volume'] * 100000
            else:
                pos['profit'] = (pos['price_open'] - pos['price_current']) * pos['volume'] * 100000
            
            # Filtrar por símbolo o ticket si se especifica
            if symbol and pos['symbol'] != symbol:
                continue
            if ticket and pos['ticket'] != ticket:
                continue
                
            filtered_positions.append(type('Position', (), pos)())
        
        return tuple(filtered_positions) if filtered_positions else None

# Instancia global del simulador
_simulator = MT5Simulator()

# Exportar funciones como si fueran del módulo MetaTrader5
initialize = _simulator.initialize
login = _simulator.login
shutdown = _simulator.shutdown
last_error = _simulator.last_error
terminal_info = _simulator.terminal_info
account_info = _simulator.account_info
symbol_select = _simulator.symbol_select
symbol_info = _simulator.symbol_info
symbol_info_tick = _simulator.symbol_info_tick
copy_rates_from_pos = _simulator.copy_rates_from_pos
copy_rates_range = _simulator.copy_rates_range
order_send = _simulator.order_send
positions_get = _simulator.positions_get

# Exportar constantes
TIMEFRAME_M1 = _simulator.TIMEFRAME_M1
TIMEFRAME_M5 = _simulator.TIMEFRAME_M5
TIMEFRAME_M15 = _simulator.TIMEFRAME_M15
TIMEFRAME_M30 = _simulator.TIMEFRAME_M30
TIMEFRAME_H1 = _simulator.TIMEFRAME_H1
TIMEFRAME_H4 = _simulator.TIMEFRAME_H4
TIMEFRAME_D1 = _simulator.TIMEFRAME_D1
TIMEFRAME_W1 = _simulator.TIMEFRAME_W1
TIMEFRAME_MN1 = _simulator.TIMEFRAME_MN1

ORDER_TYPE_BUY = _simulator.ORDER_TYPE_BUY
ORDER_TYPE_SELL = _simulator.ORDER_TYPE_SELL

POSITION_TYPE_BUY = _simulator.POSITION_TYPE_BUY
POSITION_TYPE_SELL = _simulator.POSITION_TYPE_SELL

TRADE_ACTION_DEAL = _simulator.TRADE_ACTION_DEAL
TRADE_ACTION_SLTP = _simulator.TRADE_ACTION_SLTP

TRADE_RETCODE_DONE = _simulator.TRADE_RETCODE_DONE

ORDER_TIME_GTC = _simulator.ORDER_TIME_GTC
ORDER_FILLING_FOK = _simulator.ORDER_FILLING_FOK 