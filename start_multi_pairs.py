#!/usr/bin/env python3
"""
START MULTI-PAIRS BOT - Ejecuta el bot SMC-LIT con múltiples pares de divisas
"""

import sys
import subprocess
import time
import threading
from datetime import datetime

# Pares de divisas principales (por orden de liquidez)
MAJOR_PAIRS = [
    'EURUSD',  # Euro/USD - El más líquido
    'GBPUSD',  # Libra/USD - Muy volátil
    'USDJPY',  # USD/Yen - Mercado asiático
    'AUDUSD',  # Dólar Australiano/USD
    'USDCAD',  # USD/Dólar Canadiense
    'NZDUSD',  # Dólar Neozelandés/USD
    'USDCHF'   # USD/Franco Suizo
]

def print_banner():
    """Banner del bot multi-pares"""
    print("=" * 70)
    print("🚀 SMC-LIT MULTI-PAIRS ALGORITHMIC TRADING BOT")
    print("=" * 70)
    print("📊 Smart Money Concepts + Liquidity Inducement Theorem")
    print("🤖 AI/ML Powered - XGBoost & Reinforcement Learning")
    print("💹 Multi-Currency Forex Trading - 7 Major Pairs")
    print("=" * 70)
    print(f"⏰ Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

def run_pair_bot(symbol, timeframe='M5', risk=1.0):
    """Ejecuta bot para un par específico"""
    try:
        print(f"\n🔄 Iniciando {symbol} en {timeframe}...")
        cmd = [
            sys.executable, 'main.py', 'trade',
            '--symbol', symbol,
            '--timeframe', timeframe,
            '--risk', str(risk)
        ]
        subprocess.run(cmd)
    except Exception as e:
        print(f"❌ Error en {symbol}: {e}")

def main():
    """Función principal"""
    try:
        print_banner()
        
        print("\n🎮 Modos de ejecución multi-pares:")
        print("  1. 🎯 Un solo par (interactivo)")
        print("  2. 🔥 Top 3 pares (EUR/USD, GBP/USD, USD/JPY)")
        print("  3. 🌟 Todos los pares principales (7 pares)")
        print("  4. ⚡ Par personalizado")
        
        choice = input("\n🚀 Selecciona modo (1-4): ").strip()
        
        if choice == '1':
            # Un solo par
            print("\n💱 Pares disponibles:")
            for i, pair in enumerate(MAJOR_PAIRS, 1):
                print(f"  {i}. {pair}")
            
            pair_choice = input("\n🎯 Selecciona par (1-7): ").strip()
            try:
                symbol = MAJOR_PAIRS[int(pair_choice) - 1]
                print(f"\n🚀 Ejecutando {symbol}...")
                time.sleep(1)
                run_pair_bot(symbol)
            except (ValueError, IndexError):
                print("❌ Selección inválida")
                
        elif choice == '2':
            # Top 3 pares
            top_pairs = MAJOR_PAIRS[:3]
            print(f"\n🔥 Ejecutando Top 3: {', '.join(top_pairs)}")
            print("⚠️  Se ejecutarán secuencialmente...")
            time.sleep(2)
            
            for symbol in top_pairs:
                print(f"\n📊 === {symbol} ===")
                run_pair_bot(symbol)
                time.sleep(5)  # Pausa entre pares
                
        elif choice == '3':
            # Todos los pares
            print(f"\n🌟 Ejecutando todos los pares: {', '.join(MAJOR_PAIRS)}")
            print("⚠️  Se ejecutarán secuencialmente...")
            print("⏱️  Cada par correrá por 2 minutos")
            time.sleep(2)
            
            for symbol in MAJOR_PAIRS:
                print(f"\n📊 === {symbol} ===")
                # Ejecutar cada par por tiempo limitado
                process = subprocess.Popen([
                    sys.executable, 'main.py', 'trade',
                    '--symbol', symbol,
                    '--timeframe', 'M5',
                    '--risk', '1.0'
                ])
                time.sleep(120)  # 2 minutos por par
                process.terminate()
                
        elif choice == '4':
            # Par personalizado
            symbol = input("💱 Ingresa el par (ej: EURUSD): ").strip().upper()
            timeframe = input("⏱️  Timeframe (M1/M5/M15/M30/H1/H4) [M5]: ").strip().upper() or 'M5'
            risk = input("💰 Riesgo % [1.0]: ").strip() or '1.0'
            
            print(f"\n🚀 Ejecutando {symbol} en {timeframe} con {risk}% riesgo...")
            time.sleep(1)
            run_pair_bot(symbol, timeframe, float(risk))
            
        else:
            print("❌ Opción inválida")
            
    except KeyboardInterrupt:
        print("\n\n👋 Bot multi-pares detenido por el usuario")
        print("💾 Logs guardados para cada par en archivos .log")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
    finally:
        print("\n🏁 Ejecución multi-pares terminada")

if __name__ == "__main__":
    main() 