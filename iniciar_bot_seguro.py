#!/usr/bin/env python3
"""
INICIO SEGURO SMC-LIT BOT
========================
Script de inicio con todas las protecciones de seguridad activadas
SOLO FUNCIONA EN MODO DEMO - NO USA DINERO REAL
"""

import sys
import os
import time
import json
from datetime import datetime
import subprocess

# Importar configuración segura
from config_seguro import (
    CONFIGURACION_SEGURA, 
    PARAMETROS_OPTIMIZADOS,
    validar_configuracion_segura,
    obtener_mensaje_seguridad
)

def imprimir_banner():
    """Imprime el banner del bot con información de seguridad"""
    print("=" * 70)
    print("🤖 SMC-LIT ALGORITHMIC TRADING BOT - MODO SEGURO")
    print("=" * 70)
    print("📊 Smart Money Concepts + Liquidity Inducement Theorem")
    print("🧠 IA Avanzada: XGBoost + Reinforcement Learning")
    print("🛡️  MODO DEMO ACTIVADO - SIN RIESGO DE DINERO REAL")
    print("=" * 70)
    print(f"⏰ Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("💰 Capital Virtual: ${:,.2f} USD".format(CONFIGURACION_SEGURA['CAPITAL_INICIAL']))
    print("📈 Símbolo: {}".format(CONFIGURACION_SEGURA['SIMBOLO_PRINCIPAL']))
    print("⏱️  Timeframe: {}".format(CONFIGURACION_SEGURA['TIMEFRAME_PRINCIPAL']))
    print("🎯 Riesgo por trade: {}%".format(CONFIGURACION_SEGURA['RIESGO_MAXIMO_POR_TRADE']))
    print("=" * 70)

def verificar_dependencias():
    """Verifica que todas las dependencias estén instaladas"""
    print("🔍 Verificando dependencias...")
    
    required_packages = [
        'pandas', 'numpy', 'sklearn', 'xgboost',
        'matplotlib', 'yfinance', 'ccxt'
    ]
    
    faltantes = []
    for dep in required_packages:
        try:
            __import__(dep)
        except ImportError:
            faltantes.append(dep)
    
    if faltantes:
        print(f"❌ Dependencias faltantes: {', '.join(faltantes)}")
        print("💡 Ejecuta: pip install -r requirements.txt")
        return False
    
    print("✅ Todas las dependencias están instaladas")
    return True

def verificar_archivos():
    """Verifica que todos los archivos necesarios existan"""
    print("📁 Verificando archivos del sistema...")
    
    archivos_necesarios = [
        'main.py',
        'src/mt5_connector.py',
        'src/mt5_simulator.py',
        'src/mt5_trader.py',
        'src/strategy.py',
        'src/features.py',
        'config_seguro.py'
    ]
    
    faltantes = []
    for archivo in archivos_necesarios:
        if not os.path.exists(archivo):
            faltantes.append(archivo)
    
    if faltantes:
        print(f"❌ Archivos faltantes: {', '.join(faltantes)}")
        return False
    
    print("✅ Todos los archivos necesarios están presentes")
    return True

def verificar_mercado_abierto():
    """Verifica si el mercado forex está abierto"""
    from datetime import datetime, timezone
    
    ahora = datetime.now(timezone.utc)
    dia_semana = ahora.weekday()  # 0=Lunes, 6=Domingo
    hora = ahora.hour
    
    # Forex está cerrado los fines de semana
    if dia_semana >= 5:  # Sábado o Domingo
        print("⚠️  Mercado Forex cerrado (fin de semana)")
        return False
    
    # Forex está cerrado los viernes tarde hasta domingo noche
    if dia_semana == 4 and hora >= 22:  # Viernes tarde
        print("⚠️  Mercado Forex cerrado (cierre semanal)")
        return False
    
    print("✅ Mercado Forex está abierto")
    return True

def mostrar_parametros_optimizados():
    """Muestra los parámetros optimizados que se usarán"""
    print("\n🎯 PARÁMETROS OPTIMIZADOS CARGADOS:")
    print("-" * 50)
    for key, value in PARAMETROS_OPTIMIZADOS.items():
        if isinstance(value, float):
            print(f"• {key}: {value:.4f}")
        else:
            print(f"• {key}: {value}")

def ejecutar_backtest_seguridad():
    """Ejecuta un backtest rápido para verificar que todo funciona"""
    print("\n🧪 Ejecutando backtest de seguridad...")
    
    try:
        # Ejecutar backtest rápido
        cmd = [sys.executable, 'quick_backtest.py']
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Backtest de seguridad completado exitosamente")
            return True
        else:
            print(f"❌ Error en backtest: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("⏰ Backtest de seguridad tardó demasiado")
        return False
    except Exception as e:
        print(f"❌ Error ejecutando backtest: {e}")
        return False

def confirmar_inicio_usuario():
    """Pide confirmación al usuario antes de iniciar"""
    print("\n" + obtener_mensaje_seguridad())
    
    while True:
        respuesta = input("\n¿Deseas iniciar el bot en MODO DEMO? (si/no): ").lower().strip()
        
        if respuesta in ['si', 'sí', 's', 'yes', 'y']:
            return True
        elif respuesta in ['no', 'n']:
            print("👋 Inicio cancelado por el usuario")
            return False
        else:
            print("❌ Por favor responde 'si' o 'no'")

def iniciar_bot():
    """Inicia el bot con configuración segura"""
    print("\n🚀 INICIANDO BOT SMC-LIT EN MODO SEGURO...")
    print("=" * 50)
    
    # Crear archivo de configuración temporal
    config_temp = {
        'symbol': CONFIGURACION_SEGURA['SIMBOLO_PRINCIPAL'],
        'timeframe': CONFIGURACION_SEGURA['TIMEFRAME_PRINCIPAL'],
        'risk': CONFIGURACION_SEGURA['RIESGO_MAXIMO_POR_TRADE'],
        'demo_mode': True,
        'paper_trading': True,
        'max_trades': CONFIGURACION_SEGURA['MAX_TRADES_POR_DIA'],
        'parameters': PARAMETROS_OPTIMIZADOS
    }
    
    # Guardar configuración
    with open('config_temp.json', 'w') as f:
        json.dump(config_temp, f, indent=2)
    
    try:
        # Ejecutar el bot principal
        cmd = [
            sys.executable, 'main.py', 'trade',
            '--symbol', CONFIGURACION_SEGURA['SIMBOLO_PRINCIPAL'],
            '--timeframe', CONFIGURACION_SEGURA['TIMEFRAME_PRINCIPAL'],
            '--risk', str(CONFIGURACION_SEGURA['RIESGO_MAXIMO_POR_TRADE']),
            '--max-trades', str(CONFIGURACION_SEGURA['MAX_TRADES_POR_DIA']),
            '--demo'
        ]
        
        print(f"🎯 Comando: {' '.join(cmd)}")
        print("\n📊 MONITOREANDO TRADES EN VIVO...")
        print("⚠️  Presiona Ctrl+C para detener el bot")
        print("=" * 50)
        
        # Ejecutar bot
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n\n🛑 Bot detenido por el usuario")
    except Exception as e:
        print(f"\n❌ Error ejecutando bot: {e}")
    finally:
        print("\n📊 RESUMEN DE SESIÓN:")
        print("-" * 30)
        print(f"⏰ Sesión terminada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        
        # Limpiar archivos temporales
        if os.path.exists('config_temp.json'):
            os.remove('config_temp.json')

def main():
    """Función principal del script"""
    try:
        # Banner inicial
        imprimir_banner()
        
        # Validaciones de seguridad
        if not validar_configuracion_segura():
            print("🚨 FALLO EN VALIDACIÓN DE SEGURIDAD - ABORTANDO")
            sys.exit(1)
        
        # Verificaciones del sistema
        if not verificar_dependencias():
            sys.exit(1)
        
        if not verificar_archivos():
            sys.exit(1)
        
        # Mostrar parámetros
        mostrar_parametros_optimizados()
        
        # Verificar mercado (opcional - para información)
        mercado_abierto = verificar_mercado_abierto()
        if not mercado_abierto:
            print("ℹ️  Nota: El bot puede ejecutarse en modo demo aunque el mercado esté cerrado")
        
        # Backtest de seguridad (opcional)
        print("\n🧪 ¿Ejecutar backtest de seguridad? (recomendado)")
        respuesta = input("Respuesta (si/no): ").lower().strip()
        if respuesta in ['si', 'sí', 's', 'yes', 'y']:
            if not ejecutar_backtest_seguridad():
                print("⚠️  Backtest falló pero se puede continuar en modo demo")
        
        # Confirmación final
        if confirmar_inicio_usuario():
            iniciar_bot()
        
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        print("📝 Revisa los logs para más detalles")
    finally:
        print("\n🏁 Programa terminado")

if __name__ == "__main__":
    main() 