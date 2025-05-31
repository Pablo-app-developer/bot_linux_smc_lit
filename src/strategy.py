"""
strategy.py - Reglas de trading optimizadas basadas en SMC y LIT
"""

import pandas as pd
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

class SMCStrategy:
    """
    Estrategia de trading optimizada basada en señales SMC/LIT.
    """
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.trades = []
        
        # Parámetros optimizados desde .env
        self.swing_length = int(os.getenv('SMC_SWING_LENGTH', 10))
        self.ob_strength = int(os.getenv('SMC_ORDER_BLOCK_STRENGTH', 3))
        self.liq_threshold = float(os.getenv('SMC_LIQUIDITY_THRESHOLD', 0.0015))
        self.fvg_min_size = float(os.getenv('SMC_FVG_MIN_SIZE', 0.0008))

    def generate_signals(self):
        """
        Genera señales de entrada/salida optimizadas según patrones SMC/LIT.
        """
        self.df['signal'] = 0
        self.df['signal_strength'] = 0.0
        
        for i in range(self.swing_length, len(self.df)):
            signal_score = 0.0
            
            # === SEÑALES LONG (COMPRA) ===
            long_conditions = 0
            
            # 1. CHoCH alcista + Order Block válido
            if (self.df.get('choch', pd.Series([False]*len(self.df))).iloc[i-1] and 
                self.df.get('order_block', pd.Series([False]*len(self.df))).iloc[i]):
                long_conditions += 2
                signal_score += 0.3
            
            # 2. BOS (Break of Structure) alcista
            if self.df.get('bos', pd.Series([False]*len(self.df))).iloc[i]:
                long_conditions += 1
                signal_score += 0.2
            
            # 3. Fair Value Gap alcista
            if (self.df.get('fvg_bullish', pd.Series([False]*len(self.df))).iloc[i] and
                abs(self.df['high'].iloc[i] - self.df['low'].iloc[i-2]) > self.fvg_min_size):
                long_conditions += 1
                signal_score += 0.25
            
            # 4. Liquidez barrida (sweep de liquidez)
            if self.df.get('liquidity_sweep', pd.Series([False]*len(self.df))).iloc[i]:
                long_conditions += 1
                signal_score += 0.15
            
            # 5. Momentum alcista (RSI oversold recovery)
            if (self.df.get('rsi_14', pd.Series([50]*len(self.df))).iloc[i] > 35 and 
                self.df.get('rsi_14', pd.Series([50]*len(self.df))).iloc[i-1] < 30):
                long_conditions += 1
                signal_score += 0.1
                
            # === SEÑALES SHORT (VENTA) ===
            short_conditions = 0
            
            # 1. CHoCH bajista + Order Block válido
            if (self.df.get('choch', pd.Series([False]*len(self.df))).iloc[i-1] and 
                self.df.get('order_block_bearish', pd.Series([False]*len(self.df))).iloc[i]):
                short_conditions += 2
                signal_score -= 0.3
            
            # 2. Trampa de liquidez retail
            if self.df.get('liquidity_trap', pd.Series([False]*len(self.df))).iloc[i]:
                short_conditions += 2
                signal_score -= 0.25
            
            # 3. Fair Value Gap bajista
            if self.df.get('fvg_bearish', pd.Series([False]*len(self.df))).iloc[i]:
                short_conditions += 1
                signal_score -= 0.2
            
            # 4. Momentum bajista (RSI overbought rejection)
            if (self.df.get('rsi_14', pd.Series([50]*len(self.df))).iloc[i] < 65 and 
                self.df.get('rsi_14', pd.Series([50]*len(self.df))).iloc[i-1] > 70):
                short_conditions += 1
                signal_score -= 0.15
            
            # === FILTROS DE CONFIRMACIÓN ===
            # Filtro de volatilidad (ATR)
            atr_current = self.df.get('atr_14', pd.Series([0]*len(self.df))).iloc[i]
            atr_avg = self.df.get('atr_14', pd.Series([0]*len(self.df))).iloc[i-20:i].mean()
            
            if atr_current > atr_avg * 1.2:  # Alta volatilidad
                signal_score *= 1.1  # Amplificar señal
            elif atr_current < atr_avg * 0.8:  # Baja volatilidad
                signal_score *= 0.7  # Reducir señal
            
            # === ASIGNACIÓN DE SEÑALES ===
            # LONG: Necesita al menos 2 condiciones y score > 0.3
            if long_conditions >= 2 and signal_score > 0.3:
                self.df.at[self.df.index[i], 'signal'] = 1
                self.df.at[self.df.index[i], 'signal_strength'] = min(signal_score, 1.0)
            
            # SHORT: Necesita al menos 2 condiciones y score < -0.3
            elif short_conditions >= 2 and signal_score < -0.3:
                self.df.at[self.df.index[i], 'signal'] = -1
                self.df.at[self.df.index[i], 'signal_strength'] = max(signal_score, -1.0)
            
        return self.df

    def set_stop_loss_take_profit(self, sl_atr: float = 1.8, tp_atr: float = 2.5):
        """
        Define niveles de SL y TP dinámicos optimizados usando ATR.
        """
        self.df['stop_loss'] = np.nan
        self.df['take_profit'] = np.nan
        
        for i in range(len(self.df)):
            if self.df['signal'].iloc[i] == 1:  # LONG
                atr_val = self.df.get('atr_14', pd.Series([0.001]*len(self.df))).iloc[i]
                close_price = self.df['close'].iloc[i]
                
                # SL más conservador basado en estructura
                recent_low = self.df['low'].iloc[max(0, i-5):i+1].min()
                structure_sl = recent_low - (atr_val * 0.5)
                atr_sl = close_price - (sl_atr * atr_val)
                
                self.df.at[self.df.index[i], 'stop_loss'] = min(structure_sl, atr_sl)
                self.df.at[self.df.index[i], 'take_profit'] = close_price + (tp_atr * atr_val)
                
            elif self.df['signal'].iloc[i] == -1:  # SHORT
                atr_val = self.df.get('atr_14', pd.Series([0.001]*len(self.df))).iloc[i]
                close_price = self.df['close'].iloc[i]
                
                # SL más conservador basado en estructura
                recent_high = self.df['high'].iloc[max(0, i-5):i+1].max()
                structure_sl = recent_high + (atr_val * 0.5)
                atr_sl = close_price + (sl_atr * atr_val)
                
                self.df.at[self.df.index[i], 'stop_loss'] = max(structure_sl, atr_sl)
                self.df.at[self.df.index[i], 'take_profit'] = close_price - (tp_atr * atr_val)
                
        return self.df

    def apply_risk_filters(self):
        """
        Aplica filtros adicionales de gestión de riesgo.
        """
        # Evitar señales en rangos laterales
        for i in range(20, len(self.df)):
            price_range = self.df['high'].iloc[i-20:i].max() - self.df['low'].iloc[i-20:i].min()
            atr_avg = self.df.get('atr_14', pd.Series([0.001]*len(self.df))).iloc[i-20:i].mean()
            
            # Si el rango de precios es menor a 3 ATR, es un mercado lateral
            if price_range < (atr_avg * 3):
                self.df.at[self.df.index[i], 'signal'] = 0  # Cancelar señal
        
        # Evitar señales consecutivas muy próximas
        last_signal_idx = -1
        for i in range(len(self.df)):
            if self.df['signal'].iloc[i] != 0:
                if last_signal_idx != -1 and (i - last_signal_idx) < 5:
                    # Si hay menos de 5 velas desde la última señal, cancelar
                    self.df.at[self.df.index[i], 'signal'] = 0
                else:
                    last_signal_idx = i
        
        return self.df

    def run(self):
        """
        Ejecuta la estrategia completa optimizada.
        """
        self.generate_signals()
        self.set_stop_loss_take_profit()
        self.apply_risk_filters()
        return self.df

# Uso:
# strategy = SMCStrategy(df_features)
# df_signals = strategy.run() 