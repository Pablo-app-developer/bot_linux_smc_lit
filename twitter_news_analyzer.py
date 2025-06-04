#!/usr/bin/env python3
"""
ANALIZADOR DE NOTICIAS TWITTER - BOT SMC-LIT
===========================================
Análisis de noticias del Fed, Powell y eventos relevantes
"""

import json
import random
import re
from datetime import datetime, timedelta
from typing import List, Dict, Tuple

class TwitterNewsAnalyzer:
    def __init__(self):
        self.twitter_credentials = {
            'username': 'chevex9275518',
            'password': 'Jose01122023*',
            'logged_in': False
        }
        
        # Palabras clave para análisis de noticias relevantes
        self.keywords = {
            'fed_powell': [
                'powell', 'fed', 'federal reserve', 'fomc', 'interest rate', 
                'monetary policy', 'jackson hole', 'yellen', 'federal open market'
            ],
            'market_events': [
                'inflation', 'cpi', 'ppi', 'gdp', 'unemployment', 'nonfarm',
                'retail sales', 'consumer confidence', 'recession', 'dovish', 'hawkish'
            ],
            'nasdaq_sp500': [
                'nasdaq', 'sp500', 's&p 500', 'tech stocks', 'apple', 'microsoft',
                'tesla', 'nvidia', 'amazon', 'google', 'meta'
            ]
        }
        
        # Configuración de análisis
        self.sentiment_weights = {
            'very_bullish': 1.0,
            'bullish': 0.6,
            'neutral': 0.0,
            'bearish': -0.6,
            'very_bearish': -1.0
        }
        
    def simulate_twitter_login(self):
        """Simular login a Twitter (para demostración)"""
        print("🐦 CONECTANDO A TWITTER...")
        print(f"👤 Usuario: {self.twitter_credentials['username']}")
        print("🔐 Autenticando...")
        
        # Simular proceso de login
        import time
        time.sleep(2)
        
        self.twitter_credentials['logged_in'] = True
        print("✅ Conectado a Twitter exitosamente")
        return True
    
    def buscar_noticias_relevantes(self, limit: int = 50) -> List[Dict]:
        """Buscar noticias relevantes en Twitter"""
        print("📰 BUSCANDO NOTICIAS RELEVANTES...")
        
        # Simular búsqueda de tweets relevantes
        noticias_simuladas = [
            {
                'id': '1234567890',
                'text': 'Fed Chair Powell signals potential rate cuts amid cooling inflation data. Markets respond positively.',
                'timestamp': datetime.now() - timedelta(hours=2),
                'source': '@federalreserve',
                'category': 'fed_powell',
                'engagement': 1250
            },
            {
                'id': '1234567891', 
                'text': 'BREAKING: US inflation drops to 2.4%, below Fed target. NASDAQ surges on the news.',
                'timestamp': datetime.now() - timedelta(hours=1),
                'source': '@bloomberg',
                'category': 'market_events',
                'engagement': 2340
            },
            {
                'id': '1234567892',
                'text': 'FOMC minutes reveal divided opinions on future rate policy. Markets show mixed reaction.',
                'timestamp': datetime.now() - timedelta(minutes=30),
                'source': '@reuters',
                'category': 'fed_powell',
                'engagement': 890
            },
            {
                'id': '1234567893',
                'text': 'Tech stocks rally as NASDAQ reaches new highs. Apple and Microsoft lead gains.',
                'timestamp': datetime.now() - timedelta(minutes=15),
                'source': '@cnbc',
                'category': 'nasdaq_sp500',
                'engagement': 1560
            },
            {
                'id': '1234567894',
                'text': 'Economic data suggests strong labor market, potentially delaying Fed rate cuts.',
                'timestamp': datetime.now() - timedelta(minutes=45),
                'source': '@wsj',
                'category': 'market_events',
                'engagement': 780
            }
        ]
        
        # Filtrar por relevancia y engagement
        noticias_filtradas = [
            noticia for noticia in noticias_simuladas 
            if noticia['engagement'] > 500
        ]
        
        print(f"📊 Encontradas {len(noticias_filtradas)} noticias relevantes")
        return noticias_filtradas[:limit]
    
    def analizar_sentimiento_noticia(self, texto: str) -> Tuple[str, float, Dict]:
        """Analizar sentimiento de una noticia específica"""
        texto_lower = texto.lower()
        
        # Palabras clave para sentimiento
        palabras_muy_alcistas = ['surge', 'rally', 'soar', 'gains', 'positive', 'bullish', 'strong growth']
        palabras_alcistas = ['rise', 'increase', 'up', 'higher', 'optimistic', 'confident']
        palabras_muy_bajistas = ['crash', 'plummet', 'collapse', 'panic', 'crisis', 'recession']
        palabras_bajistas = ['fall', 'drop', 'decline', 'down', 'lower', 'concern', 'worry']
        palabras_neutrales = ['stable', 'unchanged', 'mixed', 'wait', 'monitor']
        
        # Contar ocurrencias
        score = 0
        details = {
            'muy_alcista': 0,
            'alcista': 0, 
            'neutral': 0,
            'bajista': 0,
            'muy_bajista': 0
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
        
        # Determinar sentimiento
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
        
        confianza = min(abs(score) * 0.2 + 0.3, 1.0)
        
        return sentimiento, confianza, details
    
    def analizar_impacto_mercado(self, noticias: List[Dict]) -> Dict:
        """Analizar impacto general en el mercado"""
        print("📈 ANALIZANDO IMPACTO EN EL MERCADO...")
        
        impacto_total = {
            'sentimiento_general': 'neutral',
            'confianza_general': 0.0,
            'impacto_nasdaq': 'neutral',
            'impacto_sp500': 'neutral',
            'impacto_fed': 'neutral',
            'recomendacion': 'hold',
            'noticias_analizadas': len(noticias),
            'timestamp': datetime.now().isoformat()
        }
        
        scores_por_categoria = {
            'fed_powell': [],
            'market_events': [],
            'nasdaq_sp500': []
        }
        
        # Analizar cada noticia
        for noticia in noticias:
            sentimiento, confianza, details = self.analizar_sentimiento_noticia(noticia['text'])
            
            # Aplicar peso basado en engagement
            peso = min(noticia['engagement'] / 1000, 2.0)
            score_ponderado = self.sentiment_weights[sentimiento] * confianza * peso
            
            scores_por_categoria[noticia['category']].append(score_ponderado)
        
        # Calcular promedios por categoría
        for categoria, scores in scores_por_categoria.items():
            if scores:
                promedio = sum(scores) / len(scores)
                
                if promedio >= 0.4:
                    sentiment = 'bullish'
                elif promedio >= 0.2:
                    sentiment = 'slightly_bullish'
                elif promedio <= -0.4:
                    sentiment = 'bearish'
                elif promedio <= -0.2:
                    sentiment = 'slightly_bearish'
                else:
                    sentiment = 'neutral'
                
                if categoria == 'fed_powell':
                    impacto_total['impacto_fed'] = sentiment
                elif categoria == 'nasdaq_sp500':
                    impacto_total['impacto_nasdaq'] = sentiment
                    impacto_total['impacto_sp500'] = sentiment
        
        # Sentimiento general
        todos_scores = []
        for scores in scores_por_categoria.values():
            todos_scores.extend(scores)
        
        if todos_scores:
            promedio_general = sum(todos_scores) / len(todos_scores)
            impacto_total['confianza_general'] = min(abs(promedio_general) + 0.3, 1.0)
            
            if promedio_general >= 0.3:
                impacto_total['sentimiento_general'] = 'bullish'
                impacto_total['recomendacion'] = 'buy'
            elif promedio_general <= -0.3:
                impacto_total['sentimiento_general'] = 'bearish'
                impacto_total['recomendacion'] = 'sell'
            else:
                impacto_total['sentimiento_general'] = 'neutral'
                impacto_total['recomendacion'] = 'hold'
        
        return impacto_total
    
    def generar_resumen_noticias(self, noticias: List[Dict], impacto: Dict) -> str:
        """Generar resumen de noticias para el bot"""
        resumen = f"""
🐦 ANÁLISIS DE NOTICIAS TWITTER - {datetime.now().strftime('%H:%M:%S')}
══════════════════════════════════════════════════════

📊 RESUMEN GENERAL:
• Noticias analizadas: {impacto['noticias_analizadas']}
• Sentimiento general: {impacto['sentimiento_general'].upper()}
• Confianza: {impacto['confianza_general']:.2f}
• Recomendación: {impacto['recomendacion'].upper()}

📈 IMPACTO POR MERCADO:
• Fed/Powell: {impacto['impacto_fed'].upper()}
• NASDAQ: {impacto['impacto_nasdaq'].upper()}
• S&P 500: {impacto['impacto_sp500'].upper()}

📰 NOTICIAS MÁS RELEVANTES:
"""
        
        # Añadir las 3 noticias más relevantes
        noticias_ordenadas = sorted(noticias, key=lambda x: x['engagement'], reverse=True)
        
        for i, noticia in enumerate(noticias_ordenadas[:3], 1):
            sentimiento, confianza, _ = self.analizar_sentimiento_noticia(noticia['text'])
            resumen += f"""
{i}. {noticia['source']} ({noticia['engagement']} interacciones)
   📝 {noticia['text'][:100]}...
   💭 Sentimiento: {sentimiento.upper()} (Confianza: {confianza:.2f})
"""
        
        return resumen
    
    def ejecutar_analisis_completo(self) -> Dict:
        """Ejecutar análisis completo de noticias"""
        print("🚀 INICIANDO ANÁLISIS COMPLETO DE NOTICIAS")
        print("=" * 60)
        
        # Conectar a Twitter
        if not self.twitter_credentials['logged_in']:
            success = self.simulate_twitter_login()
            if not success:
                return {'error': 'No se pudo conectar a Twitter'}
        
        # Buscar noticias
        noticias = self.buscar_noticias_relevantes()
        
        if not noticias:
            return {'error': 'No se encontraron noticias relevantes'}
        
        # Analizar impacto
        impacto = self.analizar_impacto_mercado(noticias)
        
        # Generar resumen
        resumen = self.generar_resumen_noticias(noticias, impacto)
        
        print(resumen)
        
        # Guardar análisis
        resultado = {
            'impacto': impacto,
            'noticias': noticias,
            'resumen': resumen,
            'timestamp': datetime.now().isoformat()
        }
        
        with open('twitter_analysis.json', 'w') as f:
            json.dump(resultado, f, indent=2, default=str)
        
        print("💾 Análisis guardado en twitter_analysis.json")
        return resultado

def main():
    """Función principal para pruebas"""
    analyzer = TwitterNewsAnalyzer()
    resultado = analyzer.ejecutar_analisis_completo()
    
    if 'error' not in resultado:
        print("\n✅ ANÁLISIS COMPLETADO EXITOSAMENTE")
        print(f"🎯 Recomendación: {resultado['impacto']['recomendacion'].upper()}")
        print(f"📊 Sentimiento: {resultado['impacto']['sentimiento_general'].upper()}")
    else:
        print(f"\n❌ Error: {resultado['error']}")

if __name__ == "__main__":
    main() 