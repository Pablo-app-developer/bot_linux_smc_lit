"""
strategy.py - Reglas de trading optimizadas basadas en SMC y LIT
VERSIÓN OPTIMIZADA PARA MÁXIMA RENTABILIDAD
"""

import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

class SMCStrategy:
    """
    Estrategia de trading ULTRA OPTIMIZADA basada en señales SMC/LIT.
    Parámetros ajustados para máxima rentabilidad y más trades.
    """
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.trades = []
        
        # Parámetros ULTRA AGRESIVOS para más trades
        self.swing_length = 3              # Reducido de 10 a 3
        self.ob_strength = 1               # Reducido de 3 a 1
        self.liq_threshold = 0.0005        # Reducido de 0.0015 a 0.0005
        self.fvg_min_size = 0.0003         # Reducido de 0.0008 a 0.0003

    def generate_signals(self):
        """
        Genera señales OPTIMIZADAS con umbrales más bajos para más trades.
        """
        self.df['signal'] = 0
        self.df['signal_strength'] = 0.0
        
        for i in range(self.swing_length, len(self.df)):
            signal_score = 0.0
            
            # === SEÑALES LONG (COMPRA) - MÁS SENSIBLES ===
            long_conditions = 0
            
            # 1. CHoCH alcista + Order Block (PESO AUMENTADO)
            if (self.df.get('choch', pd.Series([False]*len(self.df))).iloc[i-1] and 
                self.df.get('order_block', pd.Series([False]*len(self.df))).iloc[i]):
                long_conditions += 1
                signal_score += 0.4  # Aumentado de 0.3 a 0.4
            
            # 2. BOS (Break of Structure) alcista (MÁS PESO)
            if self.df.get('bos', pd.Series([False]*len(self.df))).iloc[i]:
                long_conditions += 1
                signal_score += 0.35  # Aumentado de 0.2 a 0.35
            
            # 3. Fair Value Gap alcista (UMBRAL REDUCIDO)
            gap_size = abs(self.df['high'].iloc[i] - self.df['low'].iloc[max(0, i-2)])
            if (self.df.get('fvg_bullish', pd.Series([False]*len(self.df))).iloc[i] and
                gap_size > self.fvg_min_size):
                long_conditions += 1
                signal_score += 0.3  # Aumentado de 0.25 a 0.3
            
            # 4. Liquidez barrida (MÁS SENSIBLE)
            if self.df.get('liquidity_sweep', pd.Series([False]*len(self.df))).iloc[i]:
                long_conditions += 1
                signal_score += 0.25  # Aumentado de 0.15 a 0.25
            
            # 5. Momentum alcista (UMBRAL MÁS BAJO)
            rsi_current = self.df.get('rsi_14', pd.Series([50]*len(self.df))).iloc[i]
            rsi_prev = self.df.get('rsi_14', pd.Series([50]*len(self.df))).iloc[i-1]
            if (rsi_current > 25 and rsi_prev < 20):  # Umbrales más bajos
                long_conditions += 1
                signal_score += 0.2
            
            # 6. NUEVA: Precio cerca de mínimos recientes
            recent_low = self.df['low'].iloc[max(0, i-5):i].min()
            if self.df['close'].iloc[i] <= recent_low * 1.001:  # Dentro del 0.1%
                long_conditions += 1
                signal_score += 0.15
                
            # === SEÑALES SHORT (VENTA) - MÁS SENSIBLES ===
            short_conditions = 0
            
            # 1. CHoCH bajista + Order Block
            if (self.df.get('choch', pd.Series([False]*len(self.df))).iloc[i-1] and 
                self.df.get('order_block_bearish', pd.Series([False]*len(self.df))).iloc[i]):
                short_conditions += 1
                signal_score -= 0.4
            
            # 2. Trampa de liquidez retail (MÁS PESO)
            if self.df.get('liquidity_trap', pd.Series([False]*len(self.df))).iloc[i]:
                short_conditions += 1
                signal_score -= 0.35
            
            # 3. Fair Value Gap bajista
            if self.df.get('fvg_bearish', pd.Series([False]*len(self.df))).iloc[i]:
                short_conditions += 1
                signal_score -= 0.3
            
            # 4. Momentum bajista (UMBRAL MÁS ALTO)
            if (rsi_current < 75 and rsi_prev > 80):  # Umbrales más extremos
                short_conditions += 1
                signal_score -= 0.25
            
            # 5. NUEVA: Precio cerca de máximos recientes
            recent_high = self.df['high'].iloc[max(0, i-5):i].max()
            if self.df['close'].iloc[i] >= recent_high * 0.999:  # Dentro del 0.1%
                short_conditions += 1
                signal_score -= 0.15
            
            # === FILTROS SIMPLIFICADOS ===
            # Filtro de volatilidad (MÁS PERMISIVO)
            atr_current = self.df.get('atr_14', pd.Series([0.001]*len(self.df))).iloc[i]
            atr_avg = self.df.get('atr_14', pd.Series([0.001]*len(self.df))).iloc[max(0, i-10):i].mean()
            
            if atr_current > atr_avg * 0.8:  # Muy permisivo
                signal_score *= 1.1
            
            # === ASIGNACIÓN DE SEÑALES (UMBRALES REDUCIDOS) ===
            # LONG: Solo necesita 1 condición y score > 0.15
            if long_conditions >= 1 and signal_score > 0.15:
                self.df.at[self.df.index[i], 'signal'] = 1
                self.df.at[self.df.index[i], 'signal_strength'] = min(signal_score, 1.0)
            
            # SHORT: Solo necesita 1 condición y score < -0.15
            elif short_conditions >= 1 and signal_score < -0.15:
                self.df.at[self.df.index[i], 'signal'] = -1
                self.df.at[self.df.index[i], 'signal_strength'] = max(signal_score, -1.0)
            
        return self.df

    def set_stop_loss_take_profit(self, sl_atr: float = 1.0, tp_atr: float = 2.5):
        """
        SL/TP OPTIMIZADOS: SL más cerrado, TP más amplio para mejor R:R.
        """
        self.df['stop_loss'] = np.nan
        self.df['take_profit'] = np.nan
        
        for i in range(len(self.df)):
            if self.df['signal'].iloc[i] == 1:  # LONG
                atr_val = self.df.get('atr_14', pd.Series([0.001]*len(self.df))).iloc[i]
                close_price = self.df['close'].iloc[i]
                
                # SL más agresivo (más cerca)
                self.df.at[self.df.index[i], 'stop_loss'] = close_price - (sl_atr * atr_val)
                self.df.at[self.df.index[i], 'take_profit'] = close_price + (tp_atr * atr_val)
                
            elif self.df['signal'].iloc[i] == -1:  # SHORT
                atr_val = self.df.get('atr_14', pd.Series([0.001]*len(self.df))).iloc[i]
                close_price = self.df['close'].iloc[i]
                
                # SL más agresivo (más cerca)
                self.df.at[self.df.index[i], 'stop_loss'] = close_price + (sl_atr * atr_val)
                self.df.at[self.df.index[i], 'take_profit'] = close_price - (tp_atr * atr_val)
                
        return self.df

    def apply_risk_filters(self):
        """
        Filtros de riesgo SIMPLIFICADOS para permitir más trades.
        """
        # Evitar señales consecutivas MUY próximas (reducido a 2 velas)
        last_signal_idx = -1
        for i in range(len(self.df)):
            if self.df['signal'].iloc[i] != 0:
                if last_signal_idx != -1 and (i - last_signal_idx) < 2:  # Reducido de 5 a 2
                    # Mantener la señal más fuerte
                    if abs(self.df['signal_strength'].iloc[i]) > abs(self.df['signal_strength'].iloc[last_signal_idx]):
                        self.df.at[self.df.index[last_signal_idx], 'signal'] = 0
                        last_signal_idx = i
                    else:
                        self.df.at[self.df.index[i], 'signal'] = 0
                else:
                    last_signal_idx = i
        
        return self.df

    def run(self):
        """
        Ejecuta la estrategia ULTRA OPTIMIZADA.
        """
        self.generate_signals()
        self.set_stop_loss_take_profit()
        self.apply_risk_filters()
        return self.df

# Uso:
# strategy = SMCStrategy(df_features)
# df_signals = strategy.run() 