#!/usr/bin/env python3
"""
CONFIGURACIÓN PARA TRADING REAL CON CUENTA DEMO
===============================================
Bot operando REAL pero conectado a cuenta DEMO de MT5
NO es simulación del bot - Envía órdenes reales a MT5 Demo
"""

# CONFIGURACIÓN DE TRADING REAL
TRADING_REAL_CONFIG = {
    # MODO REAL - NO SIMULACIÓN
    'bot_simulation_mode': False,        # ✅ Bot NO simula - Opera REAL
    'use_mt5_real_connection': True,     # ✅ Conexión REAL a MT5
    'send_real_orders': True,            # ✅ Envía órdenes REALES a MT5
    
    # CUENTA DEMO MT5 (Sin dinero real)
    'mt5_account_type': 'DEMO',          # ✅ Cuenta DEMO de MT5
    'mt5_demo_balance': 10000.0,         # Balance inicial cuenta demo
    
    # PARÁMETROS DE OPERACIÓN
    'symbol': 'EURUSD',
    'timeframe': 'M5',
    'risk_per_trade': 2.0,               # 2% por operación
    'max_daily_trades': 50,
    'max_concurrent_positions': 10,
    
    # CONFIGURACIÓN AGRESIVA
    'aggressive_mode': True,
    'scalping_enabled': True,
    'high_frequency_trading': True,
    'quick_entries': True,
    
    # GESTIÓN DE RIESGO
    'stop_loss_pips': 20,
    'take_profit_pips': 40,
    'trailing_stop': True,
    'max_drawdown_percent': 10.0,
    
    # CREDENCIALES MT5 DEMO (Seguras)
    'mt5_login': '164675960',            # Tu login demo
    'mt5_server': 'MetaQuotes-Demo',     # Servidor demo
    'mt5_password': 'Chevex9292!',       # Tu password demo
}

def validar_modo_real():
    """Valida que la configuración es para trading real (no simulado)"""
    
    print("🔍 VALIDANDO CONFIGURACIÓN DE TRADING REAL")
    print("=" * 50)
    
    # Verificar modo real
    if TRADING_REAL_CONFIG['bot_simulation_mode']:
        print("❌ ERROR: Bot configurado en modo simulación")
        return False
    else:
        print("✅ Bot configurado para TRADING REAL")
    
    # Verificar conexión MT5 real
    if not TRADING_REAL_CONFIG['use_mt5_real_connection']:
        print("❌ ERROR: Conexión MT5 deshabilitada")
        return False
    else:
        print("✅ Conexión REAL a MT5 habilitada")
    
    # Verificar envío de órdenes reales
    if not TRADING_REAL_CONFIG['send_real_orders']:
        print("❌ ERROR: Envío de órdenes deshabilitado")
        return False
    else:
        print("✅ Envío de órdenes REALES habilitado")
    
    # Confirmar cuenta demo
    if TRADING_REAL_CONFIG['mt5_account_type'] == 'DEMO':
        print("✅ Usando cuenta DEMO de MT5 (sin dinero real)")
    else:
        print("⚠️  ADVERTENCIA: Configurado para cuenta REAL")
    
    print("=" * 50)
    print("🎯 RESUMEN: Bot operará con funciones REALES en cuenta DEMO")
    return True

def obtener_mensaje_confirmacion():
    """Mensaje de confirmación para el usuario"""
    return """
🚀 CONFIGURACIÓN DE TRADING REAL
================================
✅ Bot ejecutará operaciones REALES (no simuladas)
✅ Se conectará a MetaTrader 5 via API
✅ Enviará órdenes BUY/SELL reales
✅ Usará cuenta DEMO (sin dinero real)
✅ Todas las funciones de trading activadas

⚠️  IMPORTANTE:
• El bot NO simula operaciones internamente
• Se conecta y opera directamente con MT5
• Usa tu cuenta DEMO de MT5 (sin riesgo)
• Operaciones aparecerán en MT5 normalmente

🎯 ¿Esto es lo que quieres? (El bot operando REAL en cuenta DEMO)
"""

if __name__ == "__main__":
    if validar_modo_real():
        print(obtener_mensaje_confirmacion())
    else:
        print("❌ Configuración inválida") 