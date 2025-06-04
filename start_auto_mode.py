#!/usr/bin/env python3
"""
INICIO AUTOMÁTICO BOT SMC-LIT v2.0
=================================
Para VPS - Sin interacción del usuario
"""

import sys
import os
import signal
import time
from datetime import datetime

# Agregar directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def mostrar_banner():
    """Banner de inicio automático"""
    print("🤖" + "=" * 70 + "🤖")
    print("🚀 BOT SMC-LIT v2.0 - MODO AUTOMÁTICO VPS")
    print("🤖" + "=" * 70 + "🤖")
    print("📈 CARACTERÍSTICAS ACTIVAS:")
    print("  ✅ Twitter: Análisis de 7 categorías + ML")
    print("  ✅ Calendario económico: FinBERT + eventos")
    print("  ✅ NASDAQ y S&P 500: Trading automático")
    print("  ✅ Machine Learning: Predicciones avanzadas")
    print("  ✅ Modo: 100% automático sin intervención")
    print("🤖" + "=" * 70 + "🤖")
    print(f"📅 Iniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🤖" + "=" * 70 + "🤖")

def signal_handler(sig, frame):
    """Manejar señales de sistema"""
    print('\n🛑 Bot detenido por señal del sistema')
    sys.exit(0)

def main():
    """Función principal automática"""
    # Configurar manejadores de señales
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Mostrar banner
    mostrar_banner()
    
    try:
        # Importar bot principal
        from main_advanced_with_indices import AdvancedTradingBotWithIndices
        
        print("🔧 Inicializando bot en modo automático...")
        bot = AdvancedTradingBotWithIndices()
        
        # Forzar configuración automática sin preguntas
        print("🤖 Configurando modo automático sin interacción...")
        
        # Override del método de preguntas
        def configuracion_automatica_forzada():
            print("✅ Modo AUTOMÁTICO activado - VPS sin interacción")
            return bot.configurar_modo_automatico()
        
        # Reemplazar método
        bot.preguntar_modo_operacion = configuracion_automatica_forzada
        
        # Ejecutar bot
        print("🚀 Iniciando sistema completo...")
        bot.main()
        
    except KeyboardInterrupt:
        print("\n🛑 Bot detenido por usuario")
    except Exception as e:
        print(f"\n❌ Error ejecutando bot: {e}")
        import traceback
        traceback.print_exc()
        
        # Esperar antes de reiniciar
        print("⏳ Esperando 30 segundos antes de reiniciar...")
        time.sleep(30)
        
        # Reiniciar automáticamente
        print("🔄 Reiniciando bot...")
        main()

 