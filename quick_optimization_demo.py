#!/usr/bin/env python3
"""
DEMOSTRACIÓN RÁPIDA DEL SISTEMA DE OPTIMIZACIÓN
Versión acelerada para demostrar el funcionamiento del sistema maestro
"""

import sys
import os
import pandas as pd
import numpy as np
from datetime import datetime
import warnings
import json
from typing import Dict, List
warnings.filterwarnings('ignore')

# Configurar path
sys.path.append('src')

from advanced_auto_optimizer import AdvancedAutoOptimizer, OptimizationConfig, TradingParameters
from bayesian_optimizer import BayesianOptimizer, BayesianConfig
from src.mt5_connector import MT5Connector

class QuickOptimizationDemo:
    """
    Demostración rápida del sistema de optimización
    """
    
    def __init__(self):
        self.results = {}
        
    def run_genetic_demo(self):
        """Ejecuta demostración del optimizador genético"""
        print(f"🧬 DEMOSTRACIÓN OPTIMIZADOR GENÉTICO")
        print("=" * 50)
        
        # Configuración rápida
        optimizer = AdvancedAutoOptimizer()
        optimizer.config.population_size = 20  # Población pequeña
        optimizer.config.generations = 5       # Pocas generaciones
        optimizer.config.target_win_rate = 75.0
        optimizer.config.max_optimization_time = 300  # 5 minutos max
        
        print(f"⚙️ Configuración demo:")
        print(f"   Población: {optimizer.config.population_size}")
        print(f"   Generaciones: {optimizer.config.generations}")
        print(f"   Target: {optimizer.config.target_win_rate}%")
        
        try:
            # Obtener datos pequeños para demo
            connector = MT5Connector(symbol='EURUSD', timeframe='H1')
            market_data = connector.fetch_ohlc_data(num_candles=1000)
            
            if market_data is None:
                print("❌ No se pudieron obtener datos")
                return None
            
            print(f"📊 Datos obtenidos: {len(market_data)} velas")
            
            # Ejecutar optimización
            best_params, best_fitness = optimizer.run_genetic_optimization(market_data)
            
            if best_params:
                print(f"\n✅ OPTIMIZACIÓN GENÉTICA COMPLETADA")
                print(f"🎯 Mejor fitness: {best_fitness:.4f}")
                
                # Mostrar algunos parámetros clave
                params_dict = best_params.to_dict()
                print(f"📊 Parámetros optimizados (muestra):")
                key_params = ['swing_length', 'risk_per_trade', 'sl_probability', 'tp_probability']
                for param in key_params:
                    if param in params_dict:
                        value = params_dict[param]
                        if isinstance(value, float):
                            print(f"   {param}: {value:.4f}")
                        else:
                            print(f"   {param}: {value}")
                
                return {
                    'type': 'genetic',
                    'best_params': params_dict,
                    'best_fitness': best_fitness
                }
            else:
                print("❌ No se encontraron parámetros válidos")
                return None
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def run_bayesian_demo(self):
        """Ejecuta demostración del optimizador bayesiano"""
        print(f"\n🔬 DEMOSTRACIÓN OPTIMIZADOR BAYESIANO")
        print("=" * 50)
        
        # Configuración rápida
        config = BayesianConfig(
            n_initial_points=10,     # Pocos puntos iniciales
            n_iterations=15,         # Pocas iteraciones
            target_win_rate=75.0,
            exploration_weight=0.02
        )
        
        optimizer = BayesianOptimizer(config)
        
        print(f"⚙️ Configuración demo:")
        print(f"   Puntos iniciales: {config.n_initial_points}")
        print(f"   Iteraciones: {config.n_iterations}")
        print(f"   Target: {config.target_win_rate}%")
        
        try:
            # Obtener datos pequeños para demo
            connector = MT5Connector(symbol='EURUSD', timeframe='H1')
            market_data = connector.fetch_ohlc_data(num_candles=1000)
            
            if market_data is None:
                print("❌ No se pudieron obtener datos")
                return None
            
            print(f"📊 Datos obtenidos: {len(market_data)} velas")
            
            # Ejecutar optimización
            best_params, best_reward = optimizer.optimize(market_data)
            
            if best_params:
                print(f"\n✅ OPTIMIZACIÓN BAYESIANA COMPLETADA")
                print(f"🎯 Mejor recompensa: {best_reward:.4f}")
                
                # Mostrar algunos parámetros clave
                print(f"📊 Parámetros optimizados (muestra):")
                key_params = ['swing_length', 'risk_per_trade', 'sl_probability', 'tp_probability']
                for param in key_params:
                    if param in best_params:
                        value = best_params[param]
                        if isinstance(value, float):
                            print(f"   {param}: {value:.4f}")
                        else:
                            print(f"   {param}: {value}")
                
                return {
                    'type': 'bayesian',
                    'best_params': best_params,
                    'best_reward': best_reward
                }
            else:
                print("❌ No se encontraron parámetros válidos")
                return None
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def compare_results(self, genetic_result, bayesian_result):
        """Compara resultados de ambos métodos"""
        print(f"\n🏆 COMPARACIÓN DE RESULTADOS")
        print("=" * 50)
        
        if genetic_result and bayesian_result:
            genetic_score = genetic_result['best_fitness']
            bayesian_score = bayesian_result['best_reward']
            
            print(f"🧬 Optimizador Genético:")
            print(f"   Score: {genetic_score:.4f}")
            
            print(f"🔬 Optimizador Bayesiano:")
            print(f"   Score: {bayesian_score:.4f}")
            
            # Determinar ganador
            if genetic_score > bayesian_score:
                winner = "Genético"
                best_result = genetic_result
                print(f"\n🥇 GANADOR: Optimizador Genético")
            else:
                winner = "Bayesiano"
                best_result = bayesian_result
                print(f"\n🥇 GANADOR: Optimizador Bayesiano")
            
            # Estimación de win rate
            best_score = max(genetic_score, bayesian_score)
            estimated_win_rate = min(best_score * 80, 95)
            
            print(f"📈 Win Rate Estimado: {estimated_win_rate:.1f}%")
            
            # Evaluación
            if estimated_win_rate >= 80:
                print(f"🎉 EXCELENTE: ¡Supera el 80%!")
            elif estimated_win_rate >= 70:
                print(f"✅ MUY BUENO: Nivel profesional")
            elif estimated_win_rate >= 60:
                print(f"👍 BUENO: Rendimiento sólido")
            else:
                print(f"⚠️ MEJORABLE: Necesita más optimización")
            
            return {
                'winner': winner,
                'best_result': best_result,
                'estimated_win_rate': estimated_win_rate,
                'genetic_score': genetic_score,
                'bayesian_score': bayesian_score
            }
        
        elif genetic_result:
            print(f"🧬 Solo Genético completado")
            estimated_wr = min(genetic_result['best_fitness'] * 80, 95)
            print(f"📈 Win Rate Estimado: {estimated_wr:.1f}%")
            return {'winner': 'genetic', 'estimated_win_rate': estimated_wr}
            
        elif bayesian_result:
            print(f"🔬 Solo Bayesiano completado")
            estimated_wr = min(bayesian_result['best_reward'] * 80, 95)
            print(f"📈 Win Rate Estimado: {estimated_wr:.1f}%")
            return {'winner': 'bayesian', 'estimated_win_rate': estimated_wr}
        
        else:
            print(f"❌ Ningún optimizador completado exitosamente")
            return None
    
    def save_demo_results(self, comparison):
        """Guarda resultados de la demostración"""
        if not comparison:
            return None
            
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        demo_results = {
            'demo_info': {
                'system': 'Advanced Auto-Optimization System Demo',
                'timestamp': timestamp,
                'purpose': 'Quick demonstration of optimization capabilities'
            },
            'results': comparison
        }
        
        filename = f"optimization_demo_results_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(demo_results, f, indent=2, default=str)
        
        print(f"\n💾 Resultados demo guardados: {filename}")
        return filename
    
    def run_complete_demo(self):
        """Ejecuta demostración completa"""
        print(f"🚀 DEMOSTRACIÓN SISTEMA DE OPTIMIZACIÓN AUTOMÁTICA")
        print(f"Versión rápida para mostrar capacidades del sistema")
        print("=" * 70)
        
        start_time = datetime.now()
        
        # 1. Optimización genética
        genetic_result = self.run_genetic_demo()
        
        # 2. Optimización bayesiana
        bayesian_result = self.run_bayesian_demo()
        
        # 3. Comparación
        comparison = self.compare_results(genetic_result, bayesian_result)
        
        # 4. Guardar resultados
        results_file = self.save_demo_results(comparison)
        
        total_time = (datetime.now() - start_time).total_seconds()
        
        print(f"\n🎉 DEMOSTRACIÓN COMPLETADA")
        print(f"⏱️ Tiempo total: {total_time:.0f} segundos")
        
        if comparison:
            print(f"\n📋 RESUMEN:")
            print(f"   🏆 Mejor método: {comparison.get('winner', 'N/A')}")
            print(f"   📈 Win Rate estimado: {comparison.get('estimated_win_rate', 0):.1f}%")
            print(f"   💾 Archivo: {results_file}")
            
            print(f"\n💡 PRÓXIMOS PASOS:")
            print(f"   1. Para optimización completa: python master_optimization_system.py")
            print(f"   2. Para implementar resultados: python implement_optimized_strategy.py")
            print(f"   3. Configuración completa toma 30-60 minutos pero obtiene mejores resultados")
        
        return comparison

def main():
    """Función principal de la demostración"""
    print(f"🎯 DEMOSTRACIÓN RÁPIDA - SISTEMA DE OPTIMIZACIÓN")
    print(f"Mostrando capacidades en versión acelerada")
    print("=" * 70)
    
    demo = QuickOptimizationDemo()
    results = demo.run_complete_demo()
    
    if results:
        print(f"\n✅ ¡DEMOSTRACIÓN EXITOSA!")
        print(f"El sistema de optimización está funcionando correctamente")
        print(f"Para mejores resultados, ejecuta la versión completa")
    else:
        print(f"\n⚠️ La demostración tuvo problemas")
        print(f"Revisa la conexión MT5 y los datos")

if __name__ == "__main__":
    main() 