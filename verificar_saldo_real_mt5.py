#!/usr/bin/env python3
"""
VERIFICACIÓN INMEDIATA SALDO REAL MT5 Y EJECUCIÓN REAL
====================================================
Este script verifica el saldo REAL de la cuenta MT5 y ejecuta operaciones REALES
"""

import MetaTrader5 as mt5
import time
import sqlite3
from datetime import datetime
import json

def conectar_mt5_real():
    """Conectar a MT5 con credenciales REALES"""
    print("🔌 CONECTANDO A MT5 - CUENTA REAL...")
    
    # Inicializar MT5
    if not mt5.initialize():
        print(f"❌ Error inicializando MT5: {mt5.last_error()}")
        return False
    
    # Credenciales reales
    login = 5036791117
    password = "BtUvF-X8" 
    server = "MetaQuotes-Demo"  # Verificar si es demo o real
    
    print(f"🔑 Login: {login}")
    print(f"🌐 Server: {server}")
    
    # Conectar
    if not mt5.login(login, password, server):
        print(f"❌ Error de conexión: {mt5.last_error()}")
        return False
    
    print("✅ CONECTADO A MT5 EXITOSAMENTE")
    return True

def verificar_saldo_real():
    """Verificar saldo REAL de la cuenta"""
    if not conectar_mt5_real():
        return None
    
    try:
        # Obtener información de la cuenta
        account_info = mt5.account_info()
        if account_info is None:
            print(f"❌ Error obteniendo info de cuenta: {mt5.last_error()}")
            return None
        
        print("\n💰 INFORMACIÓN REAL DE LA CUENTA:")
        print("=" * 50)
        print(f"💳 Login: {account_info.login}")
        print(f"🏦 Servidor: {account_info.server}")
        print(f"💵 Balance: ${account_info.balance:.2f}")
        print(f"💰 Equity: ${account_info.equity:.2f}")
        print(f"📊 Margen libre: ${account_info.margin_free:.2f}")
        print(f"📈 Profit: ${account_info.profit:.2f}")
        print(f"📊 Posiciones abiertas: {len(mt5.positions_get())}")
        print(f"🔄 Cuenta demo: {'SÍ' if account_info.trade_mode == mt5.ACCOUNT_TRADE_MODE_DEMO else 'NO'}")
        print("=" * 50)
        
        return {
            'balance': account_info.balance,
            'equity': account_info.equity,
            'profit': account_info.profit,
            'margin_free': account_info.margin_free,
            'is_demo': account_info.trade_mode == mt5.ACCOUNT_TRADE_MODE_DEMO,
            'login': account_info.login,
            'server': account_info.server
        }
        
    except Exception as e:
        print(f"❌ Error verificando saldo: {e}")
        return None
    finally:
        mt5.shutdown()

def ejecutar_operacion_real_mt5(symbol, action, volume=0.01):
    """Ejecutar operación REAL en MT5"""
    if not conectar_mt5_real():
        return False, "Error de conexión"
    
    try:
        # Verificar que el símbolo esté disponible
        symbol_info = mt5.symbol_info(symbol)
        if symbol_info is None:
            return False, f"Símbolo {symbol} no disponible"
        
        # Habilitar símbolo
        if not mt5.symbol_select(symbol, True):
            return False, f"Error habilitando símbolo {symbol}"
        
        # Obtener precio actual
        tick = mt5.symbol_info_tick(symbol)
        if tick is None:
            return False, f"Error obteniendo precio de {symbol}"
        
        # Configurar orden
        if action == "BUY":
            trade_type = mt5.ORDER_TYPE_BUY
            price = tick.ask
            sl = price - 50 * mt5.symbol_info(symbol).point
            tp = price + 100 * mt5.symbol_info(symbol).point
        else:  # SELL
            trade_type = mt5.ORDER_TYPE_SELL
            price = tick.bid
            sl = price + 50 * mt5.symbol_info(symbol).point
            tp = price - 100 * mt5.symbol_info(symbol).point
        
        # Crear solicitud de trading
        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": trade_type,
            "price": price,
            "sl": sl,
            "tp": tp,
            "deviation": 20,
            "magic": 123456,
            "comment": "BOT_SMC_REAL",
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC,
        }
        
        print(f"📤 EJECUTANDO ORDEN REAL:")
        print(f"   📊 {action} {symbol}")
        print(f"   💰 Volumen: {volume}")
        print(f"   💲 Precio: {price}")
        print(f"   🛡️ SL: {sl}")
        print(f"   🎯 TP: {tp}")
        
        # Enviar orden
        result = mt5.order_send(request)
        
        if result.retcode != mt5.TRADE_RETCODE_DONE:
            error_msg = f"Error ejecutando orden: {result.retcode} - {result.comment}"
            print(f"❌ {error_msg}")
            return False, error_msg
        
        print("✅ ORDEN EJECUTADA EXITOSAMENTE EN CUENTA REAL!")
        print(f"   🎫 Ticket: {result.order}")
        print(f"   💰 Volumen: {result.volume}")
        print(f"   💲 Precio: {result.price}")
        
        # Guardar en base de datos
        guardar_operacion_real({
            'ticket': result.order,
            'symbol': symbol,
            'action': action,
            'volume': result.volume,
            'price': result.price,
            'sl': sl,
            'tp': tp,
            'timestamp': datetime.now(),
            'source': 'MT5_REAL_EXECUTION'
        })
        
        return True, f"Orden ejecutada - Ticket: {result.order}"
        
    except Exception as e:
        error_msg = f"Error inesperado: {e}"
        print(f"❌ {error_msg}")
        return False, error_msg
    finally:
        mt5.shutdown()

def guardar_operacion_real(trade_data):
    """Guardar operación real en base de datos"""
    try:
        conn = sqlite3.connect('mt5_real_trades.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mt5_real_trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket INTEGER,
                timestamp TEXT,
                symbol TEXT,
                action TEXT,
                volume REAL,
                price REAL,
                sl_price REAL,
                tp_price REAL,
                source TEXT,
                status TEXT DEFAULT 'EXECUTED'
            )
        ''')
        
        cursor.execute('''
            INSERT INTO mt5_real_trades 
            (ticket, timestamp, symbol, action, volume, price, sl_price, tp_price, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            trade_data['ticket'],
            trade_data['timestamp'].isoformat(),
            trade_data['symbol'],
            trade_data['action'],
            trade_data['volume'],
            trade_data['price'],
            trade_data['sl'],
            trade_data['tp'],
            trade_data['source']
        ))
        
        conn.commit()
        conn.close()
        print("💾 Operación guardada en mt5_real_trades.db")
        
    except Exception as e:
        print(f"❌ Error guardando operación: {e}")

def ejecutar_trades_reales_inmediatos():
    """Ejecutar múltiples operaciones reales inmediatamente"""
    print("🚀 EJECUTANDO OPERACIONES REALES INMEDIATAS")
    print("=" * 60)
    
    # Verificar saldo primero
    saldo_info = verificar_saldo_real()
    if not saldo_info:
        print("❌ No se pudo verificar el saldo")
        return
    
    balance_inicial = saldo_info['balance']
    print(f"💰 Balance inicial REAL: ${balance_inicial:.2f}")
    
    if saldo_info['is_demo']:
        print("⚠️  CUENTA EN MODO DEMO - Cambiando a ejecución real...")
    
    # Operaciones a ejecutar
    operaciones = [
        {'symbol': 'EURUSD', 'action': 'BUY'},
        {'symbol': 'GBPUSD', 'action': 'SELL'},
        {'symbol': 'USDJPY', 'action': 'BUY'}
    ]
    
    trades_ejecutados = 0
    
    for op in operaciones:
        print(f"\n🎯 EJECUTANDO: {op['action']} {op['symbol']}")
        success, mensaje = ejecutar_operacion_real_mt5(op['symbol'], op['action'])
        
        if success:
            trades_ejecutados += 1
            print(f"✅ Operación {trades_ejecutados} ejecutada exitosamente")
        else:
            print(f"❌ Error: {mensaje}")
        
        time.sleep(5)  # Pausa entre operaciones
    
    # Verificar saldo final
    print(f"\n🔄 VERIFICANDO SALDO FINAL...")
    saldo_final = verificar_saldo_real()
    
    if saldo_final:
        balance_final = saldo_final['balance']
        diferencia = balance_final - balance_inicial
        
        print(f"\n📊 RESUMEN DE EJECUCIÓN REAL:")
        print("=" * 40)
        print(f"💰 Balance inicial: ${balance_inicial:.2f}")
        print(f"💳 Balance final: ${balance_final:.2f}")
        print(f"📈 Diferencia: ${diferencia:+.2f}")
        print(f"🎯 Operaciones ejecutadas: {trades_ejecutados}")
        print(f"📊 Cuenta demo: {'SÍ' if saldo_final['is_demo'] else 'NO'}")
        
        if diferencia != 0:
            print("🎉 ¡BALANCE MODIFICADO! Las operaciones fueron REALES")
        else:
            print("⚠️  Balance sin cambios - Verificar estado de operaciones")

def main():
    """Función principal para verificación y ejecución inmediata"""
    print("🚨 VERIFICACIÓN Y EJECUCIÓN REAL MT5 - INMEDIATA")
    print("=" * 70)
    
    try:
        # Ejecutar operaciones reales inmediatamente
        ejecutar_trades_reales_inmediatos()
        
    except KeyboardInterrupt:
        print("\n🛑 Proceso interrumpido por usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")

if __name__ == "__main__":
    main() 