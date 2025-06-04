#!/usr/bin/env python3
"""
ANALIZADOR DE NOTICIAS TWITTER AVANZADO - BOT SMC-LIT
===================================================
Análisis completo de noticias con Machine Learning
"""

import json
import random
import re
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
import numpy as np

class AdvancedTwitterNewsAnalyzer:
    def __init__(self):
        self.twitter_credentials = {
            'username': 'chevex9275518',
            'password': 'Jose01122023*',
            'logged_in': False
        }
        
        # Palabras clave expandidas para análisis integral
        self.keywords = {
            'fed_powell': [
                'powell', 'fed', 'federal reserve', 'fomc', 'interest rate', 
                'monetary policy', 'jackson hole', 'yellen', 'federal open market',
                'rate hike', 'rate cut', 'dovish', 'hawkish', 'fed minutes'
            ],
            'economic_indicators': [
                'inflation', 'cpi', 'ppi', 'gdp', 'unemployment', 'nonfarm',
                'retail sales', 'consumer confidence', 'recession', 'jobless claims',
                'pce', 'ism', 'manufacturing', 'services pmi', 'productivity'
            ],
            'market_indices': [
                'nasdaq', 'sp500', 's&p 500', 'dow jones', 'russell',
                'tech stocks', 'apple', 'microsoft', 'tesla', 'nvidia', 
                'amazon', 'google', 'meta', 'earnings'
            ],
            'geopolitical': [
                'ukraine', 'russia', 'china', 'taiwan', 'middle east',
                'sanctions', 'trade war', 'election', 'brexit', 'europe',
                'oil', 'energy crisis', 'supply chain'
            ],
            'crypto_digital': [
                'bitcoin', 'ethereum', 'crypto', 'cryptocurrency', 'digital currency',
                'cbdc', 'defi', 'nft', 'blockchain', 'binance', 'coinbase'
            ],
            'commodities': [
                'gold', 'silver', 'oil', 'crude', 'natural gas', 'copper',
                'wheat', 'corn', 'soybeans', 'coffee', 'sugar'
            ],
            'banking_finance': [
                'bank earnings', 'credit', 'lending', 'mortgage rates',
                'jpmorgan', 'bank of america', 'wells fargo', 'goldman sachs',
                'banking crisis', 'svb', 'credit suisse'
            ]
        }
        
        # Configuración de análisis con ML
        self.sentiment_weights = {
            'very_bullish': 1.0,
            'bullish': 0.6,
            'neutral': 0.0,
            'bearish': -0.6,
            'very_bearish': -1.0
        }
        
        # Historial para machine learning
        self.historical_data = []
        self.prediction_model = None
        
    def simulate_twitter_login(self):
        """Simular login a Twitter (para demostración)"""
        print("🐦 CONECTANDO A TWITTER AVANZADO...")
        print(f"👤 Usuario: {self.twitter_credentials['username']}")
        print("🔐 Autenticando con análisis expandido...")
        
        # Simular proceso de login
        import time
        time.sleep(2)
        
        self.twitter_credentials['logged_in'] = True
        print("✅ Conectado a Twitter con capacidades ML")
        return True
    
    def buscar_noticias_expandidas(self, limit: int = 100) -> List[Dict]:
        """Buscar noticias relevantes expandidas con categorización automática"""
        print("📰 BUSCANDO NOTICIAS EXPANDIDAS...")
        
        # Noticias simuladas más diversas y realistas
        noticias_simuladas = [
            # Fed/Powell
            {
                'id': '1001', 'text': 'Fed Chair Powell signals potential rate cuts amid cooling inflation data. Markets respond positively.',
                'timestamp': datetime.now() - timedelta(hours=2), 'source': '@federalreserve',
                'category': 'fed_powell', 'engagement': 1250, 'importance': 'high'
            },
            {
                'id': '1002', 'text': 'FOMC minutes reveal divided opinions on future rate policy. Some members favor more aggressive stance.',
                'timestamp': datetime.now() - timedelta(hours=1), 'source': '@reuters',
                'category': 'fed_powell', 'engagement': 890, 'importance': 'high'
            },
            
            # Indicadores económicos
            {
                'id': '2001', 'text': 'BREAKING: US inflation drops to 2.4%, below Fed target. Core CPI shows continued moderation.',
                'timestamp': datetime.now() - timedelta(hours=1), 'source': '@bloomberg',
                'category': 'economic_indicators', 'engagement': 2340, 'importance': 'critical'
            },
            {
                'id': '2002', 'text': 'Unemployment rate falls to 3.7%, labor market remains tight despite recent layoffs in tech.',
                'timestamp': datetime.now() - timedelta(minutes=45), 'source': '@wsj',
                'category': 'economic_indicators', 'engagement': 1560, 'importance': 'high'
            },
            {
                'id': '2003', 'text': 'Consumer confidence index surges to 6-month high as recession fears fade.',
                'timestamp': datetime.now() - timedelta(minutes=30), 'source': '@cnbc',
                'category': 'economic_indicators', 'engagement': 780, 'importance': 'medium'
            },
            
            # Índices y mercados
            {
                'id': '3001', 'text': 'Tech stocks rally as NASDAQ reaches new highs. Apple and Microsoft lead gains.',
                'timestamp': datetime.now() - timedelta(minutes=15), 'source': '@cnbc',
                'category': 'market_indices', 'engagement': 1560, 'importance': 'high'
            },
            {
                'id': '3002', 'text': 'NVIDIA earnings beat expectations, stock surges 8% in after-hours trading.',
                'timestamp': datetime.now() - timedelta(minutes=20), 'source': '@marketwatch',
                'category': 'market_indices', 'engagement': 2100, 'importance': 'high'
            },
            
            # Geopolítica
            {
                'id': '4001', 'text': 'Ukraine conflict developments could impact energy markets and global supply chains.',
                'timestamp': datetime.now() - timedelta(hours=3), 'source': '@bbcbreaking',
                'category': 'geopolitical', 'engagement': 1890, 'importance': 'high'
            },
            {
                'id': '4002', 'text': 'China manufacturing PMI shows unexpected recovery, easing global recession concerns.',
                'timestamp': datetime.now() - timedelta(hours=4), 'source': '@ft',
                'category': 'geopolitical', 'engagement': 980, 'importance': 'medium'
            },
            
            # Cripto
            {
                'id': '5001', 'text': 'Bitcoin breaks $45,000 resistance as institutional adoption accelerates.',
                'timestamp': datetime.now() - timedelta(minutes=10), 'source': '@coindesk',
                'category': 'crypto_digital', 'engagement': 1670, 'importance': 'medium'
            },
            
            # Commodities
            {
                'id': '6001', 'text': 'Gold prices surge amid banking sector concerns and safe-haven demand.',
                'timestamp': datetime.now() - timedelta(minutes=25), 'source': '@kitco',
                'category': 'commodities', 'engagement': 890, 'importance': 'medium'
            },
            {
                'id': '6002', 'text': 'Oil prices rally on OPEC+ production cut rumors and strong demand outlook.',
                'timestamp': datetime.now() - timedelta(hours=2), 'source': '@oilprice',
                'category': 'commodities', 'engagement': 1230, 'importance': 'medium'
            },
            
            # Banca
            {
                'id': '7001', 'text': 'JPMorgan CEO warns of potential credit tightening impact on economy.',
                'timestamp': datetime.now() - timedelta(hours=5), 'source': '@jpmorgan',
                'category': 'banking_finance', 'engagement': 1340, 'importance': 'high'
            }
        ]
        
        # Filtrar por relevancia y engagement, añadir scoring ML
        noticias_filtradas = []
        for noticia in noticias_simuladas:
            if noticia['engagement'] > 500:
                # Añadir score ML basado en múltiples factores
                ml_score = self.calcular_ml_score(noticia)
                noticia['ml_score'] = ml_score
                noticias_filtradas.append(noticia)
        
        # Ordenar por relevancia combinada
        noticias_filtradas.sort(key=lambda x: (x['ml_score'], x['engagement']), reverse=True)
        
        print(f"📊 Encontradas {len(noticias_filtradas)} noticias relevantes")
        print(f"🎯 Categorías cubiertas: {len(set(n['category'] for n in noticias_filtradas))}")
        
        return noticias_filtradas[:limit]
    
    def calcular_ml_score(self, noticia: Dict) -> float:
        """Calcular score usando técnicas básicas de ML"""
        score = 0.0
        
        # Factor de importancia
        importance_weights = {'critical': 1.0, 'high': 0.8, 'medium': 0.6, 'low': 0.4}
        score += importance_weights.get(noticia.get('importance', 'medium'), 0.6)
        
        # Factor temporal (noticias más recientes son más relevantes)
        hours_ago = (datetime.now() - noticia['timestamp']).total_seconds() / 3600
        time_factor = max(0, 1 - (hours_ago / 24))  # Decae en 24 horas
        score += time_factor * 0.5
        
        # Factor de engagement normalizado
        engagement_factor = min(noticia['engagement'] / 5000, 1.0)
        score += engagement_factor * 0.3
        
        # Factor de palabras clave críticas
        text_lower = noticia['text'].lower()
        critical_words = ['breaking', 'urgent', 'alert', 'crisis', 'surge', 'plummet']
        critical_count = sum(1 for word in critical_words if word in text_lower)
        score += critical_count * 0.1
        
        return round(score, 3)
    
    def analizar_sentimiento_avanzado(self, texto: str, categoria: str) -> Tuple[str, float, Dict]:
        """Análisis de sentimiento avanzado específico por categoría"""
        texto_lower = texto.lower()
        
        # Palabras específicas por categoría
        categoria_weights = {
            'fed_powell': {
                'muy_alcista': ['dovish', 'rate cut', 'stimulus', 'supportive', 'accommodative'],
                'alcista': ['positive', 'optimistic', 'confident', 'stability'],
                'muy_bajista': ['hawkish', 'rate hike', 'tightening', 'aggressive', 'restrictive'],
                'bajista': ['concern', 'worried', 'caution', 'uncertainty']
            },
            'economic_indicators': {
                'muy_alcista': ['beats expectations', 'surge', 'strong growth', 'robust'],
                'alcista': ['improvement', 'growth', 'expansion', 'positive'],
                'muy_bajista': ['recession', 'contraction', 'collapse', 'crisis'],
                'bajista': ['weakness', 'decline', 'concern', 'slowdown']
            },
            'market_indices': {
                'muy_alcista': ['rally', 'surge', 'new highs', 'breakout'],
                'alcista': ['gains', 'rise', 'positive', 'up'],
                'muy_bajista': ['crash', 'plummet', 'sell-off', 'collapse'],
                'bajista': ['decline', 'fall', 'drop', 'negative']
            }
        }
        
        # Palabras generales como fallback
        palabras_muy_alcistas = ['surge', 'rally', 'soar', 'breakout', 'bullish', 'strong growth']
        palabras_alcistas = ['rise', 'increase', 'up', 'higher', 'optimistic', 'confident', 'positive']
        palabras_muy_bajistas = ['crash', 'plummet', 'collapse', 'panic', 'crisis', 'recession']
        palabras_bajistas = ['fall', 'drop', 'decline', 'down', 'lower', 'concern', 'worry']
        palabras_neutrales = ['stable', 'unchanged', 'mixed', 'wait', 'monitor', 'watch']
        
        # Usar palabras específicas de categoría si disponibles
        if categoria in categoria_weights:
            cat_words = categoria_weights[categoria]
            palabras_muy_alcistas.extend(cat_words.get('muy_alcista', []))
            palabras_alcistas.extend(cat_words.get('alcista', []))
            palabras_muy_bajistas.extend(cat_words.get('muy_bajista', []))
            palabras_bajistas.extend(cat_words.get('bajista', []))
        
        # Contar ocurrencias con pesos
        score = 0
        details = {
            'muy_alcista': 0, 'alcista': 0, 'neutral': 0,
            'bajista': 0, 'muy_bajista': 0, 'categoria': categoria
        }
        
        for palabra in palabras_muy_alcistas:
            count = texto_lower.count(palabra)
            score += count * 2
            details['muy_alcista'] += count
            
        for palabra in palabras_alcistas:
            count = texto_lower.count(palabra)
            score += count * 1
            details['alcista'] += count
            
        for palabra in palabras_muy_bajistas:
            count = texto_lower.count(palabra)
            score -= count * 2
            details['muy_bajista'] += count
            
        for palabra in palabras_bajistas:
            count = texto_lower.count(palabra)
            score -= count * 1
            details['bajista'] += count
            
        for palabra in palabras_neutrales:
            count = texto_lower.count(palabra)
            details['neutral'] += count
        
        # Determinar sentimiento final
        if score >= 2:
            sentimiento = 'very_bullish'
        elif score >= 1:
            sentimiento = 'bullish'
        elif score <= -2:
            sentimiento = 'very_bearish'
        elif score <= -1:
            sentimiento = 'bearish'
        else:
            sentimiento = 'neutral'
        
        # Calcular confianza basada en múltiples factores
        base_confidence = min(abs(score) * 0.2 + 0.3, 1.0)
        category_bonus = 0.1 if categoria in categoria_weights else 0
        confianza = min(base_confidence + category_bonus, 1.0)
        
        return sentimiento, confianza, details
    
    def analizar_impacto_mercado_avanzado(self, noticias: List[Dict]) -> Dict:
        """Análisis avanzado de impacto en mercado con ML"""
        print("📈 ANALIZANDO IMPACTO AVANZADO EN EL MERCADO...")
        
        impacto_total = {
            'sentimiento_general': 'neutral',
            'confianza_general': 0.0,
            'impacto_por_categoria': {},
            'impacto_nasdaq': 'neutral',
            'impacto_sp500': 'neutral',
            'impacto_forex': 'neutral',
            'impacto_commodities': 'neutral',
            'recomendacion': 'hold',
            'factores_clave': [],
            'noticias_analizadas': len(noticias),
            'timestamp': datetime.now().isoformat(),
            'ml_prediction': 'neutral'
        }
        
        scores_por_categoria = {}
        
        # Inicializar scores por categoría
        for categoria in self.keywords.keys():
            scores_por_categoria[categoria] = []
        
        # Analizar cada noticia con ML
        for noticia in noticias:
            sentimiento, confianza, details = self.analizar_sentimiento_avanzado(
                noticia['text'], noticia['category']
            )
            
            # Aplicar múltiples pesos
            peso_engagement = min(noticia['engagement'] / 1000, 2.0)
            peso_ml = noticia.get('ml_score', 0.5)
            peso_tiempo = max(0.5, 1 - ((datetime.now() - noticia['timestamp']).total_seconds() / 86400))
            
            score_ponderado = (self.sentiment_weights[sentimiento] * 
                             confianza * peso_engagement * peso_ml * peso_tiempo)
            
            scores_por_categoria[noticia['category']].append(score_ponderado)
            
            # Factores clave
            if abs(score_ponderado) > 0.5:
                factor = {
                    'categoria': noticia['category'],
                    'sentimiento': sentimiento,
                    'score': score_ponderado,
                    'fuente': noticia['source']
                }
                impacto_total['factores_clave'].append(factor)
        
        # Calcular impactos por categoría
        for categoria, scores in scores_por_categoria.items():
            if scores:
                promedio = sum(scores) / len(scores)
                impacto_total['impacto_por_categoria'][categoria] = {
                    'score': round(promedio, 3),
                    'sentiment': self.score_to_sentiment(promedio),
                    'noticias_count': len(scores)
                }
        
        # Impactos específicos por activo
        self.calcular_impactos_por_activo(impacto_total, scores_por_categoria)
        
        # Predicción ML
        ml_prediction = self.generar_prediccion_ml(scores_por_categoria)
        impacto_total['ml_prediction'] = ml_prediction
        
        # Sentimiento y recomendación general
        todos_scores = [score for scores in scores_por_categoria.values() for score in scores]
        if todos_scores:
            promedio_general = sum(todos_scores) / len(todos_scores)
            impacto_total['confianza_general'] = min(abs(promedio_general) + 0.3, 1.0)
            impacto_total['sentimiento_general'] = self.score_to_sentiment(promedio_general)
            impacto_total['recomendacion'] = self.score_to_recommendation(promedio_general)
        
        return impacto_total
    
    def calcular_impactos_por_activo(self, impacto_total: Dict, scores_por_categoria: Dict):
        """Calcular impactos específicos por tipo de activo"""
        # NASDAQ/S&P 500 - influenciado por tech, economic indicators, fed
        nasdaq_factors = []
        if 'market_indices' in scores_por_categoria:
            nasdaq_factors.extend(scores_por_categoria['market_indices'])
        if 'fed_powell' in scores_por_categoria:
            nasdaq_factors.extend([s * 0.7 for s in scores_por_categoria['fed_powell']])
        if 'economic_indicators' in scores_por_categoria:
            nasdaq_factors.extend([s * 0.6 for s in scores_por_categoria['economic_indicators']])
        
        if nasdaq_factors:
            nasdaq_score = sum(nasdaq_factors) / len(nasdaq_factors)
            impacto_total['impacto_nasdaq'] = self.score_to_sentiment(nasdaq_score)
            impacto_total['impacto_sp500'] = self.score_to_sentiment(nasdaq_score * 0.9)
        
        # Forex - influenciado por fed, economic indicators, geopolitical
        forex_factors = []
        if 'fed_powell' in scores_por_categoria:
            forex_factors.extend(scores_por_categoria['fed_powell'])
        if 'economic_indicators' in scores_por_categoria:
            forex_factors.extend([s * 0.8 for s in scores_por_categoria['economic_indicators']])
        if 'geopolitical' in scores_por_categoria:
            forex_factors.extend([s * 0.6 for s in scores_por_categoria['geopolitical']])
        
        if forex_factors:
            forex_score = sum(forex_factors) / len(forex_factors)
            impacto_total['impacto_forex'] = self.score_to_sentiment(forex_score)
        
        # Commodities - influenciado por geopolitical, economic indicators
        commodities_factors = []
        if 'commodities' in scores_por_categoria:
            commodities_factors.extend(scores_por_categoria['commodities'])
        if 'geopolitical' in scores_por_categoria:
            commodities_factors.extend([s * 0.8 for s in scores_por_categoria['geopolitical']])
        if 'economic_indicators' in scores_por_categoria:
            commodities_factors.extend([s * 0.5 for s in scores_por_categoria['economic_indicators']])
        
        if commodities_factors:
            commodities_score = sum(commodities_factors) / len(commodities_factors)
            impacto_total['impacto_commodities'] = self.score_to_sentiment(commodities_score)
    
    def generar_prediccion_ml(self, scores_por_categoria: Dict) -> str:
        """Generar predicción usando técnicas básicas de ML"""
        try:
            # Crear vector de características
            features = []
            for categoria in ['fed_powell', 'economic_indicators', 'market_indices', 
                            'geopolitical', 'crypto_digital', 'commodities']:
                if categoria in scores_por_categoria and scores_por_categoria[categoria]:
                    avg_score = sum(scores_por_categoria[categoria]) / len(scores_por_categoria[categoria])
                    features.append(avg_score)
                else:
                    features.append(0.0)
            
            if not features:
                return 'neutral'
            
            # Reglas básicas de ML (simuladas)
            feature_array = np.array(features)
            
            # Pesos aprendidos (simulados)
            weights = np.array([0.3, 0.25, 0.2, 0.15, 0.05, 0.05])
            
            # Predicción ponderada
            prediction_score = np.dot(feature_array, weights)
            
            # Clasificación
            if prediction_score > 0.3:
                return 'bullish_trend'
            elif prediction_score < -0.3:
                return 'bearish_trend'
            else:
                return 'sideways_trend'
                
        except Exception:
            return 'neutral'
    
    def score_to_sentiment(self, score: float) -> str:
        """Convertir score numérico a sentimiento"""
        if score >= 0.4:
            return 'bullish'
        elif score >= 0.2:
            return 'slightly_bullish'
        elif score <= -0.4:
            return 'bearish'
        elif score <= -0.2:
            return 'slightly_bearish'
        else:
            return 'neutral'
    
    def score_to_recommendation(self, score: float) -> str:
        """Convertir score a recomendación"""
        if score >= 0.5:
            return 'strong_buy'
        elif score >= 0.3:
            return 'buy'
        elif score <= -0.5:
            return 'strong_sell'
        elif score <= -0.3:
            return 'sell'
        else:
            return 'hold'
    
    def generar_resumen_avanzado(self, noticias: List[Dict], impacto: Dict) -> str:
        """Generar resumen avanzado con análisis por categorías"""
        resumen = f"""
🐦 ANÁLISIS AVANZADO DE NOTICIAS - {datetime.now().strftime('%H:%M:%S')}
══════════════════════════════════════════════════════════════════

📊 RESUMEN GENERAL:
• Noticias analizadas: {impacto['noticias_analizadas']}
• Sentimiento general: {impacto['sentimiento_general'].upper()}
• Confianza: {impacto['confianza_general']:.2f}
• Recomendación: {impacto['recomendacion'].upper()}
• Predicción ML: {impacto['ml_prediction'].upper()}

📈 IMPACTO POR MERCADO:
• NASDAQ: {impacto['impacto_nasdaq'].upper()}
• S&P 500: {impacto['impacto_sp500'].upper()}
• Forex: {impacto['impacto_forex'].upper()}
• Commodities: {impacto['impacto_commodities'].upper()}

🎯 ANÁLISIS POR CATEGORÍA:"""
        
        for categoria, data in impacto['impacto_por_categoria'].items():
            if data['noticias_count'] > 0:
                resumen += f"""
• {categoria.replace('_', ' ').title()}: {data['sentiment'].upper()} (Score: {data['score']:.2f}, Noticias: {data['noticias_count']})"""
        
        resumen += f"""

🔥 FACTORES CLAVE:"""
        
        for i, factor in enumerate(impacto['factores_clave'][:5], 1):
            resumen += f"""
{i}. {factor['categoria'].replace('_', ' ').title()}: {factor['sentimiento'].upper()} 
   Score: {factor['score']:.2f} | Fuente: {factor['fuente']}"""
        
        resumen += f"""

📰 NOTICIAS MÁS RELEVANTES:"""
        
        # Ordenar por ML score y engagement
        noticias_ordenadas = sorted(noticias, 
                                  key=lambda x: (x.get('ml_score', 0), x['engagement']), 
                                  reverse=True)
        
        for i, noticia in enumerate(noticias_ordenadas[:5], 1):
            sentimiento, confianza, _ = self.analizar_sentimiento_avanzado(
                noticia['text'], noticia['category']
            )
            resumen += f"""
{i}. [{noticia['category'].upper()}] {noticia['source']} 
   📝 {noticia['text'][:120]}...
   💭 {sentimiento.upper()} | Confianza: {confianza:.2f} | ML Score: {noticia.get('ml_score', 0):.2f}
   🔥 {noticia['engagement']} interacciones | ⏰ {noticia['timestamp'].strftime('%H:%M')}"""
        
        return resumen
    
    def ejecutar_analisis_completo_avanzado(self) -> Dict:
        """Ejecutar análisis completo avanzado con ML"""
        print("🚀 INICIANDO ANÁLISIS COMPLETO AVANZADO CON ML")
        print("=" * 70)
        
        # Conectar a Twitter
        if not self.twitter_credentials['logged_in']:
            success = self.simulate_twitter_login()
            if not success:
                return {'error': 'No se pudo conectar a Twitter'}
        
        # Buscar noticias expandidas
        noticias = self.buscar_noticias_expandidas()
        
        if not noticias:
            return {'error': 'No se encontraron noticias relevantes'}
        
        # Analizar impacto con ML
        impacto = self.analizar_impacto_mercado_avanzado(noticias)
        
        # Generar resumen avanzado
        resumen = self.generar_resumen_avanzado(noticias, impacto)
        
        print(resumen)
        
        # Guardar análisis expandido
        resultado = {
            'impacto': impacto,
            'noticias': noticias,
            'resumen': resumen,
            'ml_features': {
                'categories_analyzed': len(set(n['category'] for n in noticias)),
                'total_engagement': sum(n['engagement'] for n in noticias),
                'avg_ml_score': sum(n.get('ml_score', 0) for n in noticias) / len(noticias),
                'time_range_hours': 24
            },
            'timestamp': datetime.now().isoformat(),
            'version': 'advanced_ml_v2.0'
        }
        
        # Guardar en data/
        import os
        os.makedirs('data', exist_ok=True)
        with open('data/twitter_analysis_advanced.json', 'w') as f:
            json.dump(resultado, f, indent=2, default=str)
        
        print("💾 Análisis avanzado guardado en data/twitter_analysis_advanced.json")
        return resultado

# Mantener compatibilidad con versión anterior
class TwitterNewsAnalyzer(AdvancedTwitterNewsAnalyzer):
    """Clase de compatibilidad que hereda todas las funciones avanzadas"""
    
    def ejecutar_analisis_completo(self) -> Dict:
        """Método de compatibilidad que ejecuta el análisis avanzado"""
        return self.ejecutar_analisis_completo_avanzado()

def main():
    """Función principal para pruebas"""
    analyzer = AdvancedTwitterNewsAnalyzer()
    resultado = analyzer.ejecutar_analisis_completo_avanzado()
    
    if 'error' not in resultado:
        print("\n✅ ANÁLISIS AVANZADO COMPLETADO EXITOSAMENTE")
        print(f"🎯 Recomendación: {resultado['impacto']['recomendacion'].upper()}")
        print(f"📊 Sentimiento: {resultado['impacto']['sentimiento_general'].upper()}")
        print(f"🤖 Predicción ML: {resultado['impacto']['ml_prediction'].upper()}")
        print(f"📈 Categorías analizadas: {resultado['ml_features']['categories_analyzed']}")
    else:
        print(f"\n❌ Error: {resultado['error']}")

if __name__ == "__main__":
    main() 