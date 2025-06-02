#!/usr/bin/env python3
"""
IMPLEMENTADOR DE ESTRATEGIA OPTIMIZADA
Toma los parámetros optimizados y los implementa automáticamente
en el sistema de trading para uso en vivo
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
import json
from typing import Dict, List, Optional
from dataclasses import dataclass
warnings.filterwarnings('ignore')

# Configurar path
sys.path.append('src')

from src.mt5_connector import MT5Connector
from src.features import SMCFeatureExtractor  
from src.strategy import SMCStrategy
from src.backtester_realistic import RealisticBacktester

class OptimizedStrategyImplementer:
    """
    Implementa automáticamente la estrategia optimizada
    """
    
    def __init__(self):
        self.optimized_params = None
        self.implementation_config = {
            'live_trading': False,  # Empezar con demo
            'initial_balance': 10000,
            'max_risk_per_trade': 0.02,  # 2% máximo
            'monitoring_enabled': True,
            'auto_adjust': True
        }
        
    def load_optimized_parameters(self, params_file: str = None) -> Dict:
        """Carga parámetros optimizados desde archivo"""
        print(f"📂 CARGANDO PARÁMETROS OPTIMIZADOS")
        
        if params_file is None:
            # Buscar el archivo más reciente
            files = [f for f in os.listdir('.') if f.startswith('optimized_params_')]
            if not files:
                files = [f for f in os.listdir('.') if f.startswith('master_optimization_results_')]
            
            if not files:
                raise FileNotFoundError("No se encontraron archivos de parámetros optimizados")
            
            # Tomar el más reciente
            params_file = sorted(files)[-1]
            print(f"   📄 Archivo detectado: {params_file}")
        
        # Cargar parámetros
        with open(params_file, 'r') as f:
            if params_file.startswith('master_optimization_results_'):
                data = json.load(f)
                self.optimized_params = data['optimization_results']['final_params']
            else:
                self.optimized_params = json.load(f)
        
        if not self.optimized_params:
            raise ValueError("No se pudieron cargar los parámetros optimizados")
        
        print(f"✅ Parámetros cargados exitosamente")
        return self.optimized_params
    
    def validate_parameters(self, params: Dict) -> bool:
        """Valida que los parámetros estén en rangos seguros"""
        print(f"🔍 VALIDANDO PARÁMETROS")
        
        # Rangos seguros para trading en vivo
        safe_ranges = {
            'swing_length': (2, 10),
            'ob_strength': (1, 5),
            'liq_threshold': (0.0001, 0.005),
            'fvg_min_size': (0.0001, 0.002),
            'risk_per_trade': (0.001, 0.03),
            'rsi_period': (5, 50),
            'rsi_overbought': (60, 90),
            'rsi_oversold': (10, 40),
            'atr_period': (5, 50),
            'atr_multiplier': (0.5, 5.0),
            'ema_short': (5, 50),
            'ema_long': (20, 200),
            'sl_probability': (0.1, 0.9),
            'tp_probability': (0.1, 0.9)
        }
        
        warnings = []
        errors = []
        
        for param, value in params.items():
            if param in safe_ranges:
                min_val, max_val = safe_ranges[param]
                if not (min_val <= value <= max_val):
                    if param == 'risk_per_trade' and value > max_val:
                        errors.append(f"❌ {param}: {value} > {max_val} (RIESGO EXCESIVO)")
                    else:
                        warnings.append(f"⚠️ {param}: {value} fuera de rango seguro [{min_val}, {max_val}]")
        
        # Validaciones específicas
        if params.get('risk_per_trade', 0) > 0.02:
            errors.append("❌ Risk per trade > 2% es peligroso para live trading")
        
        if params.get('sl_probability', 0.5) > params.get('tp_probability', 0.5):
            warnings.append("⚠️ SL probability > TP probability puede ser problemático")
        
        # Mostrar resultados
        if errors:
            print(f"   ❌ ERRORES CRÍTICOS:")
            for error in errors:
                print(f"      {error}")
            return False
        
        if warnings:
            print(f"   ⚠️ ADVERTENCIAS:")
            for warning in warnings:
                print(f"      {warning}")
        
        print(f"   ✅ Validación completada")
        return True
    
    def adjust_parameters_for_live(self, params: Dict) -> Dict:
        """Ajusta parámetros para trading en vivo más conservador"""
        print(f"🛡️ AJUSTANDO PARÁMETROS PARA LIVE TRADING")
        
        adjusted = params.copy()
        
        # Hacer más conservador el riesgo
        if adjusted.get('risk_per_trade', 0) > 0.015:
            original_risk = adjusted['risk_per_trade']
            adjusted['risk_per_trade'] = min(original_risk, 0.015)
            print(f"   📉 Risk per trade: {original_risk:.4f} → {adjusted['risk_per_trade']:.4f}")
        
        # Ajustar probabilidades para ser más conservadores
        if adjusted.get('sl_probability', 0.5) < 0.3:
            adjusted['sl_probability'] = 0.3
            print(f"   🛡️ SL probability ajustada a mínimo seguro: 0.3")
        
        if adjusted.get('tp_probability', 0.5) > 0.8:
            adjusted['tp_probability'] = 0.8
            print(f"   🎯 TP probability ajustada a máximo seguro: 0.8")
        
        # Añadir filtros de seguridad si no existen
        safety_filters = {
            'trend_filter': True,
            'volatility_filter': True,
            'rsi_filter': True,
            'volume_filter': False
        }
        
        for filter_name, default_value in safety_filters.items():
            if filter_name not in adjusted:
                adjusted[filter_name] = default_value
                print(f"   🔒 Añadido filtro de seguridad: {filter_name} = {default_value}")
        
        print(f"   ✅ Parámetros ajustados para máxima seguridad")
        return adjusted
    
    def create_optimized_strategy_class(self, params: Dict) -> str:
        """Crea una clase de estrategia optimizada"""
        print(f"🏗️ CREANDO CLASE DE ESTRATEGIA OPTIMIZADA")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        class_code = f'''#!/usr/bin/env python3
"""
ESTRATEGIA OPTIMIZADA AUTOMÁTICAMENTE
Generada por el Sistema Maestro de Optimización
Fecha: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
Win Rate Objetivo: 80%+
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configurar path
sys.path.append('src')

from src.mt5_connector import MT5Connector
from src.features import SMCFeatureExtractor  
from src.strategy import SMCStrategy
from src.backtester_realistic import RealisticBacktester

class OptimizedStrategy:
    """
    Estrategia con parámetros optimizados automáticamente
    """
    
    def __init__(self):
        # Parámetros optimizados por el sistema maestro
        self.optimized_params = {json.dumps(params, indent=12)}
        
        # Configuración de trading
        self.initial_balance = 10000
        self.pairs = ['EURUSD']
        self.timeframes = ['H1']
        
    def create_features(self, df):
        """Crea features con parámetros optimizados"""
        extractor = SMCFeatureExtractor(df)
        extractor.swing_length = int(self.optimized_params['swing_length'])
        df_features = extractor.extract_all()
        
        # Añadir indicadores técnicos optimizados
        df_features['rsi'] = self.calculate_rsi(
            df_features['close'], 
            int(self.optimized_params['rsi_period'])
        )
        
        df_features['atr'] = self.calculate_atr(
            df_features, 
            int(self.optimized_params['atr_period'])
        )
        
        # EMAs optimizadas
        df_features['ema_short'] = df_features['close'].ewm(
            span=int(self.optimized_params['ema_short'])
        ).mean()
        
        df_features['ema_long'] = df_features['close'].ewm(
            span=int(self.optimized_params['ema_long'])
        ).mean()
        
        df_features['trend_bullish'] = df_features['ema_short'] > df_features['ema_long']
        
        return df_features
    
    def calculate_rsi(self, prices, period):
        """RSI optimizado"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    def calculate_atr(self, df, period):
        """ATR optimizado"""
        high_low = df['high'] - df['low']
        high_close = np.abs(df['high'] - df['close'].shift())
        low_close = np.abs(df['low'] - df['close'].shift())
        true_range = np.maximum(high_low, np.maximum(high_close, low_close))
        return true_range.rolling(window=period).mean()
    
    def create_strategy(self, df_features):
        """Crea estrategia con parámetros optimizados"""
        strategy = SMCStrategy(df_features)
        
        # Aplicar parámetros optimizados
        strategy.swing_length = int(self.optimized_params['swing_length'])
        strategy.ob_strength = int(self.optimized_params['ob_strength'])
        strategy.liq_threshold = self.optimized_params['liq_threshold']
        strategy.fvg_min_size = self.optimized_params['fvg_min_size']
        
        return strategy
    
    def apply_optimized_filters(self, df_signals):
        """Aplica filtros optimizados"""
        df_filtered = df_signals.copy()
        
        for i in range(len(df_filtered)):
            if df_filtered['signal'].iloc[i] != 0:
                
                # Filtro de tendencia
                if self.optimized_params.get('trend_filter', True):
                    if df_filtered['signal'].iloc[i] == 1 and not df_filtered.get('trend_bullish', True).iloc[i]:
                        df_filtered.at[df_filtered.index[i], 'signal'] = 0
                        continue
                    elif df_filtered['signal'].iloc[i] == -1 and df_filtered.get('trend_bullish', False).iloc[i]:
                        df_filtered.at[df_filtered.index[i], 'signal'] = 0
                        continue
                
                # Filtro RSI optimizado
                if self.optimized_params.get('rsi_filter', True):
                    rsi = df_filtered.get('rsi', 50).iloc[i]
                    if (rsi > self.optimized_params['rsi_overbought'] or 
                        rsi < self.optimized_params['rsi_oversold']):
                        df_filtered.at[df_filtered.index[i], 'signal'] = 0
                        continue
                
                # Filtro de volatilidad optimizado
                if self.optimized_params.get('volatility_filter', True):
                    atr = df_filtered.get('atr', 0.001).iloc[i]
                    atr_avg = df_filtered.get('atr', pd.Series([0.001]*len(df_filtered))).iloc[max(0,i-20):i].mean()
                    if atr > atr_avg * self.optimized_params['atr_multiplier']:
                        df_filtered.at[df_filtered.index[i], 'signal'] = 0
                        continue
        
        return df_filtered
    
    def run_optimized_backtest(self, symbol='EURUSD', timeframe='H1', candles=2000):
        """Ejecuta backtest con estrategia optimizada"""
        print(f"🚀 EJECUTANDO ESTRATEGIA OPTIMIZADA")
        print(f"Parámetros: Optimizados automáticamente")
        print(f"Símbolo: {{symbol}}, Timeframe: {{timeframe}}")
        print("=" * 60)
        
        try:
            # Obtener datos
            connector = MT5Connector(symbol=symbol, timeframe=timeframe)
            df = connector.fetch_ohlc_data(num_candles=candles)
            
            if df is None or len(df) < 500:
                print("❌ Datos insuficientes")
                return None
            
            print(f"📊 Analizando {{len(df)}} velas...")
            
            # Crear features optimizadas
            df_features = self.create_features(df)
            
            # Crear estrategia optimizada
            strategy = self.create_strategy(df_features)
            df_signals = strategy.run()
            
            # Aplicar filtros optimizados
            df_filtered = self.apply_optimized_filters(df_signals)
            
            # Backtesting con parámetros optimizados
            backtester = RealisticBacktester(
                df_filtered,
                initial_balance=self.initial_balance,
                risk_per_trade=self.optimized_params['risk_per_trade'],
                commission=0.00007
            )
            
            # Aplicar probabilidades optimizadas
            backtester.sl_probability = self.optimized_params['sl_probability']
            backtester.tp_probability = self.optimized_params['tp_probability']
            
            results = backtester.run()
            
            # Análisis de resultados
            self.analyze_optimized_results(results)
            
            return results
            
        except Exception as e:
            print(f"❌ Error: {{e}}")
            return None
    
    def analyze_optimized_results(self, results):
        """Analiza resultados de la estrategia optimizada"""
        if not results['trades'] or len(results['trades']) == 0:
            print("❌ No se generaron trades")
            return
        
        trades_df = pd.DataFrame(results['trades'])
        
        # Métricas principales
        total_trades = len(trades_df)
        winners = trades_df[trades_df['was_profitable'] == True]
        win_count = len(winners)
        win_rate = (win_count / total_trades * 100) if total_trades > 0 else 0
        
        total_pnl = trades_df['pnl'].sum()
        total_return = (total_pnl / self.initial_balance * 100)
        
        # Profit factor
        gross_profit = trades_df[trades_df['was_profitable'] == True]['pnl'].sum()
        gross_loss = abs(trades_df[trades_df['was_profitable'] == False]['pnl'].sum())
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')
        
        print(f"\\n🎯 RESULTADOS ESTRATEGIA OPTIMIZADA:")
        print(f"   💼 Trades: {{total_trades}}")
        print(f"   ✅ Win Rate: {{win_rate:.1f}}%")
        print(f"   💰 P&L: ${{total_pnl:+.2f}}")
        print(f"   📈 Retorno: {{total_return:+.1f}}%")
        print(f"   📊 Profit Factor: {{profit_factor:.2f}}")
        
        # Evaluación del rendimiento
        print(f"\\n🏆 EVALUACIÓN DE RENDIMIENTO:")
        if win_rate >= 80:
            print(f"   🥇 EXCELENTE: {{win_rate:.1f}}% - Supera expectativas")
        elif win_rate >= 70:
            print(f"   🥈 MUY BUENO: {{win_rate:.1f}}% - Rendimiento profesional")
        elif win_rate >= 60:
            print(f"   🥉 BUENO: {{win_rate:.1f}}% - Rendimiento sólido")
        else:
            print(f"   ⚠️ REVISAR: {{win_rate:.1f}}% - Necesita ajustes")
        
        return {{
            'win_rate': win_rate,
            'total_return': total_return,
            'profit_factor': profit_factor,
            'total_trades': total_trades
        }}

def main():
    """Ejecuta la estrategia optimizada"""
    strategy = OptimizedStrategy()
    results = strategy.run_optimized_backtest()
    
    if results:
        print(f"\\n✅ Estrategia optimizada ejecutada exitosamente")
    else:
        print(f"\\n❌ Error ejecutando estrategia optimizada")

if __name__ == "__main__":
    main()
'''
        
        filename = f"optimized_strategy_{timestamp}.py"
        with open(filename, 'w') as f:
            f.write(class_code)
        
        print(f"   ✅ Clase creada: {filename}")
        return filename
    
    def create_live_trading_config(self, params: Dict) -> str:
        """Crea configuración para trading en vivo"""
        print(f"⚡ CREANDO CONFIGURACIÓN LIVE TRADING")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        live_config = {
            "system_info": {
                "name": "Optimized Live Trading Bot",
                "version": "1.0",
                "created": datetime.now().isoformat(),
                "optimization_source": "Master Optimization System"
            },
            "trading_parameters": params,
            "risk_management": {
                "max_risk_per_trade": min(params.get('risk_per_trade', 0.01), 0.015),
                "max_daily_risk": 0.05,  # 5% máximo por día
                "max_drawdown": 0.15,    # 15% máximo drawdown
                "stop_trading_on_drawdown": True,
                "position_sizing": "fixed_risk"
            },
            "execution_settings": {
                "slippage_tolerance": 0.00002,  # 0.2 pips
                "max_spread": 0.00015,          # 1.5 pips
                "trading_hours": {
                    "start": "08:00",
                    "end": "18:00",
                    "timezone": "UTC"
                },
                "avoid_news": True,
                "max_positions": 3
            },
            "monitoring": {
                "performance_tracking": True,
                "real_time_alerts": True,
                "daily_reports": True,
                "stop_loss_alerts": True,
                "profit_alerts": True
            }
        }
        
        filename = f"live_trading_config_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(live_config, f, indent=2)
        
        print(f"   ✅ Configuración live: {filename}")
        return filename
    
    def run_final_validation(self, params: Dict) -> Dict:
        """Ejecuta validación final antes de implementación"""
        print(f"🔬 VALIDACIÓN FINAL PRE-IMPLEMENTACIÓN")
        
        try:
            # Crear estrategia temporalmente para validación
            connector = MT5Connector(symbol='EURUSD', timeframe='H1')
            df = connector.fetch_ohlc_data(num_candles=1000)
            
            if df is None:
                return {'success': False, 'error': 'No se pudieron obtener datos de validación'}
            
            # Test rápido con parámetros
            extractor = SMCFeatureExtractor(df)
            extractor.swing_length = int(params['swing_length'])
            df_features = extractor.extract_all()
            
            # Verificar que genera señales
            strategy = SMCStrategy(df_features)
            strategy.swing_length = int(params['swing_length'])
            strategy.ob_strength = int(params['ob_strength'])
            strategy.liq_threshold = params['liq_threshold']
            strategy.fvg_min_size = params['fvg_min_size']
            
            df_signals = strategy.run()
            signal_count = len(df_signals[df_signals['signal'] != 0])
            
            print(f"   📊 Señales generadas en validación: {signal_count}")
            
            if signal_count == 0:
                return {'success': False, 'error': 'No se generan señales de trading'}
            
            # Test de backtesting rápido
            backtester = RealisticBacktester(
                df_signals,
                initial_balance=10000,
                risk_per_trade=params['risk_per_trade'],
                commission=0.00007
            )
            
            results = backtester.run()
            
            if not results['trades']:
                return {'success': False, 'error': 'No se ejecutan trades en backtesting'}
            
            trades_df = pd.DataFrame(results['trades'])
            win_rate = (trades_df['was_profitable'].sum() / len(trades_df)) * 100
            
            print(f"   🎯 Win rate validación: {win_rate:.1f}%")
            
            return {
                'success': True,
                'validation_win_rate': win_rate,
                'signal_count': signal_count,
                'trade_count': len(trades_df)
            }
            
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def implement_strategy(self, params_file: str = None):
        """Implementa completamente la estrategia optimizada"""
        print(f"🚀 IMPLEMENTANDO ESTRATEGIA OPTIMIZADA")
        print("=" * 60)
        
        try:
            # 1. Cargar parámetros
            params = self.load_optimized_parameters(params_file)
            
            # 2. Validar parámetros
            if not self.validate_parameters(params):
                print("❌ Parámetros no válidos para implementación")
                return False
            
            # 3. Ajustar para live trading
            safe_params = self.adjust_parameters_for_live(params)
            
            # 4. Validación final
            validation = self.run_final_validation(safe_params)
            if not validation['success']:
                print(f"❌ Validación fallida: {validation['error']}")
                return False
            
            print(f"✅ Validación exitosa - Win Rate: {validation['validation_win_rate']:.1f}%")
            
            # 5. Crear archivos de implementación
            strategy_file = self.create_optimized_strategy_class(safe_params)
            config_file = self.create_live_trading_config(safe_params)
            
            # 6. Resumen final
            print(f"\n🎉 IMPLEMENTACIÓN COMPLETADA")
            print("=" * 50)
            print(f"📁 Archivos creados:")
            print(f"   🐍 Estrategia: {strategy_file}")
            print(f"   ⚙️ Configuración: {config_file}")
            
            print(f"\n📊 Métricas de validación:")
            print(f"   🎯 Win Rate: {validation['validation_win_rate']:.1f}%")
            print(f"   📈 Señales: {validation['signal_count']}")
            print(f"   💼 Trades: {validation['trade_count']}")
            
            print(f"\n🚀 PRÓXIMOS PASOS:")
            print(f"   1. Ejecutar: python {strategy_file}")
            print(f"   2. Verificar resultados en demo")
            print(f"   3. Si satisfactorio, activar live trading")
            print(f"   4. Monitorear rendimiento las primeras 24h")
            
            return True
            
        except Exception as e:
            print(f"❌ Error en implementación: {e}")
            return False

def main():
    """Función principal del implementador"""
    print(f"🎯 IMPLEMENTADOR DE ESTRATEGIA OPTIMIZADA")
    print(f"Convierte parámetros optimizados en estrategia funcional")
    print("=" * 70)
    
    implementer = OptimizedStrategyImplementer()
    
    # Configurar para máxima seguridad
    implementer.implementation_config.update({
        'live_trading': False,  # Comenzar en demo
        'max_risk_per_trade': 0.01,  # 1% máximo
        'monitoring_enabled': True
    })
    
    success = implementer.implement_strategy()
    
    if success:
        print(f"\n✅ ¡ESTRATEGIA IMPLEMENTADA EXITOSAMENTE!")
        print(f"El bot optimizado está listo para trading")
    else:
        print(f"\n❌ Error en la implementación")
        print(f"Revisa los logs y parámetros")

if __name__ == "__main__":
    main() 