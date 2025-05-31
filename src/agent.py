"""
agent.py - Agente IA para el bot SMC-LIT
"""

import pandas as pd

class SMCAgent:
    """
    Agente que utiliza el modelo IA para tomar decisiones de trading y aprender del entorno.
    """
    def __init__(self, model, df: pd.DataFrame):
        self.model = model
        self.df = df.copy()
        self.actions = []

    def act(self):
        features = [
            'body_size', 'upper_wick', 'lower_wick', 'range', 'bullish',
            'sma_20', 'sma_50', 'sma_200', 'atr_14', 'volume_ratio',
            'swing_high', 'swing_low', 'choch', 'bos', 'order_block',
            'in_range', 'liquidity_trap'
        ]
        X = self.df[features].fillna(0).astype(float)
        preds = self.model.predict(X)
        self.df['ai_signal'] = preds
        self.actions = preds
        return self.df

# Uso:
# agent = SMCAgent(model, df_features)
# df_ai = agent.act() 