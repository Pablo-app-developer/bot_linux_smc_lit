"""
trainer.py - Entrenamiento de modelos IA para el bot SMC-LIT
"""

import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

class SMCTrainer:
    """
    Entrena un modelo XGBoost para predecir señales de trading basadas en features SMC/LIT.
    """
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.model = None

    def prepare_data(self):
        features = [
            'body_size', 'upper_wick', 'lower_wick', 'range', 'bullish',
            'sma_20', 'sma_50', 'sma_200', 'atr_14', 'volume_ratio',
            'swing_high', 'swing_low', 'choch', 'bos', 'order_block',
            'in_range', 'liquidity_trap'
        ]
        X = self.df[features].fillna(0).astype(float)
        y = (self.df['signal'] != 0).astype(int)  # 1 si hay señal, 0 si no
        return train_test_split(X, y, test_size=0.2, random_state=42)

    def train(self):
        X_train, X_test, y_train, y_test = self.prepare_data()
        self.model = XGBClassifier(use_label_encoder=False, eval_metric='logloss')
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)
        print(classification_report(y_test, y_pred))
        return self.model

# Uso:
# trainer = SMCTrainer(df_signals)
# model = trainer.train() 