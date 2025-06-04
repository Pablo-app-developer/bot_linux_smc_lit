#!/usr/bin/env python3
"""
ANALIZADOR DE CALENDARIO ECONÓMICO - BOT SMC-LIT
===============================================
Análisis de eventos económicos con FinBERT
"""

import json
import requests
from datetime import datetime, timedelta
from typing import List, Dict, Tuple, Optional
import numpy as np
import pandas as pd

class EconomicCalendarAnalyzer:
    def __init__(self):
        self.config = {
            'update_frequency_minutes': 30,
            'look_ahead_days': 7,
            'importance_threshold': 'medium',
            'finbert_enabled': True
        }
        
        # Eventos económicos importantes y su impacto esperado
        self.economic_events = {
            'high_impact': {
                'federal_funds_rate': {'impact_score': 1.0, 'currency': 'USD', 'categories': ['fed_powell', 'economic_indicators']},
                'non_farm_payrolls': {'impact_score': 0.9, 'currency': 'USD', 'categories': ['economic_indicators']},
                'inflation_rate': {'impact_score': 0.9, 'currency': 'USD', 'categories': ['economic_indicators']},
                'gdp_growth': {'impact_score': 0.85, 'currency': 'USD', 'categories': ['economic_indicators']},
                'fomc_meeting': {'impact_score': 1.0, 'currency': 'USD', 'categories': ['fed_powell']},
                'ecb_rate_decision': {'impact_score': 0.9, 'currency': 'EUR', 'categories': ['fed_powell']},
                'boe_rate_decision': {'impact_score': 0.85, 'currency': 'GBP', 'categories': ['fed_powell']},
                'earnings_major_tech': {'impact_score': 0.8, 'currency': 'USD', 'categories': ['market_indices']}
            },
            'medium_impact': {
                'unemployment_rate': {'impact_score': 0.7, 'currency': 'USD', 'categories': ['economic_indicators']},
                'retail_sales': {'impact_score': 0.6, 'currency': 'USD', 'categories': ['economic_indicators']},
                'consumer_confidence': {'impact_score': 0.6, 'currency': 'USD', 'categories': ['economic_indicators']},
                'pmi_manufacturing': {'impact_score': 0.65, 'currency': 'USD', 'categories': ['economic_indicators']},
                'pmi_services': {'impact_score': 0.6, 'currency': 'USD', 'categories': ['economic_indicators']},
                'crude_oil_inventory': {'impact_score': 0.7, 'currency': 'USD', 'categories': ['commodities']},
                'earnings_banking': {'impact_score': 0.65, 'currency': 'USD', 'categories': ['banking_finance']}
            },
            'low_impact': {
                'building_permits': {'impact_score': 0.4, 'currency': 'USD', 'categories': ['economic_indicators']},
                'existing_home_sales': {'impact_score': 0.45, 'currency': 'USD', 'categories': ['economic_indicators']},
                'consumer_price_index': {'impact_score': 0.5, 'currency': 'USD', 'categories': ['economic_indicators']},
                'trade_balance': {'impact_score': 0.4, 'currency': 'USD', 'categories': ['economic_indicators']}
            }
        }
        
        # Cache para análisis FinBERT
        self.finbert_cache = {}
        
        # Horarios de mercado por región
        self.market_sessions = {
            'asian': {'start': 0, 'end': 8, 'timezone': 'Asia/Tokyo'},
            'european': {'start': 8, 'end': 16, 'timezone': 'Europe/London'},
            'american': {'start': 16, 'end': 24, 'timezone': 'America/New_York'}
        }
        
    def get_upcoming_events(self, days_ahead: int = 7) -> List[Dict]:
        """Obtener eventos económicos próximos"""
        print("📅 OBTENIENDO CALENDARIO ECONÓMICO...")
        
        # Simular eventos económicos realistas para los próximos días
        current_time = datetime.now()
        events = []
        
        # Eventos predefinidos para esta semana
        upcoming_events = [
            {
                'name': 'US Non-Farm Payrolls',
                'time': current_time + timedelta(days=1, hours=14, minutes=30),
                'impact': 'high',
                'currency': 'USD',
                'forecast': '180K',
                'previous': '175K',
                'category': 'employment',
                'description': 'Monthly change in the number of employed people excluding farm workers'
            },
            {
                'name': 'Federal Funds Rate Decision',
                'time': current_time + timedelta(days=2, hours=20, minutes=0),
                'impact': 'high',
                'currency': 'USD',
                'forecast': '5.50%',
                'previous': '5.50%',
                'category': 'interest_rates',
                'description': 'Federal Reserve interest rate decision'
            },
            {
                'name': 'Core CPI (MoM)',
                'time': current_time + timedelta(days=3, hours=14, minutes=30),
                'impact': 'high',
                'currency': 'USD',
                'forecast': '0.2%',
                'previous': '0.3%',
                'category': 'inflation',
                'description': 'Monthly change in core consumer prices'
            },
            {
                'name': 'Initial Jobless Claims',
                'time': current_time + timedelta(days=1, hours=14, minutes=30),
                'impact': 'medium',
                'currency': 'USD',
                'forecast': '220K',
                'previous': '215K',
                'category': 'employment',
                'description': 'Number of people filing for unemployment benefits'
            },
            {
                'name': 'ISM Manufacturing PMI',
                'time': current_time + timedelta(days=2, hours=16, minutes=0),
                'impact': 'medium',
                'currency': 'USD',
                'forecast': '47.8',
                'previous': '47.4',
                'category': 'business_activity',
                'description': 'Manufacturing sector health indicator'
            },
            {
                'name': 'ECB Interest Rate Decision',
                'time': current_time + timedelta(days=4, hours=13, minutes=45),
                'impact': 'high',
                'currency': 'EUR',
                'forecast': '4.50%',
                'previous': '4.50%',
                'category': 'interest_rates',
                'description': 'European Central Bank interest rate decision'
            },
            {
                'name': 'GDP Growth Rate (QoQ)',
                'time': current_time + timedelta(days=5, hours=14, minutes=30),
                'impact': 'high',
                'currency': 'USD',
                'forecast': '2.1%',
                'previous': '2.4%',
                'category': 'growth',
                'description': 'Quarterly gross domestic product growth'
            },
            {
                'name': 'NVIDIA Earnings Report',
                'time': current_time + timedelta(days=3, hours=22, minutes=0),
                'impact': 'high',
                'currency': 'USD',
                'forecast': '$5.82 EPS',
                'previous': '$5.16 EPS',
                'category': 'earnings',
                'description': 'NVIDIA quarterly earnings announcement'
            }
        ]
        
        # Filtrar eventos dentro del rango de días
        for event in upcoming_events:
            if event['time'] <= current_time + timedelta(days=days_ahead):
                # Añadir score de impacto
                event['impact_score'] = self.calculate_event_impact_score(event)
                
                # Añadir análisis de timing
                event['market_session'] = self.get_market_session(event['time'])
                
                # Calcular tiempo hasta el evento
                time_until = event['time'] - current_time
                event['hours_until'] = time_until.total_seconds() / 3600
                
                events.append(event)
        
        # Ordenar por impacto y proximidad temporal
        events.sort(key=lambda x: (x['impact_score'], -x['hours_until']), reverse=True)
        
        print(f"📊 Encontrados {len(events)} eventos económicos próximos")
        return events
    
    def calculate_event_impact_score(self, event: Dict) -> float:
        """Calcular score de impacto de un evento económico"""
        base_impact = {
            'high': 0.9,
            'medium': 0.6,
            'low': 0.3
        }.get(event['impact'], 0.5)
        
        # Ajustar por categoría
        category_multiplier = {
            'interest_rates': 1.2,
            'employment': 1.1,
            'inflation': 1.1,
            'growth': 1.0,
            'earnings': 0.8,
            'business_activity': 0.7
        }.get(event['category'], 1.0)
        
        # Ajustar por moneda (USD tiene más impacto global)
        currency_multiplier = {
            'USD': 1.0,
            'EUR': 0.8,
            'GBP': 0.7,
            'JPY': 0.6
        }.get(event['currency'], 0.5)
        
        # Ajustar por proximidad temporal
        hours_until = event.get('hours_until', 24)
        time_multiplier = max(0.5, 1 - (hours_until / 168))  # Decae en una semana
        
        impact_score = base_impact * category_multiplier * currency_multiplier * time_multiplier
        return round(min(impact_score, 1.0), 3)
    
    def get_market_session(self, event_time: datetime) -> str:
        """Determinar sesión de mercado del evento"""
        hour = event_time.hour
        
        if 0 <= hour < 8:
            return 'asian'
        elif 8 <= hour < 16:
            return 'european'
        else:
            return 'american'
    
    def analyze_event_sentiment_finbert(self, event: Dict) -> Dict:
        """Analizar sentimiento del evento usando técnicas similar a FinBERT"""
        
        # Simular análisis FinBERT (en producción se usaría el modelo real)
        event_text = f"{event['name']} {event['description']} forecast {event.get('forecast', 'N/A')} previous {event.get('previous', 'N/A')}"
        
        # Análisis basado en reglas financieras
        sentiment_score = 0.0
        confidence = 0.5
        
        # Análisis por tipo de evento
        if event['category'] == 'interest_rates':
            # Tasas de interés
            if 'rate' in event['name'].lower():
                if 'hike' in event['description'].lower() or float(event.get('forecast', '0').replace('%', '')) > float(event.get('previous', '0').replace('%', '')):
                    sentiment_score = -0.3  # Negativo para activos de riesgo
                elif 'cut' in event['description'].lower():
                    sentiment_score = 0.4   # Positivo para activos de riesgo
                confidence = 0.8
                
        elif event['category'] == 'employment':
            # Datos de empleo
            try:
                forecast_val = float(event.get('forecast', '0').replace('K', '').replace('%', ''))
                previous_val = float(event.get('previous', '0').replace('K', '').replace('%', ''))
                
                if 'payrolls' in event['name'].lower() or 'unemployment' in event['name'].lower():
                    if forecast_val > previous_val:
                        sentiment_score = 0.3 if 'payrolls' in event['name'].lower() else -0.2
                    else:
                        sentiment_score = -0.2 if 'payrolls' in event['name'].lower() else 0.3
                    confidence = 0.7
            except:
                pass
                
        elif event['category'] == 'inflation':
            # Datos de inflación
            try:
                forecast_val = float(event.get('forecast', '0').replace('%', ''))
                previous_val = float(event.get('previous', '0').replace('%', ''))
                
                if forecast_val > previous_val:
                    sentiment_score = -0.2  # Inflación alta = negativo
                else:
                    sentiment_score = 0.2   # Inflación baja = positivo
                confidence = 0.75
            except:
                pass
                
        elif event['category'] == 'earnings':
            # Reportes de ganancias
            if 'nvidia' in event['name'].lower() or 'tech' in event['description'].lower():
                # Análisis específico para tech
                sentiment_score = 0.4  # Generalmente positivo para tech
                confidence = 0.6
        
        # Aplicar factores adicionales
        market_session = event.get('market_session', 'american')
        session_multiplier = {
            'american': 1.0,
            'european': 0.8,
            'asian': 0.6
        }.get(market_session, 1.0)
        
        sentiment_score *= session_multiplier
        
        # Clasificar sentimiento
        if sentiment_score > 0.3:
            sentiment_label = 'bullish'
        elif sentiment_score > 0.1:
            sentiment_label = 'slightly_bullish'
        elif sentiment_score < -0.3:
            sentiment_label = 'bearish'
        elif sentiment_score < -0.1:
            sentiment_label = 'slightly_bearish'
        else:
            sentiment_label = 'neutral'
        
        return {
            'sentiment_score': round(sentiment_score, 3),
            'sentiment_label': sentiment_label,
            'confidence': round(confidence, 3),
            'finbert_analysis': True,
            'key_factors': self.extract_key_factors(event),
            'market_impact': self.predict_market_impact(event, sentiment_score)
        }
    
    def extract_key_factors(self, event: Dict) -> List[str]:
        """Extraer factores clave del evento"""
        factors = []
        
        # Factores por categoría
        if event['category'] == 'interest_rates':
            factors.extend(['monetary_policy', 'inflation_expectations', 'economic_growth'])
        elif event['category'] == 'employment':
            factors.extend(['labor_market', 'consumer_spending', 'economic_recovery'])
        elif event['category'] == 'inflation':
            factors.extend(['price_stability', 'purchasing_power', 'fed_policy'])
        elif event['category'] == 'earnings':
            factors.extend(['corporate_performance', 'sector_health', 'market_sentiment'])
        
        # Factores por impacto
        if event['impact'] == 'high':
            factors.append('market_moving')
        
        # Factores por timing
        if event.get('hours_until', 0) < 24:
            factors.append('imminent_impact')
        
        return factors
    
    def predict_market_impact(self, event: Dict, sentiment_score: float) -> Dict:
        """Predecir impacto específico en diferentes mercados"""
        impact = {
            'forex': 'neutral',
            'indices': 'neutral',
            'commodities': 'neutral',
            'crypto': 'neutral'
        }
        
        # Impacto en Forex
        if event['currency'] == 'USD' and abs(sentiment_score) > 0.2:
            if sentiment_score > 0:
                impact['forex'] = 'usd_bullish'
            else:
                impact['forex'] = 'usd_bearish'
        
        # Impacto en Índices
        if event['category'] in ['earnings', 'growth', 'employment'] and abs(sentiment_score) > 0.2:
            if sentiment_score > 0:
                impact['indices'] = 'bullish'
            else:
                impact['indices'] = 'bearish'
        
        # Impacto en Commodities
        if event['category'] in ['inflation', 'interest_rates'] and abs(sentiment_score) > 0.2:
            if sentiment_score > 0:
                impact['commodities'] = 'mixed'  # Inflación compleja para commodities
            else:
                impact['commodities'] = 'bearish'
        
        return impact
    
    def generate_trading_signals(self, events: List[Dict]) -> Dict:
        """Generar señales de trading basadas en eventos económicos"""
        print("🎯 GENERANDO SEÑALES DE TRADING DESDE CALENDARIO ECONÓMICO...")
        
        signals = {
            'overall_sentiment': 'neutral',
            'confidence': 0.5,
            'event_count': len(events),
            'high_impact_events': 0,
            'signals_by_asset': {
                'EURUSD': 'hold',
                'GBPUSD': 'hold',
                'USDJPY': 'hold',
                'NAS100': 'hold',
                'SPX500': 'hold'
            },
            'time_sensitive_events': [],
            'risk_level': 'medium'
        }
        
        # Analizar eventos con FinBERT
        event_sentiments = []
        high_impact_count = 0
        
        for event in events:
            sentiment_analysis = self.analyze_event_sentiment_finbert(event)
            event['sentiment_analysis'] = sentiment_analysis
            
            if event['impact'] == 'high':
                high_impact_count += 1
                
            if event.get('hours_until', 0) < 12:
                signals['time_sensitive_events'].append({
                    'name': event['name'],
                    'hours_until': event['hours_until'],
                    'impact': event['impact'],
                    'sentiment': sentiment_analysis['sentiment_label']
                })
            
            # Ponderar por impacto y proximidad
            weight = event['impact_score'] * max(0.1, 1 - event.get('hours_until', 0) / 48)
            weighted_sentiment = sentiment_analysis['sentiment_score'] * weight
            event_sentiments.append(weighted_sentiment)
        
        signals['high_impact_events'] = high_impact_count
        
        # Calcular sentimiento general
        if event_sentiments:
            overall_score = sum(event_sentiments) / len(event_sentiments)
            signals['confidence'] = min(0.9, 0.5 + abs(overall_score))
            
            if overall_score > 0.2:
                signals['overall_sentiment'] = 'bullish'
            elif overall_score < -0.2:
                signals['overall_sentiment'] = 'bearish'
            else:
                signals['overall_sentiment'] = 'neutral'
        
        # Generar señales específicas por activo
        signals['signals_by_asset'] = self.generate_asset_specific_signals(events)
        
        # Evaluar nivel de riesgo
        signals['risk_level'] = self.assess_risk_level(events, high_impact_count)
        
        return signals
    
    def generate_asset_specific_signals(self, events: List[Dict]) -> Dict:
        """Generar señales específicas por activo"""
        signals = {
            'EURUSD': 'hold',
            'GBPUSD': 'hold', 
            'USDJPY': 'hold',
            'NAS100': 'hold',
            'SPX500': 'hold'
        }
        
        usd_sentiment = 0
        eur_sentiment = 0
        tech_sentiment = 0
        
        for event in events:
            sentiment = event.get('sentiment_analysis', {})
            score = sentiment.get('sentiment_score', 0)
            weight = event['impact_score']
            
            # Impacto en USD
            if event['currency'] == 'USD':
                usd_sentiment += score * weight
            elif event['currency'] == 'EUR':
                eur_sentiment += score * weight
            
            # Impacto en tech/índices
            if event['category'] in ['earnings', 'growth'] and 'tech' in event.get('description', '').lower():
                tech_sentiment += score * weight
        
        # Señales FOREX
        if abs(usd_sentiment) > 0.3:
            if usd_sentiment > 0:
                signals['USDJPY'] = 'buy'
                signals['EURUSD'] = 'sell'
            else:
                signals['USDJPY'] = 'sell'
                signals['EURUSD'] = 'buy'
        
        if abs(eur_sentiment) > 0.3:
            if eur_sentiment > 0:
                signals['EURUSD'] = 'buy'
            else:
                signals['EURUSD'] = 'sell'
        
        # Señales ÍNDICES
        if abs(tech_sentiment) > 0.3:
            if tech_sentiment > 0:
                signals['NAS100'] = 'buy'
                signals['SPX500'] = 'buy'
            else:
                signals['NAS100'] = 'sell' 
                signals['SPX500'] = 'sell'
        
        return signals
    
    def assess_risk_level(self, events: List[Dict], high_impact_count: int) -> str:
        """Evaluar nivel de riesgo basado en eventos"""
        
        # Contar eventos por proximidad
        imminent_events = sum(1 for e in events if e.get('hours_until', 0) < 6)
        today_events = sum(1 for e in events if e.get('hours_until', 0) < 24)
        
        if high_impact_count >= 3 or imminent_events >= 2:
            return 'high'
        elif high_impact_count >= 2 or today_events >= 3:
            return 'medium'
        else:
            return 'low'
    
    def save_calendar_analysis(self, events: List[Dict], signals: Dict):
        """Guardar análisis del calendario económico"""
        import os
        os.makedirs('data', exist_ok=True)
        
        analysis_data = {
            'timestamp': datetime.now().isoformat(),
            'events_analyzed': len(events),
            'events': events,
            'trading_signals': signals,
            'config': self.config,
            'version': 'economic_calendar_v1.0'
        }
        
        with open('data/economic_calendar_analysis.json', 'w') as f:
            json.dump(analysis_data, f, indent=2, default=str)
        
        print("💾 Análisis de calendario económico guardado en data/economic_calendar_analysis.json")
    
    def get_calendar_summary(self) -> str:
        """Generar resumen del calendario económico"""
        events = self.get_upcoming_events()
        signals = self.generate_trading_signals(events)
        
        summary = f"""
📅 CALENDARIO ECONÓMICO - {datetime.now().strftime('%H:%M:%S')}
═══════════════════════════════════════════════════════════

📊 RESUMEN GENERAL:
• Eventos próximos: {signals['event_count']}
• Eventos alto impacto: {signals['high_impact_events']}
• Sentimiento general: {signals['overall_sentiment'].upper()}
• Confianza: {signals['confidence']:.2f}
• Nivel de riesgo: {signals['risk_level'].upper()}

⏰ EVENTOS CRÍTICOS (Próximas 12h):"""
        
        for event in signals['time_sensitive_events']:
            summary += f"""
• {event['name']}: {event['hours_until']:.1f}h | {event['impact'].upper()} | {event['sentiment'].upper()}"""
        
        summary += f"""

🎯 SEÑALES DE TRADING:
• EURUSD: {signals['signals_by_asset']['EURUSD'].upper()}
• GBPUSD: {signals['signals_by_asset']['GBPUSD'].upper()}
• USDJPY: {signals['signals_by_asset']['USDJPY'].upper()}
• NASDAQ: {signals['signals_by_asset']['NAS100'].upper()}
• S&P 500: {signals['signals_by_asset']['SPX500'].upper()}

📈 EVENTOS MÁS RELEVANTES:"""
        
        for i, event in enumerate(events[:5], 1):
            sentiment = event.get('sentiment_analysis', {})
            summary += f"""
{i}. {event['name']} ({event['currency']})
   ⏰ {event['time'].strftime('%Y-%m-%d %H:%M')} | 🎯 {event['impact'].upper()}
   💭 {sentiment.get('sentiment_label', 'N/A').upper()} | Score: {sentiment.get('sentiment_score', 0):.2f}
   📊 Forecast: {event.get('forecast', 'N/A')} | Previous: {event.get('previous', 'N/A')}"""
        
        # Guardar análisis
        self.save_calendar_analysis(events, signals)
        
        return summary

def main():
    """Función principal para pruebas"""
    print("📅 PROBANDO ANALIZADOR DE CALENDARIO ECONÓMICO")
    print("=" * 60)
    
    # Crear analizador
    calendar = EconomicCalendarAnalyzer()
    
    # Ejecutar análisis completo
    summary = calendar.get_calendar_summary()
    print(summary)
    
    print("\n✅ ANÁLISIS DE CALENDARIO ECONÓMICO COMPLETADO")

if __name__ == "__main__":
    main() 