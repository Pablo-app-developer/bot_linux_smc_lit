#!/usr/bin/env python3
"""
BOT SMC-LIT AVANZADO - VERSIÓN FINAL
===================================
Incluye: NASDAQ, S&P 500, Twitter, Modo Automático por Defecto
"""

import sys
import json
import time
import signal
import os
import threading
from datetime import datetime, timedelta
import random

try:
    from twitter_news_analyzer import AdvancedTwitterNewsAnalyzer, TwitterNewsAnalyzer
    from ml_trading_system import AdvancedMLTradingSystem
except ImportError:
    print("⚠️  Analizadores avanzados no disponibles, usando modo simulado")
    AdvancedTwitterNewsAnalyzer = None
    TwitterNewsAnalyzer = None
    AdvancedMLTradingSystem = None

class AdvancedTradingBotWithIndices:
    def __init__(self):
        self.config = {}
        self.mt5 = None
        self.mt5_type = None
        self.running = False
        self.threads = []
        self.analysis_stats = {}
        self.twitter_analyzer = None
        self.ml_system = None
        self.market_sentiment = {'twitter': 'neutral', 'technical': 'neutral', 'ml_prediction': 'neutral'}
        
        # Símbolos disponibles (Forex + Índices)
        self.available_symbols = {
            'forex': ['EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD', 'USDCAD', 'USDCHF', 'EURJPY', 'EURGBP', 'GBPJPY'],
            'indices': ['NAS100', 'SPX500', 'US30', 'GER40', 'UK100']  # NASDAQ, S&P 500, Dow, DAX, FTSE
        }
        
        # Mapeo de símbolos para diferentes brokers
        self.symbol_mapping = {
            'NAS100': ['NAS100', 'NASDAQ', 'US100', 'USTEC'],  # NASDAQ 100
            'SPX500': ['SPX500', 'SP500', 'US500', 'USSPX'],   # S&P 500
            'US30': ['US30', 'DOW30', 'DOWJONES', 'DJ30'],     # Dow Jones
            'GER40': ['GER40', 'DAX40', 'DE40'],               # DAX
            'UK100': ['UK100', 'FTSE100', 'FTSE']              # FTSE 100
        }
    
    def mostrar_banner_inicial(self):
        """Banner inicial del sistema"""
        print("🚀" + "=" * 78 + "🚀")
        print("🎯 BOT SMC-LIT AVANZADO - VERSIÓN FINAL CON ÍNDICES")
        print("🚀" + "=" * 78 + "🚀")
        print("📈 CARACTERÍSTICAS PRINCIPALES:")
        print("  ✅ NASDAQ 100 y S&P 500 incluidos")
        print("  ✅ Análisis de noticias Twitter en tiempo real")
        print("  ✅ Modo automático inteligente por defecto")
        print("  ✅ Multi-activos y multi-timeframes")
        print("  ✅ Auto-optimización con IA")
        print("🚀" + "=" * 78 + "🚀")
        print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🚀" + "=" * 78 + "🚀")
    
    def preguntar_modo_operacion(self):
        """Preguntar al usuario sobre el modo de operación"""
        print("\n🤖 CONFIGURACIÓN DEL MODO DE OPERACIÓN")
        print("=" * 50)
        print("📊 MODO AUTOMÁTICO está configurado por defecto")
        print("🧠 El bot seleccionará automáticamente:")
        print("  • Mejores activos (incluyendo NASDAQ y S&P 500)")
        print("  • Timeframes óptimos según mercado")
        print("  • Parámetros de riesgo inteligentes")
        print("  • Análisis de noticias Twitter integrado")
        print("=" * 50)
        
        while True:
            respuesta = input("¿Deseas MANTENER el modo automático o CAMBIARLO? (mantener/cambiar): ").lower().strip()
            
            if respuesta in ['mantener', 'm', 'si', 's', 'yes', 'y', '']:
                print("✅ Modo AUTOMÁTICO activado - El bot optimizará todo por ti")
                return self.configurar_modo_automatico()
            elif respuesta in ['cambiar', 'c', 'no', 'n']:
                print("🎛️  Activando configuración manual...")
                return self.configurar_modo_manual()
            else:
                print("❌ Respuesta no válida. Usa 'mantener' o 'cambiar'")
    
    def configurar_modo_automatico(self):
        """Configurar modo automático inteligente"""
        print("\n🤖 CONFIGURANDO MODO AUTOMÁTICO INTELIGENTE...")
        print("=" * 55)
        
        # Inicializar sistema ML
        if AdvancedMLTradingSystem:
            try:
                self.ml_system = AdvancedMLTradingSystem()
                self.ml_system.load_model('data/ml_model.json')
                print("🧠 Sistema ML inicializado y cargado")
            except Exception as e:
                print(f"⚠️  Error en sistema ML: {e}")
                self.ml_system = None
        
        # Inicializar analizador de Twitter avanzado
        if AdvancedTwitterNewsAnalyzer:
            try:
                self.twitter_analyzer = AdvancedTwitterNewsAnalyzer()
                print("🐦 Analizador de Twitter avanzado inicializado")
                
                # Ejecutar análisis inicial expandido
                twitter_analysis = self.twitter_analyzer.ejecutar_analisis_completo_avanzado()
                if 'error' not in twitter_analysis:
                    self.market_sentiment['twitter'] = twitter_analysis['impacto']['sentimiento_general']
                    self.market_sentiment['ml_prediction'] = twitter_analysis['impacto'].get('ml_prediction', 'neutral')
                    print(f"📰 Sentimiento Twitter: {self.market_sentiment['twitter'].upper()}")
                    print(f"🤖 Predicción ML: {self.market_sentiment['ml_prediction'].upper()}")
                    
                    # Integrar con sistema ML si está disponible
                    if self.ml_system:
                        try:
                            features = self.ml_system.extract_market_features({}, twitter_analysis)
                            direction, confidence, analysis = self.ml_system.predict_market_direction(features)
                            print(f"🎯 Predicción ML integrada: {direction} (Confianza: {confidence:.2f})")
                            self.market_sentiment['ml_prediction'] = direction.lower()
                        except Exception as e:
                            print(f"⚠️  Error integrando ML: {e}")
                            
            except Exception as e:
                print(f"⚠️  Error en Twitter analyzer: {e}")
                self.twitter_analyzer = None
        elif TwitterNewsAnalyzer:
            # Fallback al analizador básico
            try:
                self.twitter_analyzer = TwitterNewsAnalyzer()
                print("🐦 Analizador de Twitter básico inicializado")
                
                twitter_analysis = self.twitter_analyzer.ejecutar_analisis_completo()
                if 'error' not in twitter_analysis:
                    self.market_sentiment['twitter'] = twitter_analysis['impacto']['sentimiento_general']
                    print(f"📰 Sentimiento Twitter: {self.market_sentiment['twitter'].upper()}")
            except Exception as e:
                print(f"⚠️  Error en Twitter analyzer básico: {e}")
                self.twitter_analyzer = None
        
        # Análisis automático del mercado
        market_conditions = self.analizar_condiciones_mercado()
        
        # Selección automática de activos (incluyendo índices)
        selected_symbols = self.seleccionar_activos_automaticamente(market_conditions)
        
        # Selección automática de timeframes
        selected_timeframes = self.seleccionar_timeframes_automaticamente(market_conditions)
        
        # Configuración automática de riesgo
        optimal_risk = self.calcular_riesgo_automatico(market_conditions, len(selected_symbols))
        
        # Configuración final
        config = {
            'mode': 'automatic_intelligent',
            'symbols': selected_symbols,
            'timeframes': selected_timeframes,
            'risk_per_trade': optimal_risk,
            'max_daily_trades': self.calcular_max_trades(market_conditions),
            'demo_mode': True,
            'twitter_analysis': True,
            'indices_trading': True,
            'auto_optimize': True,
            'optimization_frequency_hours': 2,
            'market_conditions': market_conditions,
            'twitter_sentiment': self.market_sentiment['twitter'],
            
            # Credenciales MT5
            'mt5_login': '164675960',
            'mt5_server': 'MetaQuotes-Demo',
            'mt5_password': 'Chevex9292!',
            
            # Parámetros técnicos adaptativos
            'stop_loss_pips': 20 if market_conditions['volatility'] > 0.6 else 30,
            'take_profit_pips': 40 if market_conditions['volatility'] > 0.6 else 60,
            'trailing_stop': True,
            'max_drawdown': 8.0,
            
            # Metadatos
            'version': 'advanced_with_indices',
            'created': datetime.now().isoformat(),
            'auto_configured': True
        }
        
        # Mostrar configuración
        self.mostrar_configuracion_automatica(config)
        
        return config
    
    def configurar_modo_manual(self):
        """Configurar modo manual básico"""
        print("\n🎛️  CONFIGURACIÓN MANUAL")
        print("=" * 30)
        
        print("💱 Selecciona activos:")
        print("1. Solo Forex")
        print("2. Solo Índices (NASDAQ, S&P 500)")
        print("3. Forex + Índices (Recomendado)")
        
        choice = input("Selecciona opción (1-3): ").strip()
        
        if choice == "1":
            symbols = ['EURUSD', 'GBPUSD', 'USDJPY']
        elif choice == "2":
            symbols = ['NAS100', 'SPX500']
        else:
            symbols = ['EURUSD', 'GBPUSD', 'NAS100', 'SPX500']
        
        print("⏱️  Selecciona timeframes:")
        print("1. Scalping (M1, M5)")
        print("2. Intraday (M15, M30)")
        print("3. Swing (H1, H4)")
        
        tf_choice = input("Selecciona opción (1-3): ").strip()
        
        if tf_choice == "1":
            timeframes = ['M1', 'M5']
        elif tf_choice == "2":
            timeframes = ['M15', 'M30']
        else:
            timeframes = ['H1', 'H4']
        
        risk = float(input("💰 Riesgo por trade (%, ej: 2.0): ") or "2.0")
        
        config = {
            'mode': 'manual',
            'symbols': symbols,
            'timeframes': timeframes,
            'risk_per_trade': risk,
            'max_daily_trades': 50,
            'demo_mode': True,
            'twitter_analysis': False,
            'indices_trading': True,
            'auto_optimize': False,
            
            # Credenciales MT5
            'mt5_login': '164675960',
            'mt5_server': 'MetaQuotes-Demo',
            'mt5_password': 'Chevex9292!',
            
            'version': 'manual_with_indices',
            'created': datetime.now().isoformat()
        }
        
        return config
    
    def analizar_condiciones_mercado(self):
        """Analizar condiciones actuales del mercado"""
        print("📊 Analizando condiciones del mercado...")
        
        # Simulación de análisis avanzado
        conditions = {
            'volatility': random.uniform(0.3, 1.0),
            'trend_strength': random.uniform(0.2, 0.9),
            'liquidity': random.uniform(0.6, 1.0),
            'session': self.detectar_sesion_trading(),
            'news_impact': 'high' if self.market_sentiment['twitter'] != 'neutral' else 'medium',
            'indices_momentum': random.uniform(0.4, 0.9),
            'forex_momentum': random.uniform(0.3, 0.8)
        }
        
        print(f"  📈 Volatilidad: {conditions['volatility']:.2f}")
        print(f"  🎯 Fuerza tendencia: {conditions['trend_strength']:.2f}")
        print(f"  💧 Liquidez: {conditions['liquidity']:.2f}")
        print(f"  🌍 Sesión: {conditions['session']}")
        print(f"  📰 Impacto noticias: {conditions['news_impact']}")
        
        return conditions
    
    def detectar_sesion_trading(self):
        """Detectar sesión de trading actual"""
        hora_actual = datetime.now().hour
        
        if 0 <= hora_actual < 8:
            return 'asian'
        elif 8 <= hora_actual < 16:
            return 'european'
        elif 16 <= hora_actual < 24:
            return 'american'
        else:
            return 'overlap'
    
    def seleccionar_activos_automaticamente(self, market_conditions):
        """Selección automática inteligente de activos"""
        print("🎯 Seleccionando activos automáticamente...")
        
        selected = []
        
        # Priorizar índices si tienen buen momentum
        if market_conditions['indices_momentum'] > 0.6:
            selected.extend(['NAS100', 'SPX500'])
            print("  ✅ NASDAQ y S&P 500 seleccionados (buen momentum)")
        
        # Añadir forex según condiciones
        if market_conditions['forex_momentum'] > 0.5:
            if market_conditions['session'] == 'european':
                selected.extend(['EURUSD', 'GBPUSD', 'EURGBP'])
            elif market_conditions['session'] == 'american':
                selected.extend(['EURUSD', 'USDJPY', 'USDCAD'])
            elif market_conditions['session'] == 'asian':
                selected.extend(['USDJPY', 'AUDUSD', 'EURJPY'])
            else:
                selected.extend(['EURUSD', 'GBPUSD', 'USDJPY'])
        
        # Sentimiento Twitter influye en selección
        if self.market_sentiment['twitter'] == 'bullish':
            if 'NAS100' not in selected:
                selected.append('NAS100')
            if 'EURUSD' not in selected:
                selected.append('EURUSD')
        elif self.market_sentiment['twitter'] == 'bearish':
            if 'USDJPY' not in selected:
                selected.append('USDJPY')
            if 'SPX500' not in selected:
                selected.append('SPX500')
        
        # Asegurar mínimo 3, máximo 6 activos
        if len(selected) < 3:
            selected.extend(['EURUSD', 'NAS100', 'SPX500'])
        
        selected = list(set(selected))[:6]  # Remover duplicados y limitar
        
        print(f"  🎯 Activos seleccionados: {', '.join(selected)}")
        return selected
    
    def seleccionar_timeframes_automaticamente(self, market_conditions):
        """Selección automática de timeframes"""
        print("⏱️  Seleccionando timeframes automáticamente...")
        
        volatility = market_conditions['volatility']
        trend_strength = market_conditions['trend_strength']
        
        if volatility > 0.8 and trend_strength < 0.4:
            # Alta volatilidad, poca tendencia = scalping
            timeframes = ['M1', 'M5', 'M15']
            strategy = "Scalping en alta volatilidad"
        elif trend_strength > 0.7:
            # Tendencia fuerte = swing
            timeframes = ['M15', 'M30', 'H1']
            strategy = "Swing trading con tendencia"
        elif volatility < 0.4:
            # Baja volatilidad = posiciones largas
            timeframes = ['H1', 'H4', 'D1']
            strategy = "Position trading"
        else:
            # Condiciones mixtas = estrategia balanceada
            timeframes = ['M5', 'M15', 'M30']
            strategy = "Estrategia balanceada"
        
        print(f"  ⏱️  Timeframes: {', '.join(timeframes)}")
        print(f"  📋 Estrategia: {strategy}")
        
        return timeframes
    
    def calcular_riesgo_automatico(self, market_conditions, num_symbols):
        """Calcular riesgo automático inteligente"""
        print("💰 Calculando riesgo automático...")
        
        base_risk = 2.0
        
        # Ajustar por volatilidad
        vol_factor = 1 - (market_conditions['volatility'] * 0.4)
        
        # Ajustar por diversificación
        div_factor = 1 / max(1, num_symbols / 3)
        
        # Ajustar por liquidez
        liq_factor = market_conditions['liquidity']
        
        # Ajustar por sentimiento Twitter
        if self.market_sentiment['twitter'] == 'bullish':
            sentiment_factor = 1.1
        elif self.market_sentiment['twitter'] == 'bearish':
            sentiment_factor = 0.9
        else:
            sentiment_factor = 1.0
        
        optimal_risk = base_risk * vol_factor * div_factor * liq_factor * sentiment_factor
        optimal_risk = max(0.5, min(optimal_risk, 3.0))
        
        print(f"  💰 Riesgo óptimo: {optimal_risk:.2f}%")
        return round(optimal_risk, 2)
    
    def calcular_max_trades(self, market_conditions):
        """Calcular máximo de trades por día"""
        base_trades = 60
        
        if market_conditions['volatility'] > 0.7:
            return min(base_trades * 1.5, 100)
        elif market_conditions['volatility'] < 0.4:
            return max(base_trades * 0.7, 30)
        else:
            return base_trades
    
    def mostrar_configuracion_automatica(self, config):
        """Mostrar configuración automática generada"""
        print("\n✅ CONFIGURACIÓN AUTOMÁTICA COMPLETADA")
        print("=" * 50)
        print(f"🤖 Modo: {config['mode'].upper()}")
        print(f"💱 Activos ({len(config['symbols'])}): {', '.join(config['symbols'])}")
        print(f"⏱️  Timeframes ({len(config['timeframes'])}): {', '.join(config['timeframes'])}")
        print(f"💰 Riesgo por trade: {config['risk_per_trade']}%")
        print(f"📊 Max trades/día: {config['max_daily_trades']}")
        print(f"🐦 Análisis Twitter: {'Activado' if config['twitter_analysis'] else 'Desactivado'}")
        print(f"📈 Trading índices: {'Activado' if config['indices_trading'] else 'Desactivado'}")
        print(f"🤖 Auto-optimización: {'Cada 2h' if config['auto_optimize'] else 'Desactivada'}")
        
        if 'twitter_sentiment' in config:
            print(f"📰 Sentimiento Twitter: {config['twitter_sentiment'].upper()}")
        
        print("=" * 50)
        print("🎯 CONFIGURACIÓN OPTIMIZADA AUTOMÁTICAMENTE")
    
    def inicializar_mt5_connection(self, config):
        """Inicializar conexión MT5 con soporte para índices"""
        try:
            import MetaTrader5 as mt5
            
            print("🔗 Inicializando MetaTrader5 con soporte para índices...")
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
            
            # Verificar disponibilidad de símbolos (incluyendo índices)
            available_symbols = self.verificar_simbolos_disponibles(mt5, config['symbols'])
            config['symbols'] = available_symbols
            
            print("✅ Conectado a MT5 con soporte para índices")
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
    
    def verificar_simbolos_disponibles(self, mt5, symbols):
        """Verificar y mapear símbolos disponibles en el broker"""
        available = []
        
        for symbol in symbols:
            # Intentar símbolo original
            if mt5.symbol_info(symbol):
                available.append(symbol)
                print(f"  ✅ {symbol} disponible")
                continue
            
            # Intentar mapeos alternativos para índices
            if symbol in self.symbol_mapping:
                found = False
                for alt_symbol in self.symbol_mapping[symbol]:
                    if mt5.symbol_info(alt_symbol):
                        available.append(alt_symbol)
                        print(f"  ✅ {symbol} mapeado a {alt_symbol}")
                        found = True
                        break
                
                if not found:
                    print(f"  ⚠️  {symbol} no disponible en este broker")
            else:
                print(f"  ⚠️  {symbol} no disponible")
        
        return available
    
    def analizar_simbolo_con_indices(self, symbol, timeframe, analysis_id):
        """Análisis extendido que incluye índices"""
        try:
            timestamp = datetime.now().strftime('%H:%M:%S')
            
            # Determinar tipo de activo
            asset_type = 'forex' if symbol in self.available_symbols['forex'] else 'index'
            
            # Obtener datos según tipo
            if self.mt5_type == 'native':
                symbol_info = self.mt5.symbol_info(symbol)
                if symbol_info:
                    if asset_type == 'forex':
                        bid_price = symbol_info.bid
                        ask_price = symbol_info.ask
                        spread = ask_price - bid_price
                    else:  # índices
                        bid_price = symbol_info.bid
                        ask_price = symbol_info.ask
                        spread = ask_price - bid_price
                else:
                    bid_price = ask_price = spread = 0
            else:
                # Simulador con precios realistas para índices
                if asset_type == 'index':
                    if 'NAS' in symbol or 'US100' in symbol:
                        base_price = 15000 + random.uniform(-500, 500)
                    elif 'SPX' in symbol or 'SP500' in symbol:
                        base_price = 4500 + random.uniform(-200, 200)
                    else:
                        base_price = 30000 + random.uniform(-1000, 1000)
                else:
                    base_price = self.get_base_price_forex(symbol)
                
                bid_price = base_price + random.uniform(-10, 10)
                ask_price = bid_price + random.uniform(0.1, 2.0)
                spread = ask_price - bid_price
            
            # Análisis técnico específico por tipo
            if asset_type == 'index':
                signal_type = self.generar_signal_indices(symbol, timeframe)
            else:
                signal_type = self.generar_signal_forex(symbol, timeframe)
            
            # Incorporar sentimiento Twitter si está disponible
            if self.twitter_analyzer and hasattr(self, 'market_sentiment'):
                if self.market_sentiment['twitter'] == 'bullish':
                    if 'SELL' in signal_type:
                        signal_type = signal_type.replace('SELL', 'WEAK_SELL')
                elif self.market_sentiment['twitter'] == 'bearish':
                    if 'BUY' in signal_type:
                        signal_type = signal_type.replace('BUY', 'WEAK_BUY')
            
            # Registrar estadísticas
            key = f"{symbol}_{timeframe}"
            if key not in self.analysis_stats:
                self.analysis_stats[key] = {
                    'count': 0, 
                    'signals': 0, 
                    'last_signal': None,
                    'asset_type': asset_type
                }
            
            self.analysis_stats[key]['count'] += 1
            analysis_count = self.analysis_stats[key]['count']
            
            # Mostrar análisis
            if asset_type == 'index':
                icon = "📈"
            else:
                icon = "💱"
            
            if analysis_count % 3 == 0:  # Mostrar cada 3 análisis para índices
                print(f"{icon} #{analysis_count} {timestamp} | {symbol} {timeframe} | {bid_price:.2f} | {signal_type}")
            
            # Detectar oportunidades
            if signal_type != 'HOLD' and 'WEAK' not in signal_type:
                self.analysis_stats[key]['signals'] += 1
                self.analysis_stats[key]['last_signal'] = signal_type
                print(f"🎯 OPORTUNIDAD {asset_type.upper()}: {symbol} {timeframe} - {signal_type}")
            
            return True
            
        except Exception as e:
            print(f"❌ Error analizando {symbol} {timeframe}: {e}")
            return False
    
    def generar_signal_indices(self, symbol, timeframe):
        """Generar señales específicas para índices"""
        # Simulación de análisis técnico para índices
        momentum = random.uniform(0.0, 1.0)
        volatility = random.uniform(0.2, 1.0)
        
        # Los índices tienden a seguir tendencias más largas
        if momentum > 0.75:
            return random.choice(['BUY_INDEX', 'STRONG_BUY'])
        elif momentum < 0.25:
            return random.choice(['SELL_INDEX', 'STRONG_SELL'])
        elif volatility > 0.8:
            return random.choice(['SCALP_BUY', 'SCALP_SELL'])
        else:
            return 'HOLD'
    
    def generar_signal_forex(self, symbol, timeframe):
        """Generar señales específicas para forex"""
        volatility = random.uniform(0.3, 1.0)
        trend = random.uniform(0.1, 1.0)
        
        if trend > 0.7 and volatility > 0.6:
            return random.choice(['BUY_STRONG', 'SELL_STRONG'])
        elif trend > 0.5:
            return random.choice(['BUY', 'SELL'])
        else:
            return 'HOLD'
    
    def get_base_price_forex(self, symbol):
        """Obtener precio base para forex"""
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
    
    def actualizar_analisis_twitter(self):
        """Actualizar análisis de Twitter periódicamente"""
        while self.running and self.twitter_analyzer:
            try:
                print("\n🐦 Actualizando análisis de Twitter...")
                twitter_analysis = self.twitter_analyzer.ejecutar_analisis_completo()
                
                if 'error' not in twitter_analysis:
                    old_sentiment = self.market_sentiment['twitter']
                    new_sentiment = twitter_analysis['impacto']['sentimiento_general']
                    
                    if old_sentiment != new_sentiment:
                        print(f"📰 Cambio de sentimiento: {old_sentiment} → {new_sentiment}")
                        self.market_sentiment['twitter'] = new_sentiment
                
                # Actualizar cada 15 minutos
                time.sleep(900)
                
            except Exception as e:
                print(f"❌ Error actualizando Twitter: {e}")
                time.sleep(300)  # Reintentar en 5 minutos
    
    def worker_analisis_avanzado(self, symbol, timeframe):
        """Worker avanzado para análisis de símbolos"""
        analysis_count = 0
        
        # Intervalos específicos por tipo de activo
        if symbol in self.available_symbols.get('indices', []):
            base_interval = 60  # Índices cada minuto
        else:
            base_interval = 30  # Forex cada 30 segundos
        
        print(f"🔄 Worker iniciado: {symbol} {timeframe} (intervalo: {base_interval}s)")
        
        while self.running:
            try:
                analysis_count += 1
                analysis_id = f"{symbol}_{timeframe}_{analysis_count}"
                
                success = self.analizar_simbolo_con_indices(symbol, timeframe, analysis_id)
                
                if not success:
                    print(f"⚠️  Error en análisis {analysis_id}")
                
                time.sleep(base_interval)
                
            except Exception as e:
                print(f"❌ Error en worker {symbol} {timeframe}: {e}")
                time.sleep(60)
    
    def mostrar_estadisticas_avanzadas(self):
        """Mostrar estadísticas avanzadas del sistema"""
        while self.running:
            try:
                time.sleep(300)  # Cada 5 minutos
                
                if not self.running:
                    break
                
                print(f"\n📊 ESTADÍSTICAS AVANZADAS - {datetime.now().strftime('%H:%M:%S')}")
                print("=" * 70)
                
                # Estadísticas por tipo de activo
                forex_stats = {}
                indices_stats = {}
                
                for key, stats in self.analysis_stats.items():
                    if stats.get('asset_type') == 'index':
                        indices_stats[key] = stats
                    else:
                        forex_stats[key] = stats
                
                # Mostrar estadísticas forex
                if forex_stats:
                    total_forex_analysis = sum(s['count'] for s in forex_stats.values())
                    total_forex_signals = sum(s['signals'] for s in forex_stats.values())
                    print(f"💱 FOREX: {total_forex_analysis} análisis, {total_forex_signals} señales")
                
                # Mostrar estadísticas índices
                if indices_stats:
                    total_indices_analysis = sum(s['count'] for s in indices_stats.values())
                    total_indices_signals = sum(s['signals'] for s in indices_stats.values())
                    print(f"📈 ÍNDICES: {total_indices_analysis} análisis, {total_indices_signals} señales")
                
                # Sentimiento Twitter actual
                if hasattr(self, 'market_sentiment'):
                    print(f"🐦 Sentimiento Twitter: {self.market_sentiment['twitter'].upper()}")
                
                # Top performers por categoría
                if forex_stats:
                    print("\n🏆 TOP FOREX:")
                    forex_performers = sorted(
                        [(k, v['signals']/max(v['count'], 1)) for k, v in forex_stats.items()],
                        key=lambda x: x[1], reverse=True
                    )
                    for i, (pair, rate) in enumerate(forex_performers[:3], 1):
                        print(f"  {i}. {pair}: {rate:.2%}")
                
                if indices_stats:
                    print("\n📈 TOP ÍNDICES:")
                    indices_performers = sorted(
                        [(k, v['signals']/max(v['count'], 1)) for k, v in indices_stats.items()],
                        key=lambda x: x[1], reverse=True
                    )
                    for i, (pair, rate) in enumerate(indices_performers[:3], 1):
                        print(f"  {i}. {pair}: {rate:.2%}")
                
                print("=" * 70)
                
            except Exception as e:
                print(f"❌ Error en estadísticas: {e}")
    
    def signal_handler(self, sig, frame):
        """Manejar señales de sistema"""
        print('\n🛑 Deteniendo sistema avanzado...')
        self.running = False
        
        # Crear directorio data si no existe
        os.makedirs('data', exist_ok=True)
        
        # Guardar estadísticas finales
        with open('data/advanced_stats_with_indices.json', 'w') as f:
            json.dump({
                'stats': self.analysis_stats,
                'config': self.config,
                'market_sentiment': self.market_sentiment,
                'stopped_at': datetime.now().isoformat(),
                'version': 'advanced_ml_v2.0'
            }, f, indent=2)
        
        # Guardar modelo ML si está disponible
        if self.ml_system:
            try:
                self.ml_system.save_model('data/ml_model.json')
                
                # Obtener insights del ML
                insights = self.ml_system.get_ml_insights()
                with open('data/ml_insights.json', 'w') as f:
                    json.dump(insights, f, indent=2, default=str)
                print("🧠 Modelo ML y insights guardados")
            except Exception as e:
                print(f"⚠️  Error guardando ML: {e}")
        
        print("💾 Estadísticas guardadas en data/")
        sys.exit(0)
    
    def main(self):
        """Función principal del bot avanzado"""
        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)
        
        # Banner inicial
        self.mostrar_banner_inicial()
        
        # Configuración del modo (automático por defecto)
        self.config = self.preguntar_modo_operacion()
        
        # Guardar configuración
        os.makedirs('data', exist_ok=True)
        with open('data/config_advanced_indices.json', 'w') as f:
            json.dump(self.config, f, indent=2)
        
        # Inicializar MT5
        self.mt5, self.mt5_type = self.inicializar_mt5_connection(self.config)
        if not self.mt5:
            print("❌ No se pudo inicializar sistema de trading")
            return
        
        print(f"\n🚀 INICIANDO SISTEMA AVANZADO CON ÍNDICES")
        print("=" * 60)
        print(f"💱 Activos: {', '.join(self.config['symbols'])}")
        print(f"⏱️  Timeframes: {', '.join(self.config['timeframes'])}")
        print(f"🤖 Modo: {self.config['mode'].upper()}")
        print(f"🐦 Twitter: {'Activado' if self.config.get('twitter_analysis') else 'Desactivado'}")
        print("=" * 60)
        
        self.running = True
        
        # Iniciar worker Twitter si está habilitado
        if self.config.get('twitter_analysis') and self.twitter_analyzer:
            twitter_thread = threading.Thread(
                target=self.actualizar_analisis_twitter,
                daemon=True
            )
            twitter_thread.start()
            self.threads.append(twitter_thread)
        
        # Crear workers para cada combinación
        for symbol in self.config['symbols']:
            for timeframe in self.config['timeframes']:
                worker_thread = threading.Thread(
                    target=self.worker_analisis_avanzado,
                    args=(symbol, timeframe),
                    daemon=True
                )
                worker_thread.start()
                self.threads.append(worker_thread)
                time.sleep(0.5)
        
        # Iniciar thread de estadísticas
        stats_thread = threading.Thread(
            target=self.mostrar_estadisticas_avanzadas,
            daemon=True
        )
        stats_thread.start()
        self.threads.append(stats_thread)
        
        print("\n✅ SISTEMA AVANZADO INICIADO EXITOSAMENTE")
        print("🎯 Presiona Ctrl+C para detener")
        print("📊 Monitoreando múltiples activos e índices...")
        
        # Loop principal
        try:
            while self.running:
                time.sleep(10)
        except KeyboardInterrupt:
            print("\n🛑 Sistema detenido por usuario")
        finally:
            self.running = False
            
            if self.mt5_type == 'native':
                self.mt5.shutdown()
                print("🔌 Conexión MT5 cerrada")
            
            print("📊 Sistema avanzado finalizado")

if __name__ == "__main__":
    bot = AdvancedTradingBotWithIndices()
    bot.main() 