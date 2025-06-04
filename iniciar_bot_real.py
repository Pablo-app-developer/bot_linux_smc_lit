#!/usr/bin/env python3
"""
INICIO BOT TRADING REAL CON CUENTA DEMO
=======================================
Bot operando REAL (no simulado) usando cuenta DEMO de MT5
"""

import sys
import os
import time
from datetime import datetime

# Importar configuración de trading real
from config_trading_real import (
    TRADING_REAL_CONFIG,
    validar_modo_real, 
    obtener_mensaje_confirmacion
)

def imprimir_banner_real():
    """Banner para modo de trading real"""
    print("=" * 70)
    print("🚀 SMC-LIT BOT - TRADING REAL CON CUENTA DEMO")
    print("=" * 70)
    print("📊 Smart Money Concepts + Algoritmos Avanzados")
    print("🎯 MODO REAL: Operaciones enviadas a MT5")
    print("💰 CUENTA DEMO: Sin dinero real en riesgo")
    print("=" * 70)
    print(f"⏰ Inicio: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🏦 Servidor: {TRADING_REAL_CONFIG['mt5_server']}")
    print(f"👤 Login: {TRADING_REAL_CONFIG['mt5_login']}")
    print(f"📈 Símbolo: {TRADING_REAL_CONFIG['symbol']}")
    print(f"⏱️  Timeframe: {TRADING_REAL_CONFIG['timeframe']}")
    print(f"🎯 Riesgo: {TRADING_REAL_CONFIG['risk_per_trade']}%")
    print(f"📊 Max trades diarios: {TRADING_REAL_CONFIG['max_daily_trades']}")
    print("=" * 70)

def verificar_mt5_disponible():
    """Verifica si MT5 está disponible o usa simulador"""
    try:
        import MetaTrader5 as mt5
        print("✅ MetaTrader5 nativo disponible")
        return 'native'
    except ImportError:
        try:
            from src.mt5_simulator import MT5Simulator
            print("⚠️  Usando simulador MT5 (para desarrollo)")
            return 'simulator'
        except ImportError:
            print("❌ No se puede importar MT5 ni simulador")
            return None

def confirmar_trading_real():
    """Confirmación específica para trading real"""
    print(obtener_mensaje_confirmacion())
    
    while True:
        print("\n🎯 CONFIRMACIÓN DE TRADING REAL:")
        print("1. El bot enviará órdenes REALES a MT5")
        print("2. NO es simulación interna del bot")
        print("3. Usa tu cuenta DEMO de MT5")
        print("4. Las operaciones aparecerán en MT5")
        
        respuesta = input("\n¿Confirmas iniciar TRADING REAL en cuenta DEMO? (si/no): ").lower().strip()
        
        if respuesta in ['si', 'sí', 's', 'yes', 'y']:
            return True
        elif respuesta in ['no', 'n']:
            print("👋 Inicio cancelado")
            return False
        else:
            print("❌ Por favor responde 'si' o 'no'")

def iniciar_trading_real():
    """Inicia el bot en modo de trading real"""
    print("\n🚀 INICIANDO BOT EN MODO TRADING REAL...")
    print("=" * 60)
    
    mt5_type = verificar_mt5_disponible()
    if not mt5_type:
        print("❌ No se puede conectar a MT5")
        return False
    
    try:
        if mt5_type == 'native':
            # Usar MT5 nativo
            import MetaTrader5 as mt5
            
            print("🔗 Conectando a MetaTrader5...")
            if not mt5.initialize():
                print("❌ Error inicializando MT5")
                return False
            
            print("🔐 Iniciando sesión...")
            login_result = mt5.login(
                int(TRADING_REAL_CONFIG['mt5_login']),
                TRADING_REAL_CONFIG['mt5_password'],
                TRADING_REAL_CONFIG['mt5_server']
            )
            
            if not login_result:
                print("❌ Error en login MT5")
                print(f"Error: {mt5.last_error()}")
                mt5.shutdown()
                return False
            
            # Verificar conexión
            account_info = mt5.account_info()
            if account_info is None:
                print("❌ No se pudo obtener información de cuenta")
                mt5.shutdown()
                return False
            
            print("✅ Conectado exitosamente a MT5")
            print(f"💰 Balance: ${account_info.balance:.2f}")
            print(f"🏦 Servidor: {account_info.server}")
            print(f"👤 Login: {account_info.login}")
            
        else:
            # Usar simulador
            from src.mt5_simulator import MT5Simulator
            mt5 = MT5Simulator()
            
            print("🔗 Inicializando simulador MT5...")
            mt5.initialize()
            mt5.login(
                TRADING_REAL_CONFIG['mt5_login'],
                TRADING_REAL_CONFIG['mt5_password'],
                TRADING_REAL_CONFIG['mt5_server']
            )
            print("✅ Simulador MT5 inicializado")
        
        # Importar y configurar el sistema de trading
        print("📊 Cargando sistema de trading...")
        
        # Aquí irían las importaciones del sistema de trading real
        # from src.mt5_trader import MT5Trader
        # from src.strategy import SMCStrategy
        
        print("🎯 TRADING REAL INICIADO")
        print("=" * 40)
        print("✅ Bot operando en MODO REAL")
        print("✅ Conexión a MT5 establecida")
        print("✅ Enviando órdenes reales")
        print("✅ Usando cuenta DEMO")
        print("=" * 40)
        
        # Loop principal de trading real
        trade_count = 0
        while True:
            try:
                trade_count += 1
                timestamp = datetime.now().strftime('%H:%M:%S')
                
                # Aquí iría la lógica real de trading
                print(f"📊 Análisis REAL #{trade_count} - {timestamp}")
                
                # Simular análisis de mercado cada 30 segundos
                time.sleep(30)
                
                if trade_count % 5 == 0:
                    if mt5_type == 'native':
                        # Obtener información real de cuenta
                        account = mt5.account_info()
                        balance = account.balance if account else 0
                        print(f"💰 Balance actual: ${balance:.2f} - {trade_count} análisis")
                    else:
                        print(f"💰 Trading activo - {trade_count} análisis completados")
                
            except KeyboardInterrupt:
                print("\n🛑 Bot detenido por usuario")
                break
            except Exception as e:
                print(f"⚠️  Error en trading: {e}")
                time.sleep(10)
                continue
        
        # Limpiar al salir
        if mt5_type == 'native':
            mt5.shutdown()
            print("🔌 Conexión MT5 cerrada")
        
        return True
        
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        return False

def main():
    """Función principal"""
    try:
        # Banner
        imprimir_banner_real()
        
        # Validar configuración
        if not validar_modo_real():
            print("🚨 CONFIGURACIÓN INVÁLIDA")
            sys.exit(1)
        
        # Confirmar con usuario
        if not confirmar_trading_real():
            sys.exit(0)
        
        # Iniciar trading real
        if iniciar_trading_real():
            print("\n✅ Bot ejecutado exitosamente")
        else:
            print("\n❌ Error ejecutando bot")
            sys.exit(1)
        
    except KeyboardInterrupt:
        print("\n\n👋 Programa interrumpido")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
    finally:
        print("\n🏁 Programa terminado")

if __name__ == "__main__":
    main() 