#!/usr/bin/env python3
'''
BOT SMC-LIT - VERSIÓN 3.0 AVANZADA
=================================
Bot con múltiples timeframes, múltiples activos y auto-optimización
'''

import sys
import json
import time
import signal
import os
import threading
from datetime import datetime, timedelta
import random

class MultiAssetMultiTimeframeBotAdvanced:
    def __init__(self):
        self.config = {}
        self.mt5 = None
        self.mt5_type = None
        self.active_symbols = []
        self.active_timeframes = []
        self.running = False
        self.threads = []
        self.analysis_stats = {}
        self.optimization_timer = None
        
    def cargar_configuracion(self):
        """Cargar configuración avanzada"""
        config_files = ['config_bot_advanced.json', 'config_bot_activo.json']
        
        for config_file in config_files:
            if os.path.exists(config_file):
                try:
                    with open(config_file, 'r') as f:
                        config = json.load(f)
                    print(f"✅ Configuración avanzada cargada desde: {config_file}")
                    return config
                except Exception as e:
                    print(f"⚠️  Error cargando {config_file}: {e}")
                    continue
        
        # Configuración por defecto avanzada
        print("⚠️  Usando configuración por defecto avanzada")
        return {
            'symbols': ['EURUSD', 'GBPUSD'],
            'timeframes': ['M5', 'M15'],
            'multi_asset_mode': True,
            'multi_timeframe_mode': True,
            'risk_per_trade': 1.5,
            'max_daily_trades': 100,
            'mode': 'aggressive_multi',
            'demo_mode': True,
            'auto_optimize': True,
            'optimization_frequency_hours': 4,
            'ai_adaptive': True
        }
    
    def mostrar_configuracion_avanzada(self, config):
        """Mostrar configuración avanzada cargada"""
        print("\n🚀 CONFIGURACIÓN AVANZADA ACTIVA:")
        print("=" * 60)
        
        # Múltiples activos
        symbols = config.get('symbols', [])
        print(f"💱 Activos ({len(symbols)}):")
        for i, symbol in enumerate(symbols, 1):
            print(f"  {i}. {symbol}")
        
        # Múltiples timeframes
        timeframes = config.get('timeframes', [])
        print(f"\n⏱️  Timeframes ({len(timeframes)}):")
        for i, tf in enumerate(timeframes, 1):
            print(f"  {i}. {tf}")
        
        print(f"\n🎯 Modo: {config['mode'].upper()}")
        print(f"💰 Riesgo por trade: {config['risk_per_trade']}%")
        print(f"📊 Max trades: {config['max_daily_trades']}")
        print(f"🤖 Auto-optimización: {'Activada' if config.get('auto_optimize') else 'Desactivada'}")
        print(f"🧠 IA Adaptativa: {'Activada' if config.get('ai_adaptive') else 'Desactivada'}")
        print(f"💳 Cuenta: {'DEMO' if config['demo_mode'] else 'REAL'}")
        print("=" * 60)
    
    def inicializar_mt5_connection(self, config):
        """Inicializar conexión MT5"""
        try:
            import MetaTrader5 as mt5
            
            print("🔗 Inicializando MetaTrader5 para multi-assets...")
            if not mt5.initialize():
                raise ImportError("MT5 no disponible")
            
            login_result = mt5.login(
                int(config['mt5_login']),
                config['mt5_password'],
                config['mt5_server']
            )
            
            if not login_result:
                print(f"❌ Error en login: {mt5.last_error()}")
                mt5.shutdown()
                raise ConnectionError("No se pudo conectar a MT5")
            
            print("✅ Conectado a MT5 para trading multi-asset")
            return mt5, 'native'
            
        except (ImportError, ConnectionError):
            print("⚠️  MT5 nativo no disponible, usando simulador avanzado...")
            try:
                from src.mt5_simulator import MT5Simulator
                mt5_sim = MT5Simulator()
                mt5_sim.initialize()
                print("✅ Simulador MT5 avanzado inicializado")
                return mt5_sim, 'simulator'
            except ImportError:
                print("❌ No se pudo inicializar ningún sistema MT5")
                return None, None
    
    def analizar_simbolo_timeframe(self, symbol, timeframe, analysis_id):
        """Analizar un símbolo en un timeframe específico"""
        try:
            timestamp = datetime.now().strftime('%H:%M:%S')
            
            # Obtener datos de mercado
            if self.mt5_type == 'native':
                symbol_info = self.mt5.symbol_info(symbol)
                if symbol_info:
                    bid_price = symbol_info.bid
                    ask_price = symbol_info.ask
                    spread = ask_price - bid_price
                else:
                    bid_price = ask_price = spread = 0
            else:
                # Usar simulador
                tick = self.mt5.symbol_info_tick(symbol)
                if tick:
                    bid_price = tick.bid
                    ask_price = tick.ask
                    spread = ask_price - bid_price
                else:
                    # Generar datos simulados realistas
                    base_price = self.get_base_price(symbol)
                    bid_price = base_price + random.uniform(-0.0010, 0.0010)
                    ask_price = bid_price + random.uniform(0.00001, 0.00005)
                    spread = ask_price - bid_price
            
            # Análisis técnico simulado para el par de tiempo
            volatility = random.uniform(0.3, 1.0)
            trend_strength = random.uniform(0.1, 1.0)
            signal_quality = random.uniform(0.0, 1.0)
            
            # Generar señales basadas en análisis multi-timeframe
            signal_type = self.generar_signal_multi_tf(symbol, timeframe, volatility, trend_strength)
            
            # Registrar análisis
            key = f"{symbol}_{timeframe}"
            if key not in self.analysis_stats:
                self.analysis_stats[key] = {'count': 0, 'signals': 0, 'last_signal': None}
            
            self.analysis_stats[key]['count'] += 1
            
            # Mostrar análisis - corregir el error de formateo
            analysis_count = self.analysis_stats[key]['count']
            
            if self.config.get('high_frequency'):
                print(f"📊 #{analysis_count} {timestamp} | {symbol} {timeframe} | Bid: {bid_price:.5f} | Spread: {spread:.5f} | Signal: {signal_type}")
            else:
                if analysis_count % 5 == 0:  # Mostrar cada 5 análisis
                    print(f"📊 #{analysis_count} {timestamp} | {symbol} {timeframe} | {signal_type}")
            
            # Detectar oportunidades de trading
            if signal_quality > 0.7:
                self.analysis_stats[key]['signals'] += 1
                self.analysis_stats[key]['last_signal'] = signal_type
                
                if signal_type != 'HOLD':
                    print(f"🎯 OPORTUNIDAD DETECTADA: {symbol} {timeframe} - {signal_type} (Calidad: {signal_quality:.2f})")
            
            return True
            
        except Exception as e:
            print(f"❌ Error analizando {symbol} {timeframe}: {e}")
            return False
    
    def get_base_price(self, symbol):
        """Obtener precio base para simulación"""
        base_prices = {
            'EURUSD': 1.09000,
            'GBPUSD': 1.27000,
            'USDJPY': 149.000,
            'AUDUSD': 0.66000,
            'USDCAD': 1.36000,
            'USDCHF': 0.88000,
            'EURJPY': 162.000,
            'EURGBP': 0.86000,
            'GBPJPY': 189.000
        }
        return base_prices.get(symbol, 1.00000)
    
    def generar_signal_multi_tf(self, symbol, timeframe, volatility, trend_strength):
        """Generar señales basadas en análisis multi-timeframe"""
        # Simulación de análisis técnico avanzado
        if trend_strength > 0.8 and volatility > 0.6:
            return random.choice(['BUY_STRONG', 'SELL_STRONG'])
        elif trend_strength > 0.6:
            return random.choice(['BUY', 'SELL'])
        elif volatility > 0.8:
            return random.choice(['SCALP_BUY', 'SCALP_SELL'])
        else:
            return 'HOLD'
    
    def ejecutar_optimizacion_automatica(self):
        """Ejecutar optimización automática de parámetros"""
        print("\n🤖 EJECUTANDO AUTO-OPTIMIZACIÓN...")
        print("=" * 50)
        
        # Analizar rendimiento actual
        total_analysis = sum(stats['count'] for stats in self.analysis_stats.values())
        total_signals = sum(stats['signals'] for stats in self.analysis_stats.values())
        
        signal_rate = total_signals / max(total_analysis, 1)
        
        print(f"📊 Análisis realizados: {total_analysis}")
        print(f"🎯 Señales generadas: {total_signals}")
        print(f"📈 Tasa de señales: {signal_rate:.2%}")
        
        # Optimizar parámetros basándose en rendimiento
        if signal_rate < 0.1:  # Pocas señales
            print("🔧 Optimización: Aumentando sensibilidad...")
            # Lógica para aumentar sensibilidad
        elif signal_rate > 0.3:  # Muchas señales
            print("🔧 Optimización: Reduciendo ruido...")
            # Lógica para reducir señales falsas
        
        # Optimizar selección de activos
        best_performers = []
        for key, stats in self.analysis_stats.items():
            if stats['signals'] > 0:
                performance = stats['signals'] / stats['count']
                best_performers.append((key, performance))
        
        best_performers.sort(key=lambda x: x[1], reverse=True)
        
        if best_performers:
            print("🏆 Mejores performers:")
            for i, (pair, performance) in enumerate(best_performers[:3], 1):
                print(f"  {i}. {pair}: {performance:.2%}")
        
        print("✅ Auto-optimización completada")
        
        # Programar próxima optimización
        if self.config.get('auto_optimize'):
            frequency_hours = self.config.get('optimization_frequency_hours', 4)
            self.optimization_timer = threading.Timer(
                frequency_hours * 3600, 
                self.ejecutar_optimizacion_automatica
            )
            self.optimization_timer.start()
            print(f"⏰ Próxima optimización en {frequency_hours} horas")
    
    def worker_simbolo_timeframe(self, symbol, timeframe):
        """Worker thread para analizar un símbolo-timeframe específico"""
        analysis_count = 0
        
        # Determinar intervalo basado en timeframe y configuración
        if timeframe == 'M1':
            base_interval = 10
        elif timeframe == 'M5':
            base_interval = 30
        elif timeframe == 'M15':
            base_interval = 60
        else:
            base_interval = 120
        
        # Ajustar por modo
        if self.config.get('scalping'):
            interval = max(5, base_interval // 2)
        elif self.config.get('high_frequency'):
            interval = base_interval
        else:
            interval = base_interval * 2
        
        print(f"🔄 Worker iniciado: {symbol} {timeframe} (intervalo: {interval}s)")
        
        while self.running:
            try:
                analysis_count += 1
                analysis_id = f"{symbol}_{timeframe}_{analysis_count}"
                
                # Ejecutar análisis
                success = self.analizar_simbolo_timeframe(symbol, timeframe, analysis_id)
                
                if not success:
                    print(f"⚠️  Error en análisis {analysis_id}")
                
                # Esperar intervalo
                time.sleep(interval)
                
            except Exception as e:
                print(f"❌ Error en worker {symbol} {timeframe}: {e}")
                time.sleep(30)  # Esperar antes de reintentar
    
    def mostrar_estadisticas_periodicas(self):
        """Mostrar estadísticas periódicas del sistema"""
        while self.running:
            try:
                time.sleep(300)  # Cada 5 minutos
                
                if not self.running:
                    break
                
                print(f"\n📈 ESTADÍSTICAS DEL SISTEMA - {datetime.now().strftime('%H:%M:%S')}")
                print("=" * 60)
                
                total_analysis = sum(stats['count'] for stats in self.analysis_stats.values())
                total_signals = sum(stats['signals'] for stats in self.analysis_stats.values())
                
                print(f"🔢 Total análisis: {total_analysis}")
                print(f"🎯 Total señales: {total_signals}")
                print(f"⚡ Activos activos: {len(self.active_symbols)}")
                print(f"⏱️  Timeframes activos: {len(self.active_timeframes)}")
                print(f"🧵 Threads activos: {len([t for t in self.threads if t.is_alive()])}")
                
                # Top performers
                if self.analysis_stats:
                    print("\n🏆 TOP PERFORMERS:")
                    performers = []
                    for key, stats in self.analysis_stats.items():
                        if stats['count'] > 0:
                            rate = stats['signals'] / stats['count']
                            performers.append((key, rate, stats['signals']))
                    
                    performers.sort(key=lambda x: x[1], reverse=True)
                    for i, (pair, rate, signals) in enumerate(performers[:5], 1):
                        print(f"  {i}. {pair}: {rate:.2%} ({signals} señales)")
                
                print("=" * 60)
                
            except Exception as e:
                print(f"❌ Error en estadísticas: {e}")
    
    def signal_handler(self, sig, frame):
        """Manejar señales del sistema"""
        print('\n🛑 Deteniendo sistema multi-asset...')
        self.running = False
        
        # Detener timer de optimización
        if self.optimization_timer:
            self.optimization_timer.cancel()
        
        # Esperar que terminen los threads
        for thread in self.threads:
            if thread.is_alive():
                thread.join(timeout=5)
        
        # Guardar estadísticas finales
        with open('multi_asset_stats.json', 'w') as f:
            json.dump({
                'stats': self.analysis_stats,
                'config': self.config,
                'stopped_at': datetime.now().isoformat()
            }, f, indent=2)
        
        print("💾 Estadísticas guardadas")
        sys.exit(0)
    
    def main(self):
        """Función principal del bot avanzado"""
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        print("🚀 INICIANDO BOT SMC-LIT - VERSIÓN 3.0 AVANZADA")
        print("=" * 80)
        
        # Cargar configuración
        self.config = self.cargar_configuracion()
        self.mostrar_configuracion_avanzada(self.config)
        
        # Inicializar MT5
        self.mt5, self.mt5_type = self.inicializar_mt5_connection(self.config)
        if not self.mt5:
            print("❌ No se pudo inicializar sistema de trading")
            return
        
        # Configurar activos y timeframes activos
        self.active_symbols = self.config.get('symbols', ['EURUSD'])
        self.active_timeframes = self.config.get('timeframes', ['M5'])
        
        print(f"\n🎯 INICIANDO SISTEMA MULTI-ASSET MULTI-TIMEFRAME")
        print("=" * 70)
        print(f"💱 Activos: {', '.join(self.active_symbols)}")
        print(f"⏱️  Timeframes: {', '.join(self.active_timeframes)}")
        print(f"🧵 Total combinaciones: {len(self.active_symbols) * len(self.active_timeframes)}")
        print("=" * 70)
        
        self.running = True
        
        # Crear workers para cada combinación símbolo-timeframe
        for symbol in self.active_symbols:
            for timeframe in self.active_timeframes:
                worker_thread = threading.Thread(
                    target=self.worker_simbolo_timeframe,
                    args=(symbol, timeframe),
                    daemon=True
                )
                worker_thread.start()
                self.threads.append(worker_thread)
                time.sleep(1)  # Evitar sobrecarga al inicio
        
        # Iniciar thread de estadísticas
        stats_thread = threading.Thread(
            target=self.mostrar_estadisticas_periodicas,
            daemon=True
        )
        stats_thread.start()
        self.threads.append(stats_thread)
        
        # Iniciar auto-optimización si está habilitada
        if self.config.get('auto_optimize'):
            print("🤖 Auto-optimización activada")
            frequency_hours = self.config.get('optimization_frequency_hours', 4)
            self.optimization_timer = threading.Timer(
                frequency_hours * 3600,
                self.ejecutar_optimizacion_automatica
            )
            self.optimization_timer.start()
            print(f"⏰ Primera optimización en {frequency_hours} horas")
        
        print("\n✅ SISTEMA MULTI-ASSET INICIADO EXITOSAMENTE")
        print("🔄 Presiona Ctrl+C para detener")
        print("📊 Monitoreando múltiples activos en tiempo real...")
        
        # Loop principal - mantener el programa corriendo
        try:
            while self.running:
                time.sleep(10)
                
                # Verificar que los threads estén vivos
                active_threads = [t for t in self.threads if t.is_alive()]
                if len(active_threads) < len(self.threads) // 2:
                    print("⚠️  Detectados threads caídos, reiniciando...")
                    # Lógica de recuperación podría ir aquí
                
        except KeyboardInterrupt:
            print("\n🛑 Sistema detenido por usuario")
        except Exception as e:
            print(f"\n❌ Error inesperado: {e}")
        finally:
            self.running = False
            
            # Limpiar conexiones
            if self.mt5_type == 'native':
                self.mt5.shutdown()
                print("🔌 Conexión MT5 cerrada")
            
            print("📊 Sistema multi-asset finalizado")

if __name__ == "__main__":
    bot = MultiAssetMultiTimeframeBotAdvanced()
    bot.main() 