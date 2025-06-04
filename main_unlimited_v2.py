#!/usr/bin/env python3
'''
BOT SMC-LIT - VERSIÓN 2.0 CON CONFIGURACIÓN DINÁMICA
===================================================
Bot que carga configuración desde archivo JSON y opera según parámetros
'''

import sys
import json
import time
import signal
import os
from datetime import datetime

def cargar_configuracion():
    """Cargar configuración desde archivo JSON"""
    config_files = ['config_bot_activo.json', 'config_trading_real.json']
    
    for config_file in config_files:
        if os.path.exists(config_file):
            try:
                with open(config_file, 'r') as f:
                    config = json.load(f)
                print(f"✅ Configuración cargada desde: {config_file}")
                return config
            except Exception as e:
                print(f"⚠️  Error cargando {config_file}: {e}")
                continue
    
    # Configuración por defecto si no hay archivo
    print("⚠️  Usando configuración por defecto")
    return {
        'symbol': 'EURUSD',
        'timeframe': 'M5',
        'risk_per_trade': 2.0,
        'max_daily_trades': 50,
        'mode': 'aggressive',
        'demo_mode': True,
        'aggressive': True,
        'scalping': False,
        'high_frequency': True,
        'stop_loss_pips': 20,
        'take_profit_pips': 40,
        'trailing_stop': True,
        'max_drawdown': 10.0,
        'bos_threshold': 0.0003,
        'choch_threshold': 0.0005,
        'liquidity_threshold': 0.0004,
        'rsi_oversold': 30,
        'rsi_overbought': 70,
        'mt5_login': '164675960',
        'mt5_server': 'MetaQuotes-Demo',
        'mt5_password': 'Chevex9292!'
    }

def mostrar_configuracion(config):
    """Mostrar configuración cargada"""
    print("\n📊 CONFIGURACIÓN ACTIVA:")
    print("=" * 40)
    print(f"📈 Símbolo: {config['symbol']}")
    print(f"⏱️  Timeframe: {config['timeframe']}")
    print(f"💰 Riesgo por trade: {config['risk_per_trade']}%")
    print(f"📊 Max trades diarios: {config['max_daily_trades']}")
    print(f"🎯 Modo: {config['mode'].upper()}")
    print(f"💳 Cuenta: {'DEMO' if config['demo_mode'] else 'REAL'}")
    print(f"⚡ Agresivo: {'Sí' if config['aggressive'] else 'No'}")
    print(f"🎯 Scalping: {'Sí' if config['scalping'] else 'No'}")
    print(f"🚀 Alta frecuencia: {'Sí' if config['high_frequency'] else 'No'}")
    print("=" * 40)

def signal_handler(sig, frame):
    print('\n🛑 Bot detenido por señal del sistema')
    # Guardar estado antes de salir
    with open('bot_status.json', 'w') as f:
        json.dump({
            'stopped_at': datetime.now().isoformat(),
            'reason': 'system_signal'
        }, f)
    sys.exit(0)

def inicializar_mt5_connection(config):
    """Inicializar conexión MT5 según configuración"""
    try:
        # Intentar MT5 nativo primero
        import MetaTrader5 as mt5
        
        print("🔗 Inicializando MetaTrader5...")
        if not mt5.initialize():
            raise ImportError("MT5 no disponible")
        
        print("🔐 Conectando a cuenta...")
        login_result = mt5.login(
            int(config['mt5_login']),
            config['mt5_password'],
            config['mt5_server']
        )
        
        if not login_result:
            print(f"❌ Error en login: {mt5.last_error()}")
            mt5.shutdown()
            raise ConnectionError("No se pudo conectar a MT5")
        
        account_info = mt5.account_info()
        if account_info is None:
            raise ConnectionError("No se pudo obtener info de cuenta")
        
        print("✅ Conectado a MT5 exitosamente")
        print(f"💰 Balance: ${account_info.balance:.2f}")
        print(f"🏦 Servidor: {account_info.server}")
        
        return mt5, 'native'
        
    except (ImportError, ConnectionError):
        print("⚠️  MT5 nativo no disponible, usando simulador...")
        try:
            from src.mt5_simulator import MT5Simulator
            mt5_sim = MT5Simulator()
            mt5_sim.initialize()
            mt5_sim.login(
                config['mt5_login'],
                config['mt5_password'],
                config['mt5_server']
            )
            print("✅ Simulador MT5 inicializado")
            return mt5_sim, 'simulator'
        except ImportError:
            print("❌ No se pudo inicializar ningún sistema MT5")
            return None, None

def ejecutar_analisis_trading(config, mt5, mt5_type, analysis_count):
    """Ejecutar análisis de trading según configuración"""
    timestamp = datetime.now().strftime('%H:%M:%S')
    
    # Obtener datos de mercado
    if mt5_type == 'native':
        # Usar MT5 real para obtener datos
        symbol_info = mt5.symbol_info(config['symbol'])
        if symbol_info:
            bid_price = symbol_info.bid
            ask_price = symbol_info.ask
            spread = ask_price - bid_price
        else:
            bid_price = ask_price = spread = 0
    else:
        # Usar simulador
        tick = mt5.symbol_info_tick(config['symbol'])
        if tick:
            bid_price = tick.bid
            ask_price = tick.ask
            spread = ask_price - bid_price
        else:
            bid_price = ask_price = spread = 0
    
    # Mostrar análisis
    if config['high_frequency']:
        print(f"📊 Análisis #{analysis_count} - {timestamp} | {config['symbol']} | Bid: {bid_price:.5f} | Ask: {ask_price:.5f}")
    else:
        print(f"📊 Análisis #{analysis_count} - {timestamp} | {config['symbol']}")
    
    # Simular lógica de trading según modo
    if config['mode'] == 'scalping' and analysis_count % 3 == 0:
        print(f"⚡ Oportunidad de scalping detectada - Análisis #{analysis_count}")
    elif config['aggressive'] and analysis_count % 7 == 0:
        print(f"🎯 Señal agresiva detectada - Análisis #{analysis_count}")
    elif analysis_count % 10 == 0:
        print(f"💹 Evaluación de mercado - {analysis_count} análisis completados")
    
    return True

def main():
    """Función principal mejorada"""
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    print("🚀 INICIANDO BOT SMC-LIT - VERSIÓN 2.0")
    print("=" * 60)
    
    # Cargar configuración
    config = cargar_configuracion()
    mostrar_configuracion(config)
    
    # Inicializar MT5
    mt5, mt5_type = inicializar_mt5_connection(config)
    if not mt5:
        print("❌ No se pudo inicializar sistema de trading")
        return
    
    # Inicializar sistema de trading
    print("\n📊 INICIANDO SISTEMA DE TRADING...")
    print("=" * 45)
    
    # Determinar intervalos según configuración
    if config['scalping']:
        interval = 5  # 5 segundos para scalping
    elif config['high_frequency']:
        interval = 15  # 15 segundos para alta frecuencia
    elif config['aggressive']:
        interval = 30  # 30 segundos para modo agresivo
    else:
        interval = 60  # 1 minuto para modo conservador
    
    print(f"⏱️  Intervalo de análisis: {interval} segundos")
    print(f"🎯 Modo activo: {config['mode'].upper()}")
    print("🔄 Presiona Ctrl+C para detener")
    print("=" * 45)
    
    # Loop principal de trading
    analysis_count = 0
    start_time = datetime.now()
    
    try:
        while True:
            analysis_count += 1
            
            # Ejecutar análisis
            success = ejecutar_analisis_trading(config, mt5, mt5_type, analysis_count)
            
            if not success:
                print("⚠️  Error en análisis, continuando...")
            
            # Estadísticas periódicas
            if analysis_count % 20 == 0:
                elapsed = datetime.now() - start_time
                print(f"📈 ESTADÍSTICAS: {analysis_count} análisis | Tiempo activo: {elapsed}")
            
            # Verificar límites diarios
            if analysis_count >= config['max_daily_trades'] * 10:  # Factor de seguridad
                print(f"🛑 Límite de análisis diario alcanzado: {analysis_count}")
                break
            
            # Esperar según configuración
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n🛑 Bot detenido por usuario")
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
    finally:
        # Limpiar conexiones
        if mt5_type == 'native':
            mt5.shutdown()
            print("🔌 Conexión MT5 cerrada")
        
        # Guardar estadísticas finales
        end_time = datetime.now()
        session_data = {
            'start_time': start_time.isoformat(),
            'end_time': end_time.isoformat(),
            'total_analysis': analysis_count,
            'config_used': config,
            'mt5_type': mt5_type
        }
        
        with open('session_stats.json', 'w') as f:
            json.dump(session_data, f, indent=2)
        
        print(f"📊 Sesión completada: {analysis_count} análisis en {end_time - start_time}")
        print("💾 Estadísticas guardadas en session_stats.json")

if __name__ == "__main__":
    main() 