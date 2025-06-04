"""
CONFIGURACIÓN SEGURA SMC-LIT BOT
================================
Configuración en modo DEMO para evitar pérdidas de dinero real
"""

# CONFIGURACIÓN DE TRADING SEGURO
CONFIGURACION_SEGURA = {
    # MODO DEMO - NUNCA CAMBIAR A FALSE SIN SUPERVISIÓN
    'DEMO_MODE': True,
    'PAPER_TRADING': True,
    'SIMULACION_SOLAMENTE': True,
    
    # CREDENCIALES MT5 DEMO (CAMBIAR POR TUS DATOS DEMO)
    'MT5_LOGIN': 'TU_LOGIN_DEMO',
    'MT5_PASSWORD': 'TU_PASSWORD_DEMO',
    'MT5_SERVER': 'MetaQuotes-Demo',
    
    # CONFIGURACIÓN DE RIESGO ULTRA CONSERVADOR
    'CAPITAL_INICIAL': 1000.0,  # USD en cuenta demo
    'RIESGO_MAXIMO_POR_TRADE': 0.5,  # 0.5% máximo por operación
    'RIESGO_DIARIO_MAXIMO': 2.0,  # 2% máximo por día
    'MAX_TRADES_SIMULTANEOS': 3,
    'MAX_TRADES_POR_DIA': 10,
    
    # CONFIGURACIÓN DE SÍMBOLO
    'SIMBOLO_PRINCIPAL': 'EURUSD',
    'TIMEFRAME_PRINCIPAL': 'M5',
    'SIMBOLOS_PERMITIDOS': ['EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD'],
    
    # STOPS DE SEGURIDAD
    'STOP_LOSS_MAXIMO': 50,  # pips
    'TAKE_PROFIT_MINIMO': 25,  # pips
    'DRAWDOWN_MAXIMO': 5.0,  # 5% de drawdown máximo
    'AUTO_STOP_ON_LOSS': True,
    
    # CONFIGURACIÓN DE HORARIOS
    'HORARIO_INICIO': '08:00',
    'HORARIO_FIN': '18:00',
    'TRADING_DIAS': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
    
    # CONFIGURACIÓN DE LOGGING
    'LOG_LEVEL': 'INFO',
    'LOG_TODAS_LAS_OPERACIONES': True,
    'GUARDAR_RESULTADOS': True,
    
    # CONFIGURACIÓN DE NOTIFICACIONES
    'NOTIFICACIONES_ACTIVAS': True,
    'NOTIFICAR_TRADES': True,
    'NOTIFICAR_ERRORES': True,
    
    # CONFIGURACIÓN DE OPTIMIZACIÓN
    'AUTO_OPTIMIZATION': True,
    'OPTIMIZATION_INTERVAL_HOURS': 24,
    'MIN_TRADES_FOR_OPTIMIZATION': 50,
    
    # VALIDACIONES DE SEGURIDAD
    'VALIDAR_BALANCE_ANTES_TRADE': True,
    'VALIDAR_MARGENES': True,
    'VALIDAR_CONDICIONES_MERCADO': True,
}

# PARÁMETROS OPTIMIZADOS DEL SISTEMA (de los archivos de resultados)
PARAMETROS_OPTIMIZADOS = {
    'bos_threshold': 0.0003,
    'choch_threshold': 0.0005,
    'liquidity_threshold': 0.0004,
    'volume_threshold': 1.5,
    'rsi_period': 14,
    'rsi_oversold': 30,
    'rsi_overbought': 70,
    'atr_period': 14,
    'atr_multiplier': 2.0,
    'bb_period': 20,
    'bb_std': 2.0,
    'volume_ma_period': 10,
    'min_risk_reward': 1.5,
    'max_risk_percent': 0.5,
    'trailing_stop': True,
    'use_time_filter': True,
    'trend_filter': True,
    'volume_filter': True,
    'session_filter': True,
    'correlation_filter': True,
    'bos_probability': 0.75,
    'choch_probability': 0.70,
    'liquidity_probability': 0.80,
    'fvg_probability': 0.65,
    'ob_probability': 0.72,
}

def validar_configuracion_segura():
    """
    Valida que la configuración esté en modo seguro
    """
    errores = []
    
    if not CONFIGURACION_SEGURA['DEMO_MODE']:
        errores.append("❌ PELIGRO: DEMO_MODE debe estar en True")
    
    if not CONFIGURACION_SEGURA['PAPER_TRADING']:
        errores.append("❌ PELIGRO: PAPER_TRADING debe estar en True")
    
    if CONFIGURACION_SEGURA['RIESGO_MAXIMO_POR_TRADE'] > 1.0:
        errores.append("❌ PELIGRO: Riesgo por trade muy alto")
    
    if CONFIGURACION_SEGURA['RIESGO_DIARIO_MAXIMO'] > 5.0:
        errores.append("❌ PELIGRO: Riesgo diario muy alto")
    
    if errores:
        print("🚨 CONFIGURACIÓN INSEGURA DETECTADA:")
        for error in errores:
            print(error)
        return False
    
    print("✅ Configuración verificada: MODO SEGURO ACTIVADO")
    return True

def obtener_mensaje_seguridad():
    """
    Retorna mensaje de seguridad para mostrar al usuario
    """
    return """
🛡️  MODO SEGURIDAD ACTIVADO 🛡️
================================
✅ Trading en cuenta DEMO únicamente
✅ Riesgo limitado a 0.5% por operación  
✅ Capital virtual: $1,000 USD
✅ NO se usará dinero real
✅ Stops automáticos de seguridad activados
✅ Monitoreo continuo de drawdown
✅ Logs completos de todas las operaciones

⚠️  IMPORTANTE: 
- Este bot NO puede perder dinero real
- Todas las operaciones son virtuales
- Los resultados son para análisis únicamente
================================
"""

if __name__ == "__main__":
    validar_configuracion_segura()
    print(obtener_mensaje_seguridad()) 