#!/usr/bin/env python3
"""
INICIO RÁPIDO - BOT SMC-LIT AVANZADO
==================================
Ejecuta automáticamente el sistema completo
"""

import os
import sys

def mostrar_banner():
    """Mostrar banner de inicio"""
    print("🚀" + "=" * 80 + "🚀")
    print("🎯 BOT SMC-LIT AVANZADO - INICIO RÁPIDO")
    print("🚀" + "=" * 80 + "🚀")
    print()
    print("✅ CARACTERÍSTICAS INCLUIDAS:")
    print("  📈 NASDAQ 100 y S&P 500")
    print("  🐦 Análisis de noticias Twitter (@chevex9275518)")
    print("  🤖 Modo automático inteligente por defecto")
    print("  💱 Múltiples activos y timeframes")
    print("  🧠 Auto-optimización con IA")
    print("  📊 Análisis de noticias Fed/Powell")
    print()
    print("🚀" + "=" * 80 + "🚀")

def verificar_archivos():
    """Verificar que todos los archivos necesarios existen"""
    archivos_necesarios = [
        'twitter_news_analyzer.py',
        'main_advanced_with_indices.py'
    ]
    
    faltantes = []
    for archivo in archivos_necesarios:
        if not os.path.exists(archivo):
            faltantes.append(archivo)
    
    if faltantes:
        print("❌ Archivos faltantes:")
        for archivo in faltantes:
            print(f"  • {archivo}")
        return False
    
    print("✅ Todos los archivos necesarios están disponibles")
    return True

def main():
    """Función principal de inicio"""
    mostrar_banner()
    
    print("🔍 Verificando sistema...")
    if not verificar_archivos():
        print("❌ Sistema incompleto. Ejecuta primero la configuración.")
        return
    
    print("🚀 Iniciando bot avanzado...")
    print("=" * 50)
    
    try:
        # Importar y ejecutar el bot principal
        from main_advanced_with_indices import AdvancedTradingBotWithIndices
        
        bot = AdvancedTradingBotWithIndices()
        bot.main()
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        print("💡 Asegúrate de que todos los archivos estén en el mismo directorio")
    except KeyboardInterrupt:
        print("\n🛑 Inicio cancelado por usuario")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    main() 