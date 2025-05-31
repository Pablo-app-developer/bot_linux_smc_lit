#!/usr/bin/env python3
"""
START SMC-LIT BOT - Script de inicio simplificado
Ejecuta el bot de trading algorítmico SMC-LIT
"""

import sys
import os
import subprocess
import time
from datetime import datetime

def print_banner():
    """Imprime banner del bot"""
    print("=" * 60)
    print("🚀 SMC-LIT ALGORITHMIC TRADING BOT")
    print("=" * 60)
    print("📊 Smart Money Concepts + Liquidity Inducement Theorem")
    print("🤖 Powered by AI/ML - XGBoost & Reinforcement Learning")
    print("💹 Multi-Currency Forex Trading")
    print("=" * 60)
    print(f"⏰ Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

def check_environment():
    """Verifica que el entorno esté configurado correctamente"""
    print("🔍 Verificando entorno...")
    
    # Verificar Python
    if sys.version_info < (3, 8):
        print("❌ Error: Se requiere Python 3.8 o superior")
        sys.exit(1)
    print(f"✅ Python {sys.version.split()[0]} OK")
    
    # Verificar archivos necesarios
    required_files = [
        'main.py',
        'src/mt5_connector.py',
        'src/mt5_simulator.py',
        'requirements.txt',
        '.env'
    ]
    
    for file in required_files:
        if not os.path.exists(file):
            print(f"❌ Error: Archivo requerido no encontrado: {file}")
            sys.exit(1)
    print("✅ Archivos necesarios OK")
    
    # Verificar dependencias
    try:
        import pandas
        import numpy
        import sklearn
        import xgboost
        print("✅ Dependencias principales OK")
    except ImportError as e:
        print(f"❌ Error: Falta dependencia: {e}")
        print("💡 Ejecuta: pip install -r requirements.txt")
        sys.exit(1)

def get_user_config():
    """Obtiene configuración del usuario"""
    print("\n📝 Configuración de Trading:")
    print("-" * 30)
    
    # Símbolos disponibles
    symbols = ['EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 'USDCAD', 'NZDUSD', 'USDCHF']
    print("💱 Pares de divisas disponibles:")
    for i, symbol in enumerate(symbols, 1):
        print(f"  {i}. {symbol}")
    
    while True:
        try:
            choice = input("\n🎯 Selecciona par (1-7) o presiona Enter para EURUSD: ").strip()
            if not choice:
                symbol = 'EURUSD'
                break
            choice = int(choice)
            if 1 <= choice <= len(symbols):
                symbol = symbols[choice - 1]
                break
            print("❌ Opción inválida")
        except ValueError:
            print("❌ Por favor ingresa un número")
    
    # Timeframe
    timeframes = ['M1', 'M5', 'M15', 'M30', 'H1', 'H4']
    print(f"\n⏱️  Timeframes disponibles: {', '.join(timeframes)}")
    while True:
        timeframe = input("🕐 Selecciona timeframe (o presiona Enter para M5): ").strip().upper()
        if not timeframe:
            timeframe = 'M5'
            break
        if timeframe in timeframes:
            break
        print("❌ Timeframe inválido")
    
    # Riesgo
    while True:
        try:
            risk = input("💰 Riesgo por operación % (o presiona Enter para 1%): ").strip()
            if not risk:
                risk = 1.0
                break
            risk = float(risk)
            if 0.1 <= risk <= 5.0:
                break
            print("❌ Riesgo debe estar entre 0.1% y 5%")
        except ValueError:
            print("❌ Por favor ingresa un número válido")
    
    return symbol, timeframe, risk

def main():
    """Función principal"""
    try:
        print_banner()
        
        print("\n🚀 Iniciando bot SMC-LIT con configuración por defecto...")
        print("📊 Par: EURUSD")
        print("⏱️  Timeframe: M5") 
        print("💰 Riesgo: 1%")
        print("\n⚠️  Presiona Ctrl+C para detener")
        time.sleep(2)
        
        # Ejecutar bot directamente
        cmd = [sys.executable, 'main.py', 'trade', '--symbol', 'EURUSD', '--timeframe', 'M5', '--risk', '1.0']
        subprocess.run(cmd)
            
    except KeyboardInterrupt:
        print("\n\n👋 Bot detenido por el usuario")
        print("💾 Logs guardados en archivos .log")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
    finally:
        print("\n🏁 Ejecución terminada")

if __name__ == "__main__":
    main() 