"""
features.py - Detección de estructuras SMC y LIT para el bot de trading SMC-LIT
"""

import pandas as pd
import numpy as np

class SMCFeatureExtractor:
    """
    Extrae estructuras clave del mercado según Smart Money Concepts (SMC):
    - Change of Character (CHoCH)
    - Break of Structure (BOS)
    - Order Blocks (OB)
    - Rangos
    - Zonas de liquidez (LIT)
    """
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def detect_swings(self, lookback: int = 3):
        """
        Detecta swing highs y swing lows para identificar puntos de estructura.
        """
        self.df['swing_high'] = self.df['high'] == self.df['high'].rolling(window=lookback*2+1, center=True).max()
        self.df['swing_low'] = self.df['low'] == self.df['low'].rolling(window=lookback*2+1, center=True).min()
        return self.df

    def detect_choch_bos(self):
        """
        Detecta cambios de carácter (CHoCH) y rupturas de estructura (BOS).
        """
        self.df['choch'] = False
        self.df['bos'] = False
        for i in range(2, len(self.df)):
            # CHoCH: cambio de tendencia (ejemplo simple)
            if self.df['swing_high'].iloc[i-1] and self.df['close'].iloc[i] < self.df['low'].iloc[i-1]:
                self.df.at[self.df.index[i], 'choch'] = True
            if self.df['swing_low'].iloc[i-1] and self.df['close'].iloc[i] > self.df['high'].iloc[i-1]:
                self.df.at[self.df.index[i], 'choch'] = True
            # BOS: ruptura de estructura
            if self.df['swing_high'].iloc[i-1] and self.df['close'].iloc[i] > self.df['high'].iloc[i-1]:
                self.df.at[self.df.index[i], 'bos'] = True
            if self.df['swing_low'].iloc[i-1] and self.df['close'].iloc[i] < self.df['low'].iloc[i-1]:
                self.df.at[self.df.index[i], 'bos'] = True
        return self.df

    def detect_order_blocks(self, window: int = 20):
        """
        Detecta order blocks simples como zonas de reversión tras CHoCH/BOS.
        """
        self.df['order_block'] = False
        for i in range(window, len(self.df)):
            if self.df['choch'].iloc[i-window:i].any() or self.df['bos'].iloc[i-window:i].any():
                # Order block: vela con mayor volumen tras ruptura
                idx = self.df.iloc[i-window:i].volume.idxmax()
                self.df.at[idx, 'order_block'] = True
        return self.df

    def detect_ranges(self, window: int = 20, threshold: float = 0.01):
        """
        Detecta rangos laterales por baja volatilidad relativa.
        """
        self.df['range'] = self.df['high'] - self.df['low']
        self.df['range_mean'] = self.df['range'].rolling(window=window).mean()
        self.df['in_range'] = (self.df['range'] < self.df['range_mean'] * (1 + threshold))
        return self.df

    def detect_liquidity_traps(self, window: int = 20, vol_ratio: float = 2.0):
        """
        Detecta trampas de liquidez (LIT) como rupturas falsas con volumen anómalo.
        """
        self.df['liquidity_trap'] = False
        for i in range(window, len(self.df)):
            if self.df['in_range'].iloc[i-window:i].all():
                # Ruptura con volumen alto
                if self.df['volume'].iloc[i] > self.df['volume_sma_20'].iloc[i] * vol_ratio:
                    self.df.at[self.df.index[i], 'liquidity_trap'] = True
        return self.df

    def extract_all(self):
        self.detect_swings()
        self.detect_choch_bos()
        self.detect_order_blocks()
        self.detect_ranges()
        self.detect_liquidity_traps()
        return self.df

# Uso:
# extractor = SMCFeatureExtractor(df)
# df_features = extractor.extract_all()
