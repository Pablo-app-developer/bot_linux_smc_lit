#!/usr/bin/env python3
"""
OPTIMIZADOR BAYESIANO AVANZADO
Sistema de optimización bayesiana con Gaussian Process
Complementa al optimizador genético para máximo rendimiento
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
import json
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
import random
from scipy.optimize import minimize
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern, RBF, ConstantKernel
from scipy.stats import norm
import matplotlib.pyplot as plt
warnings.filterwarnings('ignore')

# Configurar path
sys.path.append('src')

from src.mt5_connector import MT5Connector
from src.features import SMCFeatureExtractor  
from src.strategy import SMCStrategy
from src.backtester_realistic import RealisticBacktester

@dataclass
class BayesianConfig:
    """Configuración para optimización bayesiana"""
    n_initial_points: int = 20
    n_iterations: int = 100
    acquisition_function: str = 'EI'  # Expected Improvement
    exploration_weight: float = 0.01
    target_win_rate: float = 78.0
    reward_weights: Dict[str, float] = None
    
    def __post_init__(self):
        if self.reward_weights is None:
            self.reward_weights = {
                'win_rate': 0.35,
                'profit_factor': 0.25,
                'sharpe_ratio': 0.15,
                'max_drawdown': 0.10,
                'consistency': 0.10,
                'trade_frequency': 0.05
            }

class MultiObjectiveRewardSystem:
    """
    Sistema de recompensas multi-objetivo avanzado
    """
    
    def __init__(self, weights: Dict[str, float], target_metrics: Dict[str, float] = None):
        self.weights = weights
        self.target_metrics = target_metrics or {
            'win_rate': 75.0,
            'profit_factor': 2.5,
            'sharpe_ratio': 1.5,
            'max_drawdown': 0.15,
            'consistency': 0.8,
            'trade_frequency': 1.0
        }
        
        # Métricas de performance histórica
        self.performance_history = []
        
    def calculate_multi_objective_reward(self, results: Dict) -> Dict[str, float]:
        """
        Calcula recompensas multi-objetivo con sistema profesional
        """
        if not results or not results.get('trades'):
            return {'total_reward': 0.0, 'metrics': {}}
        
        trades_df = pd.DataFrame(results['trades'])
        
        if len(trades_df) < 5:
            return {'total_reward': 0.0, 'metrics': {}}
        
        metrics = {}
        rewards = {}
        
        # 1. Win Rate Reward
        win_rate = (trades_df['was_profitable'].sum() / len(trades_df)) * 100
        metrics['win_rate'] = win_rate
        
        # Recompensa escalonada con bonificaciones
        if win_rate >= 85:
            rewards['win_rate'] = 1.5  # Bonus excepcional
        elif win_rate >= 80:
            rewards['win_rate'] = 1.3  # Excelente
        elif win_rate >= 75:
            rewards['win_rate'] = 1.1  # Muy bueno
        elif win_rate >= 70:
            rewards['win_rate'] = 1.0  # Bueno
        elif win_rate >= 60:
            rewards['win_rate'] = 0.8  # Aceptable
        else:
            rewards['win_rate'] = max(win_rate / 70.0, 0.2)  # Proporcional con mínimo
        
        # 2. Profit Factor Reward
        winners = trades_df[trades_df['was_profitable'] == True]['pnl'].sum()
        losers = abs(trades_df[trades_df['was_profitable'] == False]['pnl'].sum())
        profit_factor = winners / losers if losers > 0 else 5.0
        metrics['profit_factor'] = profit_factor
        
        if profit_factor >= 4.0:
            rewards['profit_factor'] = 1.4
        elif profit_factor >= 3.0:
            rewards['profit_factor'] = 1.2
        elif profit_factor >= 2.5:
            rewards['profit_factor'] = 1.0
        elif profit_factor >= 2.0:
            rewards['profit_factor'] = 0.8
        else:
            rewards['profit_factor'] = max(profit_factor / 2.5, 0.3)
        
        # 3. Sharpe Ratio Reward
        returns = trades_df['pnl'].values
        if len(returns) > 1 and np.std(returns) > 0:
            sharpe = np.mean(returns) / np.std(returns)
            metrics['sharpe_ratio'] = sharpe
            
            if sharpe >= 2.0:
                rewards['sharpe_ratio'] = 1.3
            elif sharpe >= 1.5:
                rewards['sharpe_ratio'] = 1.1
            elif sharpe >= 1.0:
                rewards['sharpe_ratio'] = 1.0
            elif sharpe >= 0.5:
                rewards['sharpe_ratio'] = 0.8
            else:
                rewards['sharpe_ratio'] = max(sharpe / 1.0, 0.2)
        else:
            rewards['sharpe_ratio'] = 0.5
            metrics['sharpe_ratio'] = 0.0
        
        # 4. Max Drawdown Reward (invertido)
        cumulative_pnl = trades_df['pnl'].cumsum()
        running_max = cumulative_pnl.expanding().max()
        drawdown = (cumulative_pnl - running_max) / running_max.abs()
        max_drawdown = abs(drawdown.min()) if len(drawdown) > 0 else 0
        metrics['max_drawdown'] = max_drawdown
        
        if max_drawdown <= 0.05:  # 5%
            rewards['max_drawdown'] = 1.4
        elif max_drawdown <= 0.10:  # 10%
            rewards['max_drawdown'] = 1.2
        elif max_drawdown <= 0.15:  # 15%
            rewards['max_drawdown'] = 1.0
        elif max_drawdown <= 0.25:  # 25%
            rewards['max_drawdown'] = 0.6
        else:
            rewards['max_drawdown'] = max(1 - max_drawdown, 0.1)
        
        # 5. Consistency Reward
        if len(returns) > 3:
            # Coeficiente de variación invertido
            cv = np.std(returns) / abs(np.mean(returns)) if np.mean(returns) != 0 else 10
            consistency = 1 / (1 + cv)
            metrics['consistency'] = consistency
            
            if consistency >= 0.8:
                rewards['consistency'] = 1.3
            elif consistency >= 0.6:
                rewards['consistency'] = 1.1
            elif consistency >= 0.4:
                rewards['consistency'] = 1.0
            else:
                rewards['consistency'] = max(consistency / 0.4, 0.3)
        else:
            rewards['consistency'] = 0.5
            metrics['consistency'] = 0.0
        
        # 6. Trade Frequency Reward
        if len(trades_df) > 0:
            first_trade = pd.to_datetime(trades_df['timestamp'].iloc[0])
            last_trade = pd.to_datetime(trades_df['timestamp'].iloc[-1])
            days = max((last_trade - first_trade).days, 1)
            trade_frequency = len(trades_df) / days
            metrics['trade_frequency'] = trade_frequency
            
            # Frecuencia óptima: 0.5-2.0 trades por día
            if 0.5 <= trade_frequency <= 2.0:
                rewards['trade_frequency'] = 1.0
            elif 0.2 <= trade_frequency < 0.5:
                rewards['trade_frequency'] = 0.8
            elif 2.0 < trade_frequency <= 4.0:
                rewards['trade_frequency'] = 0.9
            else:
                rewards['trade_frequency'] = 0.5
        else:
            rewards['trade_frequency'] = 0.0
            metrics['trade_frequency'] = 0.0
        
        # Calcular recompensa total ponderada
        total_reward = sum(self.weights[metric] * rewards[metric] 
                          for metric in self.weights.keys())
        
        # Bonus por superar múltiples targets simultáneamente
        targets_met = 0
        if win_rate >= 75: targets_met += 1
        if profit_factor >= 2.5: targets_met += 1
        if metrics['sharpe_ratio'] >= 1.0: targets_met += 1
        if max_drawdown <= 0.15: targets_met += 1
        if metrics['consistency'] >= 0.6: targets_met += 1
        
        # Multiplicador por targets alcanzados
        if targets_met >= 4:
            total_reward *= 1.3  # Bonus excepcional
        elif targets_met >= 3:
            total_reward *= 1.2  # Bonus muy bueno
        elif targets_met >= 2:
            total_reward *= 1.1  # Bonus bueno
        
        # Penalty por performance muy baja
        if win_rate < 40 or profit_factor < 1.0:
            total_reward *= 0.5
        
        return {
            'total_reward': total_reward,
            'metrics': metrics,
            'individual_rewards': rewards,
            'targets_met': targets_met
        }
    
    def update_performance_history(self, results: Dict):
        """Actualiza historial de performance"""
        reward_data = self.calculate_multi_objective_reward(results)
        self.performance_history.append({
            'timestamp': datetime.now(),
            'reward': reward_data['total_reward'],
            'metrics': reward_data['metrics']
        })

class BayesianOptimizer:
    """
    Optimizador bayesiano con Gaussian Process
    """
    
    def __init__(self, config: BayesianConfig):
        self.config = config
        self.reward_system = MultiObjectiveRewardSystem(config.reward_weights)
        
        # Gaussian Process
        kernel = ConstantKernel(1.0) * Matern(length_scale=1.0, nu=2.5)
        self.gp = GaussianProcessRegressor(
            kernel=kernel,
            alpha=1e-6,
            normalize_y=True,
            n_restarts_optimizer=10,
            random_state=42
        )
        
        # Espacio de parámetros
        self.param_bounds = {
            'swing_length': (2, 8),
            'ob_strength': (1, 3),
            'liq_threshold': (0.0003, 0.002),
            'fvg_min_size': (0.0002, 0.001),
            'risk_per_trade': (0.005, 0.03),
            'rsi_period': (10, 20),
            'rsi_overbought': (65, 80),
            'rsi_oversold': (20, 35),
            'atr_period': (10, 20),
            'atr_multiplier': (1.0, 3.0),
            'ema_short': (12, 30),
            'ema_long': (40, 70),
            'sl_probability': (0.25, 0.5),
            'tp_probability': (0.5, 0.8)
        }
        
        # Historia de optimización
        self.X_observed = []
        self.y_observed = []
        self.iteration_history = []
        
    def generate_initial_points(self, n_points: int) -> List[Dict]:
        """Genera puntos iniciales aleatorios"""
        points = []
        for _ in range(n_points):
            point = {}
            for param, (min_val, max_val) in self.param_bounds.items():
                if param in ['swing_length', 'ob_strength', 'rsi_period', 'atr_period', 'ema_short', 'ema_long']:
                    point[param] = random.randint(int(min_val), int(max_val))
                else:
                    point[param] = random.uniform(min_val, max_val)
            points.append(point)
        return points
    
    def params_to_vector(self, params: Dict) -> np.ndarray:
        """Convierte parámetros a vector numérico"""
        vector = []
        for param in self.param_bounds.keys():
            vector.append(params[param])
        return np.array(vector)
    
    def vector_to_params(self, vector: np.ndarray) -> Dict:
        """Convierte vector a parámetros"""
        params = {}
        for i, param in enumerate(self.param_bounds.keys()):
            if param in ['swing_length', 'ob_strength', 'rsi_period', 'atr_period', 'ema_short', 'ema_long']:
                params[param] = int(round(vector[i]))
            else:
                params[param] = vector[i]
        return params
    
    def expected_improvement(self, X: np.ndarray, gp: GaussianProcessRegressor, 
                           y_best: float, xi: float = 0.01) -> np.ndarray:
        """Calcula Expected Improvement"""
        mu, sigma = gp.predict(X, return_std=True)
        mu = mu.reshape(-1, 1)
        
        with np.errstate(divide='warn'):
            imp = mu - y_best - xi
            Z = imp / sigma.reshape(-1, 1)
            ei = imp * norm.cdf(Z) + sigma.reshape(-1, 1) * norm.pdf(Z)
            ei[sigma == 0.0] = 0.0
        
        return ei.flatten()
    
    def acquire_next_point(self) -> Dict:
        """Encuentra el siguiente punto a evaluar usando acquisition function"""
        if len(self.X_observed) < 2:
            # Puntos aleatorios si no hay suficientes datos
            return self.generate_initial_points(1)[0]
        
        # Entrenar GP
        X_train = np.array(self.X_observed)
        y_train = np.array(self.y_observed)
        self.gp.fit(X_train, y_train)
        
        y_best = np.max(y_train)
        
        # Optimizar acquisition function
        def neg_ei(x):
            x_reshaped = x.reshape(1, -1)
            return -self.expected_improvement(x_reshaped, self.gp, y_best, self.config.exploration_weight)[0]
        
        # Bounds para scipy.optimize
        bounds = [(min_val, max_val) for min_val, max_val in self.param_bounds.values()]
        
        # Múltiples puntos de inicio aleatorios
        best_x = None
        best_ei = float('inf')
        
        for _ in range(20):  # 20 intentos
            x0 = np.array([random.uniform(min_val, max_val) for min_val, max_val in self.param_bounds.values()])
            
            try:
                result = minimize(neg_ei, x0, bounds=bounds, method='L-BFGS-B')
                if result.fun < best_ei:
                    best_ei = result.fun
                    best_x = result.x
            except:
                continue
        
        if best_x is None:
            # Fallback a punto aleatorio
            return self.generate_initial_points(1)[0]
        
        return self.vector_to_params(best_x)
    
    def evaluate_params(self, params: Dict, market_data: pd.DataFrame) -> float:
        """Evalúa parámetros usando el sistema de recompensas"""
        try:
            # Crear features
            extractor = SMCFeatureExtractor(market_data)
            extractor.swing_length = int(params['swing_length'])
            df_features = extractor.extract_all()
            
            # Añadir indicadores técnicos
            df_features = self.add_technical_indicators(df_features, params)
            
            # Crear estrategia
            strategy = SMCStrategy(df_features)
            strategy.swing_length = int(params['swing_length'])
            strategy.ob_strength = int(params['ob_strength'])
            strategy.liq_threshold = params['liq_threshold']
            strategy.fvg_min_size = params['fvg_min_size']
            
            df_signals = strategy.run()
            
            # Aplicar filtros
            df_filtered = self.apply_filters(df_signals, params)
            
            # Backtesting
            backtester = RealisticBacktester(
                df_filtered,
                initial_balance=10000,
                risk_per_trade=params['risk_per_trade'],
                commission=0.00007
            )
            
            backtester.sl_probability = params['sl_probability']
            backtester.tp_probability = params['tp_probability']
            
            results = backtester.run()
            
            # Calcular recompensa multi-objetivo
            reward_data = self.reward_system.calculate_multi_objective_reward(results)
            
            return reward_data['total_reward']
            
        except Exception as e:
            print(f"⚠️ Error evaluando parámetros: {e}")
            return 0.0
    
    def add_technical_indicators(self, df: pd.DataFrame, params: Dict) -> pd.DataFrame:
        """Añade indicadores técnicos"""
        df_copy = df.copy()
        
        # RSI
        df_copy['rsi'] = self.calculate_rsi(df_copy['close'], int(params['rsi_period']))
        
        # ATR
        df_copy['atr'] = self.calculate_atr(df_copy, int(params['atr_period']))
        
        # EMAs
        df_copy['ema_short'] = df_copy['close'].ewm(span=int(params['ema_short'])).mean()
        df_copy['ema_long'] = df_copy['close'].ewm(span=int(params['ema_long'])).mean()
        df_copy['trend_bullish'] = df_copy['ema_short'] > df_copy['ema_long']
        
        return df_copy
    
    def calculate_rsi(self, prices, period):
        """Calcula RSI"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))
    
    def calculate_atr(self, df, period):
        """Calcula ATR"""
        high_low = df['high'] - df['low']
        high_close = np.abs(df['high'] - df['close'].shift())
        low_close = np.abs(df['low'] - df['close'].shift())
        true_range = np.maximum(high_low, np.maximum(high_close, low_close))
        return true_range.rolling(window=period).mean()
    
    def apply_filters(self, df_signals: pd.DataFrame, params: Dict) -> pd.DataFrame:
        """Aplica filtros según parámetros"""
        df_filtered = df_signals.copy()
        
        for i in range(len(df_filtered)):
            if df_filtered['signal'].iloc[i] != 0:
                
                # Filtro de tendencia
                if df_filtered['signal'].iloc[i] == 1 and not df_filtered.get('trend_bullish', True).iloc[i]:
                    df_filtered.at[df_filtered.index[i], 'signal'] = 0
                    continue
                elif df_filtered['signal'].iloc[i] == -1 and df_filtered.get('trend_bullish', False).iloc[i]:
                    df_filtered.at[df_filtered.index[i], 'signal'] = 0
                    continue
                
                # Filtro RSI
                rsi = df_filtered.get('rsi', 50).iloc[i]
                if rsi > params['rsi_overbought'] or rsi < params['rsi_oversold']:
                    df_filtered.at[df_filtered.index[i], 'signal'] = 0
                    continue
                
                # Filtro de volatilidad
                atr = df_filtered.get('atr', 0.001).iloc[i]
                atr_avg = df_filtered.get('atr', pd.Series([0.001]*len(df_filtered))).iloc[max(0,i-20):i].mean()
                if atr > atr_avg * params['atr_multiplier']:
                    df_filtered.at[df_filtered.index[i], 'signal'] = 0
                    continue
        
        return df_filtered
    
    def optimize(self, market_data: pd.DataFrame):
        """Ejecuta optimización bayesiana"""
        print(f"\n🔬 INICIANDO OPTIMIZACIÓN BAYESIANA")
        print(f"Puntos iniciales: {self.config.n_initial_points}")
        print(f"Iteraciones: {self.config.n_iterations}")
        print(f"Función de adquisición: {self.config.acquisition_function}")
        print("=" * 60)
        
        # Generar puntos iniciales
        print(f"🎲 Generando {self.config.n_initial_points} puntos iniciales...")
        initial_points = self.generate_initial_points(self.config.n_initial_points)
        
        # Evaluar puntos iniciales
        for i, params in enumerate(initial_points):
            print(f"   Evaluando punto inicial {i+1}/{len(initial_points)}")
            reward = self.evaluate_params(params, market_data)
            
            self.X_observed.append(self.params_to_vector(params))
            self.y_observed.append(reward)
            
            self.iteration_history.append({
                'iteration': i,
                'params': params,
                'reward': reward,
                'type': 'initial'
            })
        
        best_reward = max(self.y_observed)
        best_idx = np.argmax(self.y_observed)
        best_params = self.vector_to_params(self.X_observed[best_idx])
        
        print(f"   🎯 Mejor recompensa inicial: {best_reward:.4f}")
        
        # Iteraciones bayesianas
        for iteration in range(self.config.n_iterations):
            print(f"\n🔄 Iteración Bayesiana {iteration + 1}/{self.config.n_iterations}")
            
            # Encontrar siguiente punto
            next_params = self.acquire_next_point()
            
            # Evaluar
            reward = self.evaluate_params(next_params, market_data)
            
            # Actualizar
            self.X_observed.append(self.params_to_vector(next_params))
            self.y_observed.append(reward)
            
            # Actualizar mejor resultado
            if reward > best_reward:
                best_reward = reward
                best_params = next_params
                print(f"   🎉 Nueva mejor recompensa: {best_reward:.4f}")
            
            self.iteration_history.append({
                'iteration': len(initial_points) + iteration,
                'params': next_params,
                'reward': reward,
                'type': 'bayesian'
            })
            
            print(f"   📊 Recompensa: {reward:.4f} (Mejor: {best_reward:.4f})")
        
        print(f"\n✅ Optimización bayesiana completada")
        print(f"🏆 Mejor recompensa final: {best_reward:.4f}")
        
        return best_params, best_reward
    
    def save_results(self, best_params: Dict, best_reward: float):
        """Guarda resultados de optimización bayesiana"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        results = {
            'timestamp': timestamp,
            'best_reward': best_reward,
            'best_parameters': best_params,
            'config': {
                'n_initial_points': self.config.n_initial_points,
                'n_iterations': self.config.n_iterations,
                'target_win_rate': self.config.target_win_rate,
                'reward_weights': self.config.reward_weights
            },
            'iteration_history': self.iteration_history,
            'all_rewards': self.y_observed
        }
        
        filename = f"bayesian_optimization_results_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        
        print(f"💾 Resultados bayesianos guardados en: {filename}")
        return filename

def run_bayesian_optimization():
    """Ejecuta optimización bayesiana standalone"""
    print(f"🔬 SISTEMA DE OPTIMIZACIÓN BAYESIANA")
    print(f"Método: Gaussian Process + Expected Improvement")
    print(f"Objetivo: Máximo rendimiento multi-objetivo")
    print("=" * 60)
    
    # Configuración
    config = BayesianConfig(
        n_initial_points=25,
        n_iterations=80,
        target_win_rate=80.0,
        exploration_weight=0.02
    )
    
    # Optimizador
    optimizer = BayesianOptimizer(config)
    
    # Datos de mercado
    print(f"📊 Obteniendo datos de mercado...")
    connector = MT5Connector(symbol='EURUSD', timeframe='H1')
    market_data = connector.fetch_ohlc_data(num_candles=3000)
    
    if market_data is None or len(market_data) < 1000:
        print("❌ Error: Datos insuficientes")
        return
    
    print(f"✅ {len(market_data)} velas obtenidas")
    
    # Ejecutar optimización
    best_params, best_reward = optimizer.optimize(market_data)
    
    # Análisis final
    print(f"\n🏆 ANÁLISIS FINAL BAYESIANO")
    print("=" * 50)
    
    print(f"📊 MEJORES PARÁMETROS:")
    for key, value in best_params.items():
        if isinstance(value, float):
            print(f"   {key}: {value:.6f}")
        else:
            print(f"   {key}: {value}")
    
    print(f"\n🎯 MÉTRICAS:")
    print(f"   🔥 Recompensa Máxima: {best_reward:.4f}")
    
    estimated_win_rate = min(best_reward * 75, 95)
    print(f"   📈 Win Rate Estimado: {estimated_win_rate:.1f}%")
    
    # Guardar resultados
    optimizer.save_results(best_params, best_reward)
    
    return best_params, best_reward

if __name__ == "__main__":
    run_bayesian_optimization() 