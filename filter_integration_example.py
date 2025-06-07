#!/usr/bin/env python3
# Ejemplo de Integración del Filtro con Bot SMC-LIT
# ================================================

# EJEMPLO: Cómo usar el filtro en tu bot existente

from bot_signal_filter import signal_filter

def example_signal_processing():
    """Ejemplo de cómo procesar señales con el filtro"""
    
    # Ejemplo de señal del bot
    bot_signal = {
        'symbol': 'EURUSD',
        'action': 'BUY',
        'smc_signal': 'STRONG_BUY',
        'rsi_signal': 'BULLISH',
        'macd_signal': 'BULLISH',
        'volume': 'HIGH_VOLUME',
        'confidence': 0.85,
        'entry_price': 1.0950,
        'timestamp': '2024-06-05T22:00:00'
    }
    
    # Evaluar con el filtro inteligente
    should_execute, score, reason = signal_filter.should_execute_signal(bot_signal)
    
    if should_execute:
        print(f"✅ EJECUTAR SEÑAL: {bot_signal['action']} {bot_signal['symbol']}")
        print(f"   📊 Score: {score:.1f}")
        print(f"   💡 Motivo: {reason}")
        
        # AQUÍ VA TU CÓDIGO DE EJECUCIÓN DE OPERACIÓN
        # execute_trade(bot_signal)
        
    else:
        print(f"❌ RECHAZAR SEÑAL: {bot_signal['action']} {bot_signal['symbol']}")
        print(f"   📊 Score: {score:.1f}")
        print(f"   💡 Motivo: {reason}")

# INTEGRACIÓN EN TU BOT PRINCIPAL:
# ================================
# 
# 1. Importar el filtro:
#    from bot_signal_filter import signal_filter
#
# 2. Antes de ejecutar cualquier operación:
#    should_execute, score, reason = signal_filter.should_execute_signal(signal_data)
#    if should_execute:
#        # Ejecutar operación
#        execute_trade(signal_data)
#    else:
#        # Log de señal rechazada
#        log_rejected_signal(signal_data, reason)
#
# 3. Ver estadísticas diarias:
#    stats = signal_filter.get_daily_stats()
#    print(f"Señales aprobadas hoy: {stats['approved_signals']}")

if __name__ == "__main__":
    example_signal_processing()
