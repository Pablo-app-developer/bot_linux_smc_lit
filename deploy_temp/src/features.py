"""
features.py - Detección OPTIMIZADA de estructuras SMC y LIT 
VERSIÓN ULTRA SENSIBLE para generar más señales rentables
"""

import pandas as pd
import numpy as np

class SMCFeatureExtractor:
    """
    Extrae estructuras clave del mercado según Smart Money Concepts (SMC):
    VERSIÓN OPTIMIZADA con parámetros más agresivos para más detecciones
    """
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()

    def detect_swings(self, lookback: int = 2):  # Reducido de 3 a 2
        """
        Detecta swing highs y swing lows MÁS SENSIBLES.
        """
        # Detección más agresiva con ventana más pequeña
        self.df['swing_high'] = self.df['high'] == self.df['high'].rolling(window=lookback*2+1, center=True).max()
        self.df['swing_low'] = self.df['low'] == self.df['low'].rolling(window=lookback*2+1, center=True).min()
        
        # NUEVA: Detectar también swing highs/lows locales (más sensible)
        self.df['local_high'] = (self.df['high'] > self.df['high'].shift(1)) & (self.df['high'] > self.df['high'].shift(-1))
        self.df['local_low'] = (self.df['low'] < self.df['low'].shift(1)) & (self.df['low'] < self.df['low'].shift(-1))
        
        return self.df

    def detect_choch_bos(self):
        """
        Detecta CHoCH y BOS con CRITERIOS MÁS PERMISIVOS.
        """
        self.df['choch'] = False
        self.df['bos'] = False
        
        for i in range(2, len(self.df)):
            # CHoCH: Cambio de tendencia (MÁS SENSIBLE)
            # CHoCH alcista: precio rompe por encima de swing high anterior
            if (self.df['swing_high'].iloc[i-2:i].any() and 
                self.df['close'].iloc[i] > self.df['high'].iloc[i-2:i].max()):
                self.df.at[self.df.index[i], 'choch'] = True
            
            # CHoCH bajista: precio rompe por debajo de swing low anterior
            if (self.df['swing_low'].iloc[i-2:i].any() and 
                self.df['close'].iloc[i] < self.df['low'].iloc[i-2:i].min()):
                self.df.at[self.df.index[i], 'choch'] = True
                
            # BOS: Ruptura de estructura (MÁS AGRESIVO)
            # BOS alcista: cierre por encima del máximo reciente
            if self.df['close'].iloc[i] > self.df['high'].iloc[i-3:i].max():
                self.df.at[self.df.index[i], 'bos'] = True
                
            # BOS bajista: cierre por debajo del mínimo reciente  
            if self.df['close'].iloc[i] < self.df['low'].iloc[i-3:i].min():
                self.df.at[self.df.index[i], 'bos'] = True
                
        return self.df

    def detect_order_blocks(self, window: int = 10):  # Reducido de 20 a 10
        """
        Detecta order blocks con MAYOR SENSIBILIDAD.
        """
        self.df['order_block'] = False
        self.df['order_block_bearish'] = False
        
        for i in range(window, len(self.df)):
            # Order block alcista: tras CHoCH/BOS alcista
            if (self.df['choch'].iloc[i-window:i].any() or self.df['bos'].iloc[i-window:i].any()):
                # Buscar vela con mayor volumen en ventana reducida
                recent_data = self.df.iloc[i-5:i]  # Ventana más pequeña
                if len(recent_data) > 0:
                    volume_col = 'volume' if 'volume' in recent_data.columns else 'tick_volume'
                    if volume_col in recent_data.columns:
                        max_vol_idx = recent_data[volume_col].idxmax()
                        self.df.at[max_vol_idx, 'order_block'] = True
            
            # Order block bajista
            if self.df['choch'].iloc[i-5:i].any():  # Ventana más pequeña
                recent_data = self.df.iloc[i-5:i]
                if len(recent_data) > 0:
                    volume_col = 'volume' if 'volume' in recent_data.columns else 'tick_volume'
                    if volume_col in recent_data.columns:
                        max_vol_idx = recent_data[volume_col].idxmax()
                        self.df.at[max_vol_idx, 'order_block_bearish'] = True
                        
        return self.df

    def detect_ranges(self, window: int = 10, threshold: float = 0.005):  # Más permisivo
        """
        Detecta rangos laterales con UMBRAL MÁS BAJO.
        """
        self.df['range'] = self.df['high'] - self.df['low']
        self.df['range_mean'] = self.df['range'].rolling(window=window).mean()
        self.df['in_range'] = (self.df['range'] < self.df['range_mean'] * (1 + threshold))
        return self.df

    def detect_liquidity_traps(self, window: int = 10, vol_ratio: float = 1.5):  # Más sensible
        """
        Detecta trampas de liquidez con CRITERIOS MÁS PERMISIVOS.
        """
        self.df['liquidity_trap'] = False
        self.df['liquidity_sweep'] = False
        
        for i in range(window, len(self.df)):
            # Trampa de liquidez: ruptura falsa con volumen alto
            if self.df['in_range'].iloc[i-5:i].any():  # Ventana reducida
                volume_col = 'volume' if 'volume' in self.df.columns else 'tick_volume'
                if volume_col in self.df.columns:
                    vol_avg = self.df[volume_col].iloc[i-10:i].mean()
                    if self.df[volume_col].iloc[i] > vol_avg * vol_ratio:
                        self.df.at[self.df.index[i], 'liquidity_trap'] = True
            
            # Liquidity sweep: barrido de máximos/mínimos
            recent_high = self.df['high'].iloc[i-5:i].max()
            recent_low = self.df['low'].iloc[i-5:i].min()
            
            if (self.df['high'].iloc[i] > recent_high * 1.0005 or  # 0.05% por encima
                self.df['low'].iloc[i] < recent_low * 0.9995):    # 0.05% por debajo
                self.df.at[self.df.index[i], 'liquidity_sweep'] = True
                
        return self.df

    def detect_fair_value_gaps(self):
        """
        NUEVA: Detecta Fair Value Gaps (FVG) alcistas y bajistas.
        """
        self.df['fvg_bullish'] = False
        self.df['fvg_bearish'] = False
        
        for i in range(2, len(self.df)):
            # FVG alcista: gap entre máximo de i-2 y mínimo de i
            if self.df['low'].iloc[i] > self.df['high'].iloc[i-2]:
                gap_size = self.df['low'].iloc[i] - self.df['high'].iloc[i-2]
                if gap_size > 0.0003:  # Umbral mínimo muy bajo
                    self.df.at[self.df.index[i], 'fvg_bullish'] = True
            
            # FVG bajista: gap entre mínimo de i-2 y máximo de i
            if self.df['high'].iloc[i] < self.df['low'].iloc[i-2]:
                gap_size = self.df['low'].iloc[i-2] - self.df['high'].iloc[i]
                if gap_size > 0.0003:  # Umbral mínimo muy bajo
                    self.df.at[self.df.index[i], 'fvg_bearish'] = True
                    
        return self.df

    def detect_market_structure_breaks(self):
        """
        NUEVA: Detecta rupturas de estructura de mercado adicionales.
        """
        self.df['structure_break_bull'] = False
        self.df['structure_break_bear'] = False
        
        for i in range(5, len(self.df)):
            # Ruptura alcista: precio por encima de resistencia
            resistance = self.df['high'].iloc[i-5:i].max()
            if self.df['close'].iloc[i] > resistance:
                self.df.at[self.df.index[i], 'structure_break_bull'] = True
                
            # Ruptura bajista: precio por debajo de soporte
            support = self.df['low'].iloc[i-5:i].min()
            if self.df['close'].iloc[i] < support:
                self.df.at[self.df.index[i], 'structure_break_bear'] = True
                
        return self.df

    def extract_all(self):
        """
        Extrae TODAS las features optimizadas para máxima sensibilidad.
        """
        self.detect_swings()
        self.detect_choch_bos()
        self.detect_order_blocks()
        self.detect_ranges()
        self.detect_liquidity_traps()
        self.detect_fair_value_gaps()
        self.detect_market_structure_breaks()
        return self.df

# Uso:
# extractor = SMCFeatureExtractor(df)
# df_features = extractor.extract_all()
