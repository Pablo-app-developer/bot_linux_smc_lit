#!/usr/bin/env python3
# Wrapper del Filtro Inteligente para Bot SMC-LIT
# ==============================================

from intelligent_signal_filter import IntelligentSignalFilter
import json
from datetime import datetime
from typing import Dict, List, Optional

class BotSignalFilter:
    """Wrapper del filtro para integración fácil con el bot"""
    
    def __init__(self):
        self.filter = IntelligentSignalFilter()
        self.daily_approved_signals = []
    
    def should_execute_signal(self, signal_data: Dict) -> tuple[bool, float, str]:
        """
        Determinar si una señal debe ejecutarse
        
        Args:
            signal_data: Datos de la señal del bot
            
        Returns:
            (should_execute, score, reason)
        """
        try:
            # Convertir formato del bot al formato del filtro
            formatted_signal = self._format_signal_for_filter(signal_data)
            
            # Evaluar con el filtro inteligente
            approved, score, reason = self.filter.filter_signal(formatted_signal)
            
            if approved:
                self.daily_approved_signals.append({
                    'signal': formatted_signal,
                    'score': score,
                    'timestamp': datetime.now().isoformat()
                })
            
            return approved, score, reason
            
        except Exception as e:
            return False, 0.0, f"Error en filtro: {e}"
    
    def _format_signal_for_filter(self, bot_signal: Dict) -> Dict:
        """Convertir señal del bot al formato del filtro"""
        return {
            'symbol': bot_signal.get('symbol', bot_signal.get('pair', 'UNKNOWN')),
            'type': bot_signal.get('action', bot_signal.get('signal_type', 'BUY')),
            'smc_signal': bot_signal.get('smc_signal', 'NEUTRAL'),
            'rsi': bot_signal.get('rsi_signal', 'NEUTRAL'),
            'macd': bot_signal.get('macd_signal', 'NEUTRAL'),
            'ema': bot_signal.get('ema_signal', 'NEUTRAL'),
            'volume_analysis': bot_signal.get('volume', 'NEUTRAL'),
            'signal_strength': bot_signal.get('confidence', 0.5),
            'entry_price': bot_signal.get('entry_price', 0.0),
            'timestamp': bot_signal.get('timestamp', datetime.now().isoformat())
        }
    
    def get_daily_stats(self) -> Dict:
        """Obtener estadísticas del día"""
        return {
            'approved_signals': len(self.daily_approved_signals),
            'average_score': sum(s['score'] for s in self.daily_approved_signals) / len(self.daily_approved_signals) if self.daily_approved_signals else 0,
            'top_signals': sorted(self.daily_approved_signals, key=lambda x: x['score'], reverse=True)[:5]
        }

# Instancia global para uso fácil en el bot
signal_filter = BotSignalFilter()
