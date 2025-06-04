#!/usr/bin/env python3
"""
SISTEMA DE MACHINE LEARNING AVANZADO - BOT SMC-LIT
=================================================
Aprendizaje automático para optimización de trading
"""

import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional
import os
from dataclasses import dataclass
import pickle

@dataclass
class MarketFeatures:
    """Estructura para características del mercado"""
    timestamp: datetime
    sentiment_score: float
    volatility: float
    volume: float
    price_change: float
    news_impact: float
    category_scores: Dict[str, float]
    technical_indicators: Dict[str, float]

@dataclass
class TradingOutcome:
    """Estructura para resultados de trading"""
    timestamp: datetime
    symbol: str
    direction: str
    entry_price: float
    exit_price: float
    profit_loss: float
    success: bool
    market_conditions: MarketFeatures

class AdvancedMLTradingSystem:
    def __init__(self):
        self.model_data = {
            'features': [],
            'outcomes': [],
            'learning_rate': 0.01,
            'accuracy': 0.5,
            'total_predictions': 0,
            'correct_predictions': 0
        }
        
        # Configuración de aprendizaje
        self.config = {
            'min_data_points': 10,
            'retrain_frequency': 50,
            'feature_importance_threshold': 0.1,
            'confidence_threshold': 0.6
        }
        
        # Características técnicas para análisis
        self.technical_features = [
            'rsi', 'macd', 'bollinger_bands', 'moving_average_5',
            'moving_average_20', 'volume_trend', 'price_momentum',
            'support_resistance', 'fibonacci_levels'
        ]
        
        # Pesos iniciales para modelo simple
        self.feature_weights = {
            'sentiment_score': 0.25,
            'volatility': 0.15,
            'volume': 0.10,
            'price_change': 0.20,
            'news_impact': 0.15,
            'technical_score': 0.15
        }
        
        self.prediction_history = []
        self.performance_metrics = {
            'daily_accuracy': [],
            'weekly_accuracy': [],
            'category_performance': {},
            'best_conditions': {},
            'worst_conditions': {}
        }
        
    def extract_market_features(self, market_data: Dict, news_analysis: Dict) -> MarketFeatures:
        """Extraer características del mercado para ML"""
        
        # Características de noticias
        sentiment_score = news_analysis.get('impacto', {}).get('confianza_general', 0.5)
        news_impact = self.calculate_news_impact(news_analysis)
        
        # Características de mercado (simuladas pero realistas)
        volatility = np.random.uniform(0.1, 2.0)
        volume = np.random.uniform(0.5, 3.0)
        price_change = np.random.uniform(-5.0, 5.0)
        
        # Scores por categoría de noticias
        category_scores = {}
        impacto_por_categoria = news_analysis.get('impacto', {}).get('impacto_por_categoria', {})
        
        for categoria, data in impacto_por_categoria.items():
            if isinstance(data, dict) and 'score' in data:
                category_scores[categoria] = data['score']
            else:
                category_scores[categoria] = 0.0
        
        # Indicadores técnicos simulados
        technical_indicators = self.generate_technical_indicators()
        
        return MarketFeatures(
            timestamp=datetime.now(),
            sentiment_score=sentiment_score,
            volatility=volatility,
            volume=volume,
            price_change=price_change,
            news_impact=news_impact,
            category_scores=category_scores,
            technical_indicators=technical_indicators
        )
    
    def calculate_news_impact(self, news_analysis: Dict) -> float:
        """Calcular impacto de noticias en el mercado"""
        try:
            noticias = news_analysis.get('noticias', [])
            if not noticias:
                return 0.5
            
            # Factores de impacto
            total_engagement = sum(n.get('engagement', 0) for n in noticias)
            avg_ml_score = sum(n.get('ml_score', 0.5) for n in noticias) / len(noticias)
            critical_news = sum(1 for n in noticias if n.get('importance') == 'critical')
            
            # Normalizar impacto
            engagement_factor = min(total_engagement / 10000, 1.0)
            ml_factor = avg_ml_score
            critical_factor = min(critical_news / 3, 1.0)
            
            news_impact = (engagement_factor * 0.4 + ml_factor * 0.4 + critical_factor * 0.2)
            return max(0.0, min(news_impact, 1.0))
            
        except Exception:
            return 0.5
    
    def generate_technical_indicators(self) -> Dict[str, float]:
        """Generar indicadores técnicos simulados"""
        indicators = {}
        
        for indicator in self.technical_features:
            if indicator == 'rsi':
                indicators[indicator] = np.random.uniform(20, 80)
            elif indicator == 'macd':
                indicators[indicator] = np.random.uniform(-2, 2)
            elif 'moving_average' in indicator:
                indicators[indicator] = np.random.uniform(0.8, 1.2)
            elif indicator == 'volume_trend':
                indicators[indicator] = np.random.uniform(0.5, 2.0)
            elif indicator == 'price_momentum':
                indicators[indicator] = np.random.uniform(-10, 10)
            else:
                indicators[indicator] = np.random.uniform(0.0, 1.0)
        
        return indicators
    
    def predict_market_direction(self, features: MarketFeatures) -> Tuple[str, float, Dict]:
        """Predecir dirección del mercado usando ML"""
        
        # Crear vector de características
        feature_vector = self.create_feature_vector(features)
        
        # Aplicar modelo (inicialmente regresión lineal simple)
        prediction_score = self.apply_ml_model(feature_vector)
        
        # Determinar dirección y confianza
        if prediction_score > 0.3:
            direction = 'BUY'
            confidence = min(prediction_score, 1.0)
        elif prediction_score < -0.3:
            direction = 'SELL'
            confidence = min(abs(prediction_score), 1.0)
        else:
            direction = 'HOLD'
            confidence = 0.5
        
        # Análisis detallado
        analysis = {
            'prediction_score': round(prediction_score, 3),
            'feature_contributions': self.analyze_feature_contributions(feature_vector),
            'market_regime': self.detect_market_regime(features),
            'risk_assessment': self.assess_risk(features),
            'optimal_timeframe': self.suggest_timeframe(features)
        }
        
        return direction, confidence, analysis
    
    def create_feature_vector(self, features: MarketFeatures) -> np.ndarray:
        """Crear vector de características para ML"""
        vector = []
        
        # Características básicas
        vector.extend([
            features.sentiment_score,
            features.volatility / 2.0,  # Normalizar
            features.volume / 3.0,      # Normalizar
            features.price_change / 10.0,  # Normalizar
            features.news_impact
        ])
        
        # Características por categoría (top 6)
        main_categories = ['fed_powell', 'economic_indicators', 'market_indices', 
                          'geopolitical', 'crypto_digital', 'commodities']
        
        for category in main_categories:
            score = features.category_scores.get(category, 0.0)
            vector.append(max(-1.0, min(score, 1.0)))  # Clip entre -1 y 1
        
        # Indicadores técnicos principales
        tech_score = np.mean([
            features.technical_indicators.get('rsi', 50) / 100,
            (features.technical_indicators.get('macd', 0) + 2) / 4,
            features.technical_indicators.get('moving_average_5', 1.0),
            features.technical_indicators.get('volume_trend', 1.0) / 2.0
        ])
        vector.append(tech_score)
        
        return np.array(vector)
    
    def apply_ml_model(self, feature_vector: np.ndarray) -> float:
        """Aplicar modelo de ML (inicialmente regresión lineal)"""
        try:
            # Pesos del modelo (inicialmente manual, luego aprendido)
            if len(self.model_data['features']) < self.config['min_data_points']:
                # Modelo inicial basado en reglas
                weights = np.array([
                    0.25,  # sentiment_score
                    -0.15, # volatility (alta volatilidad = precaución)
                    0.10,  # volume
                    0.20,  # price_change
                    0.15,  # news_impact
                    0.05, 0.10, 0.15, 0.05, 0.03, 0.02,  # categorías
                    0.10   # technical_score
                ])
            else:
                # Usar pesos aprendidos
                weights = self.get_learned_weights()
            
            # Asegurar compatibilidad de dimensiones
            min_length = min(len(feature_vector), len(weights))
            prediction = np.dot(feature_vector[:min_length], weights[:min_length])
            
            # Aplicar función de activación suave
            prediction = np.tanh(prediction)
            
            return float(prediction)
            
        except Exception as e:
            print(f"⚠️  Error en modelo ML: {e}")
            return 0.0
    
    def get_learned_weights(self) -> np.ndarray:
        """Obtener pesos aprendidos del modelo"""
        try:
            # Implementación básica de aprendizaje
            features_array = np.array(self.model_data['features'])
            outcomes_array = np.array([1 if o else -1 for o in self.model_data['outcomes']])
            
            # Regresión lineal simple
            if len(features_array) > 0:
                # Pseudo-inverse para regresión
                weights = np.linalg.pinv(features_array).dot(outcomes_array)
                return weights
            else:
                return np.random.uniform(-0.1, 0.1, 12)  # Pesos aleatorios pequeños
                
        except Exception:
            return np.random.uniform(-0.1, 0.1, 12)
    
    def analyze_feature_contributions(self, feature_vector: np.ndarray) -> Dict[str, float]:
        """Analizar contribución de cada característica"""
        feature_names = [
            'sentiment', 'volatility', 'volume', 'price_change', 'news_impact',
            'fed_powell', 'economic', 'market_indices', 'geopolitical', 
            'crypto', 'commodities', 'technical'
        ]
        
        contributions = {}
        weights = self.get_learned_weights() if len(self.model_data['features']) >= self.config['min_data_points'] else np.array([0.25, -0.15, 0.10, 0.20, 0.15, 0.05, 0.10, 0.15, 0.05, 0.03, 0.02, 0.10])
        
        for i, name in enumerate(feature_names):
            if i < len(feature_vector) and i < len(weights):
                contribution = feature_vector[i] * weights[i]
                contributions[name] = round(contribution, 3)
        
        return contributions
    
    def detect_market_regime(self, features: MarketFeatures) -> str:
        """Detectar régimen de mercado actual"""
        volatility = features.volatility
        sentiment = features.sentiment_score
        volume = features.volume
        
        if volatility > 1.5 and volume > 2.0:
            return 'high_volatility_high_volume'
        elif volatility > 1.2 and sentiment > 0.7:
            return 'bullish_momentum'
        elif volatility > 1.2 and sentiment < 0.3:
            return 'bearish_momentum'
        elif volatility < 0.5:
            return 'low_volatility_consolidation'
        elif sentiment > 0.6 and volume > 1.5:
            return 'strong_trend'
        else:
            return 'neutral_market'
    
    def assess_risk(self, features: MarketFeatures) -> Dict[str, float]:
        """Evaluar riesgo del mercado"""
        risk_factors = {
            'volatility_risk': min(features.volatility / 2.0, 1.0),
            'news_risk': features.news_impact,
            'sentiment_risk': abs(features.sentiment_score - 0.5) * 2,
            'technical_risk': self.calculate_technical_risk(features.technical_indicators)
        }
        
        overall_risk = np.mean(list(risk_factors.values()))
        risk_factors['overall_risk'] = round(overall_risk, 3)
        
        return risk_factors
    
    def calculate_technical_risk(self, tech_indicators: Dict[str, float]) -> float:
        """Calcular riesgo técnico"""
        try:
            rsi = tech_indicators.get('rsi', 50)
            rsi_risk = 0.5 if 30 <= rsi <= 70 else 1.0
            
            volume_trend = tech_indicators.get('volume_trend', 1.0)
            volume_risk = abs(volume_trend - 1.0)
            
            momentum = tech_indicators.get('price_momentum', 0)
            momentum_risk = min(abs(momentum) / 10, 1.0)
            
            return np.mean([rsi_risk, volume_risk, momentum_risk])
            
        except Exception:
            return 0.5
    
    def suggest_timeframe(self, features: MarketFeatures) -> str:
        """Sugerir timeframe óptimo basado en condiciones"""
        volatility = features.volatility
        news_impact = features.news_impact
        
        if volatility > 1.5 and news_impact > 0.7:
            return 'M1_M5'  # Scalping en alta volatilidad
        elif volatility > 1.0:
            return 'M5_M15'  # Trading rápido
        elif news_impact > 0.6:
            return 'M15_M30'  # Swing corto
        else:
            return 'H1_H4'  # Swing trading
    
    def learn_from_outcome(self, features: MarketFeatures, actual_outcome: bool, 
                          prediction: str, confidence: float):
        """Aprender del resultado real para mejorar el modelo"""
        
        # Agregar a datos de entrenamiento
        feature_vector = self.create_feature_vector(features)
        self.model_data['features'].append(feature_vector.tolist())
        self.model_data['outcomes'].append(actual_outcome)
        
        # Actualizar métricas
        self.model_data['total_predictions'] += 1
        if actual_outcome:
            self.model_data['correct_predictions'] += 1
        
        # Calcular accuracy
        self.model_data['accuracy'] = (self.model_data['correct_predictions'] / 
                                     self.model_data['total_predictions'])
        
        # Reentrenar si es necesario
        if (self.model_data['total_predictions'] % self.config['retrain_frequency'] == 0 and
            self.model_data['total_predictions'] >= self.config['min_data_points']):
            self.retrain_model()
        
        # Actualizar métricas de rendimiento
        self.update_performance_metrics(features, actual_outcome, prediction, confidence)
        
        print(f"📚 Aprendizaje ML: Accuracy actual: {self.model_data['accuracy']:.3f} "
              f"({self.model_data['correct_predictions']}/{self.model_data['total_predictions']})")
    
    def retrain_model(self):
        """Reentrenar el modelo con nuevos datos"""
        print("🧠 Reentrenando modelo ML...")
        
        try:
            # Implementación básica de reentrenamiento
            features_array = np.array(self.model_data['features'])
            outcomes_array = np.array([1 if o else -1 for o in self.model_data['outcomes']])
            
            # Aplicar gradient descent básico
            learning_rate = self.model_data['learning_rate']
            current_weights = self.get_learned_weights()
            
            # Calcular gradientes (simplificado)
            predictions = features_array.dot(current_weights)
            errors = outcomes_array - predictions
            gradients = features_array.T.dot(errors) / len(features_array)
            
            # Actualizar pesos
            new_weights = current_weights + learning_rate * gradients
            
            # Validar mejora
            new_predictions = features_array.dot(new_weights)
            new_accuracy = np.mean((new_predictions > 0) == (outcomes_array > 0))
            
            if new_accuracy > self.model_data['accuracy']:
                print(f"✅ Modelo mejorado: {self.model_data['accuracy']:.3f} → {new_accuracy:.3f}")
                # Aquí guardaríamos los nuevos pesos
            else:
                print(f"⚠️  Modelo no mejoró, manteniendo pesos anteriores")
                
        except Exception as e:
            print(f"❌ Error en reentrenamiento: {e}")
    
    def update_performance_metrics(self, features: MarketFeatures, outcome: bool, 
                                 prediction: str, confidence: float):
        """Actualizar métricas de rendimiento"""
        
        # Métricas por régimen de mercado
        regime = self.detect_market_regime(features)
        if regime not in self.performance_metrics['category_performance']:
            self.performance_metrics['category_performance'][regime] = {
                'correct': 0, 'total': 0, 'accuracy': 0.0
            }
        
        regime_stats = self.performance_metrics['category_performance'][regime]
        regime_stats['total'] += 1
        if outcome:
            regime_stats['correct'] += 1
        regime_stats['accuracy'] = regime_stats['correct'] / regime_stats['total']
        
        # Identificar mejores/peores condiciones
        condition_key = f"{regime}_{prediction}"
        
        if outcome and confidence > 0.7:
            if condition_key not in self.performance_metrics['best_conditions']:
                self.performance_metrics['best_conditions'][condition_key] = 0
            self.performance_metrics['best_conditions'][condition_key] += 1
        elif not outcome and confidence > 0.6:
            if condition_key not in self.performance_metrics['worst_conditions']:
                self.performance_metrics['worst_conditions'][condition_key] = 0
            self.performance_metrics['worst_conditions'][condition_key] += 1
    
    def get_ml_insights(self) -> Dict:
        """Obtener insights del sistema ML"""
        return {
            'model_stats': {
                'total_predictions': self.model_data['total_predictions'],
                'accuracy': self.model_data['accuracy'],
                'data_points': len(self.model_data['features']),
                'learning_rate': self.model_data['learning_rate']
            },
            'performance_by_regime': self.performance_metrics['category_performance'],
            'best_conditions': dict(sorted(
                self.performance_metrics['best_conditions'].items(),
                key=lambda x: x[1], reverse=True
            )[:5]),
            'worst_conditions': dict(sorted(
                self.performance_metrics['worst_conditions'].items(),
                key=lambda x: x[1], reverse=True
            )[:5]),
            'feature_importance': self.calculate_feature_importance()
        }
    
    def calculate_feature_importance(self) -> Dict[str, float]:
        """Calcular importancia de características"""
        if len(self.model_data['features']) < self.config['min_data_points']:
            return {'insufficient_data': 1.0}
        
        try:
            weights = self.get_learned_weights()
            feature_names = [
                'sentiment', 'volatility', 'volume', 'price_change', 'news_impact',
                'fed_powell', 'economic', 'market_indices', 'geopolitical', 
                'crypto', 'commodities', 'technical'
            ]
            
            importance = {}
            for i, name in enumerate(feature_names):
                if i < len(weights):
                    importance[name] = abs(float(weights[i]))
            
            # Normalizar
            total = sum(importance.values())
            if total > 0:
                importance = {k: v/total for k, v in importance.items()}
            
            return dict(sorted(importance.items(), key=lambda x: x[1], reverse=True))
            
        except Exception:
            return {'error': 1.0}
    
    def save_model(self, filepath: str = 'data/ml_model.json'):
        """Guardar modelo y datos"""
        os.makedirs('data', exist_ok=True)
        
        model_export = {
            'model_data': self.model_data,
            'performance_metrics': self.performance_metrics,
            'config': self.config,
            'feature_weights': self.feature_weights,
            'saved_at': datetime.now().isoformat(),
            'version': 'ml_v2.0'
        }
        
        with open(filepath, 'w') as f:
            json.dump(model_export, f, indent=2, default=str)
        
        print(f"💾 Modelo ML guardado en {filepath}")
    
    def load_model(self, filepath: str = 'data/ml_model.json'):
        """Cargar modelo guardado"""
        try:
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    model_export = json.load(f)
                
                self.model_data = model_export.get('model_data', self.model_data)
                self.performance_metrics = model_export.get('performance_metrics', self.performance_metrics)
                self.config = model_export.get('config', self.config)
                self.feature_weights = model_export.get('feature_weights', self.feature_weights)
                
                print(f"📚 Modelo ML cargado desde {filepath}")
                print(f"   Accuracy: {self.model_data['accuracy']:.3f}")
                print(f"   Predicciones: {self.model_data['total_predictions']}")
                return True
            else:
                print(f"⚠️  Archivo {filepath} no encontrado, usando modelo nuevo")
                return False
        except Exception as e:
            print(f"❌ Error cargando modelo: {e}")
            return False

def main():
    """Función principal para pruebas"""
    print("🧠 PROBANDO SISTEMA ML AVANZADO")
    print("=" * 50)
    
    # Crear sistema ML
    ml_system = AdvancedMLTradingSystem()
    
    # Simular análisis de noticias
    fake_news_analysis = {
        'impacto': {
            'confianza_general': 0.8,
            'impacto_por_categoria': {
                'fed_powell': {'score': 0.6},
                'economic_indicators': {'score': 0.4},
                'market_indices': {'score': 0.7}
            }
        },
        'noticias': [
            {'engagement': 2000, 'ml_score': 0.8, 'importance': 'high'},
            {'engagement': 1500, 'ml_score': 0.6, 'importance': 'medium'}
        ]
    }
    
    # Extraer características
    features = ml_system.extract_market_features({}, fake_news_analysis)
    
    # Hacer predicción
    direction, confidence, analysis = ml_system.predict_market_direction(features)
    
    print(f"🎯 Predicción: {direction}")
    print(f"🎲 Confianza: {confidence:.3f}")
    print(f"📊 Score: {analysis['prediction_score']}")
    print(f"🏢 Régimen: {analysis['market_regime']}")
    print(f"⚠️  Riesgo: {analysis['risk_assessment']['overall_risk']:.3f}")
    print(f"⏰ Timeframe: {analysis['optimal_timeframe']}")
    
    # Simular aprendizaje
    for i in range(20):
        outcome = np.random.choice([True, False], p=[0.6, 0.4])
        ml_system.learn_from_outcome(features, outcome, direction, confidence)
        
        # Nueva predicción
        features = ml_system.extract_market_features({}, fake_news_analysis)
        direction, confidence, analysis = ml_system.predict_market_direction(features)
    
    # Mostrar insights
    insights = ml_system.get_ml_insights()
    print(f"\n📈 INSIGHTS ML:")
    print(f"   Accuracy final: {insights['model_stats']['accuracy']:.3f}")
    print(f"   Datos entrenamiento: {insights['model_stats']['data_points']}")
    
    # Guardar modelo
    ml_system.save_model()
    
    print("\n✅ PRUEBA ML COMPLETADA")

if __name__ == "__main__":
    main() 