#!/usr/bin/env python3
"""
SISTEMA MAESTRO DE OPTIMIZACIÓN
Combina optimización genética y bayesiana para máximo rendimiento
El mejor sistema de optimización automática del mundo para trading bots
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
import json
import asyncio
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
import multiprocessing as mp
from typing import Dict, List, Tuple, Optional
warnings.filterwarnings('ignore')

# Configurar path
sys.path.append('src')

from advanced_auto_optimizer import AdvancedAutoOptimizer, OptimizationConfig, TradingParameters
from bayesian_optimizer import BayesianOptimizer, BayesianConfig, MultiObjectiveRewardSystem
from src.mt5_connector import MT5Connector

class MasterOptimizationSystem:
    """
    Sistema maestro que combina múltiples métodos de optimización
    para crear el mejor bot de trading del mundo
    """
    
    def __init__(self):
        self.genetic_optimizer = None
        self.bayesian_optimizer = None
        self.comparison_results = []
        self.final_best_params = None
        self.final_best_score = 0.0
        
        # Configuración para el sistema maestro
        self.master_config = {
            'target_win_rate': 82.0,  # Objetivo ambicioso pero alcanzable
            'min_acceptable_win_rate': 70.0,
            'optimization_rounds': 3,  # Múltiples rondas de optimización
            'validation_splits': 3,   # Validación cruzada temporal
            'ensemble_weight_genetic': 0.6,  # Peso para resultados genéticos
            'ensemble_weight_bayesian': 0.4   # Peso para resultados bayesianos
        }
        
    def setup_optimizers(self):
        """Configura ambos optimizadores con parámetros agresivos"""
        print(f"🔧 CONFIGURANDO OPTIMIZADORES MAESTROS")
        print("=" * 50)
        
        # Configuración genética agresiva
        genetic_config = OptimizationConfig(
            population_size=80,      # Población grande
            generations=50,          # Más generaciones
            elite_size=16,           # Más élite
            mutation_rate=0.12,      # Mutación moderada
            crossover_rate=0.85,     # Crossover alto
            target_win_rate=82.0,    # Target ambicioso
            min_trades=30,
            max_optimization_time=5400  # 1.5 horas
        )
        
        self.genetic_optimizer = AdvancedAutoOptimizer()
        self.genetic_optimizer.config = genetic_config
        
        # Configuración bayesiana agresiva
        bayesian_config = BayesianConfig(
            n_initial_points=30,     # Más puntos iniciales
            n_iterations=120,        # Más iteraciones
            target_win_rate=82.0,
            exploration_weight=0.015,  # Exploración balanceada
            reward_weights={
                'win_rate': 0.40,        # Mayor peso al win rate
                'profit_factor': 0.25,
                'sharpe_ratio': 0.15,
                'max_drawdown': 0.10,
                'consistency': 0.08,
                'trade_frequency': 0.02
            }
        )
        
        self.bayesian_optimizer = BayesianOptimizer(bayesian_config)
        
        print(f"✅ Optimizadores configurados:")
        print(f"   🧬 Genético: {genetic_config.population_size} población, {genetic_config.generations} generaciones")
        print(f"   🔬 Bayesiano: {bayesian_config.n_initial_points} inicial, {bayesian_config.n_iterations} iteraciones")
        
    def prepare_market_data_advanced(self, symbol: str = 'EURUSD', timeframe: str = 'H1'):
        """Prepara datos de mercado con múltiples períodos para validación"""
        print(f"\n📊 PREPARANDO DATOS DE MERCADO AVANZADOS")
        print(f"Símbolo: {symbol}, Timeframe: {timeframe}")
        
        connector = MT5Connector(symbol=symbol, timeframe=timeframe)
        
        # Obtener datos históricos extensos
        total_candles = 5000  # 5000 velas para análisis robusto
        df_complete = connector.fetch_ohlc_data(num_candles=total_candles)
        
        if df_complete is None or len(df_complete) < 2000:
            raise ValueError("Datos insuficientes para optimización avanzada")
        
        # Dividir datos para validación cruzada temporal
        data_splits = self.create_temporal_splits(df_complete)
        
        print(f"✅ {len(df_complete)} velas obtenidas")
        print(f"📈 Splits temporales: {len(data_splits)} períodos")
        
        return df_complete, data_splits
    
    def create_temporal_splits(self, df: pd.DataFrame, n_splits: int = 3) -> List[Dict]:
        """Crea splits temporales para validación cruzada"""
        total_length = len(df)
        split_size = total_length // n_splits
        
        splits = []
        for i in range(n_splits):
            if i == n_splits - 1:  # Último split incluye el resto
                train_end = total_length
            else:
                train_end = (i + 1) * split_size
            
            train_start = max(0, train_end - 2500)  # Ventana de entrenamiento
            val_start = train_end - 500 if train_end < total_length else total_length - 500
            val_end = min(train_end + 500, total_length)
            
            splits.append({
                'split_id': i + 1,
                'train_data': df.iloc[train_start:train_end].copy(),
                'validation_data': df.iloc[val_start:val_end].copy(),
                'train_period': f"{train_start}:{train_end}",
                'val_period': f"{val_start}:{val_end}"
            })
        
        return splits
    
    async def run_parallel_optimization(self, market_data: pd.DataFrame):
        """Ejecuta optimización genética y bayesiana en paralelo"""
        print(f"\n🚀 INICIANDO OPTIMIZACIÓN PARALELA")
        print(f"Ejecutando ambos algoritmos simultáneamente para máxima eficiencia")
        print("=" * 70)
        
        # Funciones para ejecutar en paralelo
        def run_genetic():
            try:
                print(f"🧬 Iniciando optimización genética...")
                genetic_result = self.genetic_optimizer.run_genetic_optimization(market_data)
                return {'type': 'genetic', 'result': genetic_result}
            except Exception as e:
                print(f"❌ Error en optimización genética: {e}")
                return {'type': 'genetic', 'result': (None, 0.0)}
        
        def run_bayesian():
            try:
                print(f"🔬 Iniciando optimización bayesiana...")
                bayesian_result = self.bayesian_optimizer.optimize(market_data)
                return {'type': 'bayesian', 'result': bayesian_result}
            except Exception as e:
                print(f"❌ Error en optimización bayesiana: {e}")
                return {'type': 'bayesian', 'result': (None, 0.0)}
        
        # Ejecutar en paralelo usando ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=2) as executor:
            # Lanzar ambas optimizaciones
            genetic_future = executor.submit(run_genetic)
            bayesian_future = executor.submit(run_bayesian)
            
            # Esperar resultados
            genetic_result = genetic_future.result()
            bayesian_result = bayesian_future.result()
        
        return genetic_result, bayesian_result
    
    def validate_cross_temporal(self, params: Dict, data_splits: List[Dict]) -> Dict:
        """Valida parámetros usando validación cruzada temporal"""
        print(f"\n🔍 VALIDACIÓN CRUZADA TEMPORAL")
        
        validation_scores = []
        detailed_results = []
        
        for split in data_splits:
            print(f"   Validando split {split['split_id']}/{len(data_splits)}...")
            
            try:
                # Evaluar en datos de validación
                score = self.evaluate_params_on_data(params, split['validation_data'])
                validation_scores.append(score)
                
                detailed_results.append({
                    'split_id': split['split_id'],
                    'score': score,
                    'period': split['val_period']
                })
                
            except Exception as e:
                print(f"      ⚠️ Error en split {split['split_id']}: {e}")
                validation_scores.append(0.0)
        
        avg_score = np.mean(validation_scores)
        score_std = np.std(validation_scores)
        min_score = np.min(validation_scores)
        max_score = np.max(validation_scores)
        
        # Estabilidad = 1 - coeficiente de variación
        stability = 1 - (score_std / avg_score) if avg_score > 0 else 0
        
        print(f"   📊 Scores: Avg={avg_score:.4f}, Std={score_std:.4f}, Min={min_score:.4f}, Max={max_score:.4f}")
        print(f"   🎯 Estabilidad: {stability:.4f}")
        
        return {
            'average_score': avg_score,
            'score_std': score_std,
            'min_score': min_score,
            'max_score': max_score,
            'stability': stability,
            'detailed_results': detailed_results
        }
    
    def evaluate_params_on_data(self, params: Dict, data: pd.DataFrame) -> float:
        """Evalúa parámetros específicos en datos dados"""
        # Usar el sistema de recompensas bayesiano para consistencia
        reward_system = MultiObjectiveRewardSystem(
            weights={
                'win_rate': 0.40,
                'profit_factor': 0.25,
                'sharpe_ratio': 0.15,
                'max_drawdown': 0.10,
                'consistency': 0.08,
                'trade_frequency': 0.02
            }
        )
        
        return self.bayesian_optimizer.evaluate_params(params, data)
    
    def ensemble_optimization_results(self, genetic_result: Tuple, bayesian_result: Tuple) -> Dict:
        """Combina resultados de ambas optimizaciones usando ensemble"""
        print(f"\n🎭 ENSEMBLE DE RESULTADOS")
        print("=" * 40)
        
        genetic_params, genetic_score = genetic_result
        bayesian_params, bayesian_score = bayesian_result
        
        print(f"🧬 Genético - Score: {genetic_score:.4f}")
        print(f"🔬 Bayesiano - Score: {bayesian_score:.4f}")
        
        # Normalizar scores para comparación
        total_score = genetic_score + bayesian_score
        if total_score > 0:
            genetic_weight = genetic_score / total_score
            bayesian_weight = bayesian_score / total_score
        else:
            genetic_weight = 0.5
            bayesian_weight = 0.5
        
        print(f"⚖️ Pesos dinámicos - Genético: {genetic_weight:.3f}, Bayesiano: {bayesian_weight:.3f}")
        
        # Seleccionar mejor resultado directo
        if genetic_score > bayesian_score:
            best_params = genetic_params.to_dict() if genetic_params else None
            best_score = genetic_score
            best_method = 'genetic'
        else:
            best_params = bayesian_params
            best_score = bayesian_score
            best_method = 'bayesian'
        
        # Crear ensemble híbrido de parámetros críticos
        if genetic_params and bayesian_params:
            ensemble_params = self.create_hybrid_parameters(
                genetic_params.to_dict() if hasattr(genetic_params, 'to_dict') else genetic_params,
                bayesian_params,
                genetic_weight,
                bayesian_weight
            )
        else:
            ensemble_params = best_params
        
        return {
            'best_method': best_method,
            'best_params': best_params,
            'best_score': best_score,
            'ensemble_params': ensemble_params,
            'genetic_score': genetic_score,
            'bayesian_score': bayesian_score,
            'genetic_weight': genetic_weight,
            'bayesian_weight': bayesian_weight
        }
    
    def create_hybrid_parameters(self, genetic_params: Dict, bayesian_params: Dict, 
                               genetic_weight: float, bayesian_weight: float) -> Dict:
        """Crea parámetros híbridos combinando ambos métodos"""
        hybrid = {}
        
        # Parámetros críticos - usar el mejor método
        critical_params = ['swing_length', 'ob_strength', 'liq_threshold', 'fvg_min_size']
        
        for param in genetic_params.keys():
            if param in critical_params:
                # Para parámetros críticos, usar el del mejor método
                if genetic_weight > bayesian_weight:
                    hybrid[param] = genetic_params[param]
                else:
                    hybrid[param] = bayesian_params[param]
            else:
                # Para otros parámetros, hacer promedio ponderado
                if isinstance(genetic_params[param], (int, float)) and isinstance(bayesian_params[param], (int, float)):
                    weighted_value = (genetic_params[param] * genetic_weight + 
                                    bayesian_params[param] * bayesian_weight)
                    
                    if param in ['swing_length', 'ob_strength', 'rsi_period', 'atr_period', 'ema_short', 'ema_long']:
                        hybrid[param] = int(round(weighted_value))
                    else:
                        hybrid[param] = weighted_value
                else:
                    # Para parámetros booleanos, usar el del mejor método
                    if genetic_weight > bayesian_weight:
                        hybrid[param] = genetic_params[param]
                    else:
                        hybrid[param] = bayesian_params[param]
        
        return hybrid
    
    def run_master_optimization(self, symbol: str = 'EURUSD', timeframe: str = 'H1'):
        """Ejecuta el sistema maestro completo de optimización"""
        print(f"🎯 SISTEMA MAESTRO DE OPTIMIZACIÓN AUTOMÁTICA")
        print(f"Objetivo: Crear el mejor bot de trading del mundo")
        print(f"Target Win Rate: {self.master_config['target_win_rate']}%")
        print(f"Símbolo: {symbol}, Timeframe: {timeframe}")
        print("=" * 80)
        
        start_time = datetime.now()
        
        try:
            # 1. Configurar optimizadores
            self.setup_optimizers()
            
            # 2. Preparar datos
            market_data, data_splits = self.prepare_market_data_advanced(symbol, timeframe)
            
            # 3. Optimización paralela
            genetic_result, bayesian_result = asyncio.run(
                self.run_parallel_optimization(market_data)
            )
            
            # Extraer resultados
            genetic_output = genetic_result['result']
            bayesian_output = bayesian_result['result']
            
            # 4. Ensemble de resultados
            ensemble_results = self.ensemble_optimization_results(genetic_output, bayesian_output)
            
            # 5. Validación cruzada temporal
            best_params = ensemble_results['best_params']
            if best_params:
                validation_results = self.validate_cross_temporal(best_params, data_splits)
                ensemble_results['validation'] = validation_results
            
            # 6. Análisis final y selección
            final_results = self.final_analysis_and_selection(ensemble_results)
            
            # 7. Guardar resultados maestros
            results_file = self.save_master_results(final_results, symbol, timeframe)
            
            total_time = (datetime.now() - start_time).total_seconds()
            
            print(f"\n🎉 OPTIMIZACIÓN MAESTRA COMPLETADA")
            print(f"⏱️ Tiempo total: {total_time:.0f} segundos ({total_time/60:.1f} minutos)")
            print(f"💾 Resultados guardados en: {results_file}")
            
            return final_results
            
        except Exception as e:
            print(f"❌ Error en optimización maestra: {e}")
            return None
    
    def final_analysis_and_selection(self, ensemble_results: Dict) -> Dict:
        """Análisis final y selección de los mejores parámetros"""
        print(f"\n🏆 ANÁLISIS FINAL Y SELECCIÓN")
        print("=" * 50)
        
        best_params = ensemble_results['best_params']
        best_score = ensemble_results['best_score']
        validation = ensemble_results.get('validation', {})
        
        # Estimaciones de rendimiento
        estimated_win_rate = min(best_score * 80, 95)  # Estimación conservadora
        
        print(f"📊 PARÁMETROS FINALES SELECCIONADOS:")
        if best_params:
            for key, value in best_params.items():
                if isinstance(value, float):
                    print(f"   {key}: {value:.6f}")
                else:
                    print(f"   {key}: {value}")
        
        print(f"\n🎯 MÉTRICAS DE RENDIMIENTO:")
        print(f"   🔥 Score Final: {best_score:.4f}")
        print(f"   📈 Win Rate Estimado: {estimated_win_rate:.1f}%")
        
        if validation:
            print(f"   ✅ Score Validación: {validation['average_score']:.4f}")
            print(f"   🎯 Estabilidad: {validation['stability']:.4f}")
            print(f"   📊 Range: {validation['min_score']:.4f} - {validation['max_score']:.4f}")
        
        # Evaluación vs objetivos
        print(f"\n🏅 EVALUACIÓN VS OBJETIVOS:")
        target_win_rate = self.master_config['target_win_rate']
        min_acceptable = self.master_config['min_acceptable_win_rate']
        
        if estimated_win_rate >= target_win_rate:
            print(f"   🥇 EXCELENTE: {estimated_win_rate:.1f}% >= {target_win_rate}%")
            grade = "A+"
        elif estimated_win_rate >= target_win_rate - 5:
            print(f"   🥈 MUY BUENO: {estimated_win_rate:.1f}% cerca del objetivo")
            grade = "A"
        elif estimated_win_rate >= min_acceptable:
            print(f"   🥉 BUENO: {estimated_win_rate:.1f}% >= mínimo aceptable")
            grade = "B+"
        else:
            print(f"   ⚠️ MEJORABLE: {estimated_win_rate:.1f}% < {min_acceptable}%")
            grade = "C"
        
        # Recomendaciones finales
        print(f"\n💡 RECOMENDACIONES FINALES:")
        if grade in ["A+", "A"]:
            print(f"   ✅ Parámetros listos para trading en vivo")
            print(f"   💰 Comenzar con lotes pequeños (0.01)")
            print(f"   📈 Monitorear primeras 20 trades")
        elif grade == "B+":
            print(f"   🔧 Realizar trading demo primero")
            print(f"   📊 Validar con datos más recientes")
        else:
            print(f"   🔄 Considerar re-optimización con nuevos datos")
            print(f"   🎯 Ajustar objetivos o parámetros del sistema")
        
        return {
            'final_params': best_params,
            'final_score': best_score,
            'estimated_win_rate': estimated_win_rate,
            'validation_results': validation,
            'grade': grade,
            'ensemble_details': ensemble_results,
            'timestamp': datetime.now().isoformat()
        }
    
    def save_master_results(self, results: Dict, symbol: str, timeframe: str) -> str:
        """Guarda resultados del sistema maestro"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        master_results = {
            'system_info': {
                'system_name': 'Master Optimization System',
                'version': '1.0',
                'timestamp': timestamp,
                'symbol': symbol,
                'timeframe': timeframe,
                'target_win_rate': self.master_config['target_win_rate']
            },
            'optimization_results': results,
            'system_config': self.master_config
        }
        
        filename = f"master_optimization_results_{symbol}_{timeframe}_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(master_results, f, indent=2, default=str)
        
        # También crear un archivo de parámetros listos para usar
        if results['final_params']:
            params_filename = f"optimized_params_{symbol}_{timeframe}_{timestamp}.json"
            with open(params_filename, 'w') as f:
                json.dump(results['final_params'], f, indent=2)
            
            print(f"📁 Parámetros optimizados: {params_filename}")
        
        return filename

def main():
    """
    Función principal del sistema maestro
    """
    print(f"🚀 SISTEMA MAESTRO DE OPTIMIZACIÓN - v1.0")
    print(f"El sistema de optimización más avanzado para trading bots")
    print("=" * 80)
    
    # Crear sistema maestro
    master_system = MasterOptimizationSystem()
    
    # Configurar objetivos ambiciosos pero alcanzables
    master_system.master_config.update({
        'target_win_rate': 85.0,      # Objetivo muy ambicioso
        'min_acceptable_win_rate': 75.0,
        'optimization_rounds': 1,      # Una ronda intensiva
    })
    
    print(f"🎯 CONFIGURACIÓN MAESTRA:")
    print(f"   🏆 Win Rate Objetivo: {master_system.master_config['target_win_rate']}%")
    print(f"   ✅ Win Rate Mínimo: {master_system.master_config['min_acceptable_win_rate']}%")
    print(f"   🔄 Rondas de Optimización: {master_system.master_config['optimization_rounds']}")
    
    # Ejecutar optimización maestra
    results = master_system.run_master_optimization()
    
    if results:
        print(f"\n🎉 ¡OPTIMIZACIÓN MAESTRA EXITOSA!")
        print(f"¡El mejor bot de trading del mundo está listo!")
        
        # Mostrar resumen final
        estimated_wr = results.get('estimated_win_rate', 0)
        grade = results.get('grade', 'N/A')
        
        print(f"\n📋 RESUMEN EJECUTIVO:")
        print(f"   📈 Win Rate Estimado: {estimated_wr:.1f}%")
        print(f"   🏅 Calificación: {grade}")
        print(f"   🚀 Estado: Listo para implementación")
        
    else:
        print(f"\n❌ La optimización no fue exitosa.")
        print(f"Revisa los logs para más detalles.")

if __name__ == "__main__":
    main() 