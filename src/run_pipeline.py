"""
run_pipeline.py - Pipeline maestro para optimización y entrenamiento del bot SMC-LIT
"""

import sys
import os

# Verificar entorno virtual
if not (
    (hasattr(sys, 'real_prefix')) or
    (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix) or
    ('VIRTUAL_ENV' in os.environ) or
    ('CONDA_DEFAULT_ENV' in os.environ)
):
    print("[ERROR] Este script debe ejecutarse dentro de un entorno virtual (venv o conda). Aborta.")
    sys.exit(1)

import pandas as pd
import numpy as np
from fetch_data import get_market_data
from features import SMCFeatureExtractor
from strategy import SMCStrategy
from backtester import Backtester
from trainer import SMCTrainer
from agent import SMCAgent
from utils import setup_logger
from ta.momentum import RSIIndicator
from ta.trend import MACD
import warnings
warnings.filterwarnings('ignore')

logger = setup_logger('pipeline')

# 1. Descargar datos desde FXCM
symbol = 'EUR/USD'
interval = 'm5'
period = '1000'
logger.info(f"Descargando datos FXCM para {symbol} {interval}")
df = get_market_data(symbol, interval=interval, period=period, source='fxcm')

# 2. Extraer features SMC/LIT y técnicos
logger.info("Extrayendo features SMC/LIT y técnicos")
features = SMCFeatureExtractor(df).extract_all()
# Añadir features técnicos populares
features['rsi_14'] = RSIIndicator(close=features['close'], window=14).rsi()
macd = MACD(close=features['close'])
features['macd'] = macd.macd()
features['macd_signal'] = macd.macd_signal()
features['macd_diff'] = macd.macd_diff()
features = features.fillna(0)

# 3. Optimización de parámetros (simple grid search sobre ATR y señales)
logger.info("Optimizando parámetros de estrategia")
best_pf = -np.inf
best_params = {}
best_signals = None
for sl_atr in [1.0, 1.5, 2.0]:
    for tp_atr in [1.5, 2.0, 3.0]:
        strategy = SMCStrategy(features)
        signals = strategy.run()
        signals = strategy.set_stop_loss_take_profit(sl_atr=sl_atr, tp_atr=tp_atr)
        bt = Backtester(signals)
        bt.simulate()
        metrics = bt.metrics()
        pf = metrics['profit_factor'] if not np.isnan(metrics['profit_factor']) else 0
        if pf > best_pf and metrics['num_trades'] > 5:
            best_pf = pf
            best_params = {'sl_atr': sl_atr, 'tp_atr': tp_atr}
            best_signals = signals.copy()
logger.info(f"Mejores parámetros: {best_params}, Profit Factor: {best_pf}")

# 4. Entrenamiento IA
logger.info("Entrenando modelo IA (XGBoost)")
trainer = SMCTrainer(best_signals)
model = trainer.train()

# 5. Agente IA y backtesting con señales IA
logger.info("Probando agente IA sobre datos")
agent = SMCAgent(model, features)
ai_df = agent.act()
ai_signals = best_signals.copy()
ai_signals['signal'] = ai_df['ai_signal']
bt_ai = Backtester(ai_signals)
bt_ai.simulate()
ai_metrics = bt_ai.metrics()

# 6. Reporte de métricas
logger.info("Resultados finales:")
logger.info(f"Estrategia SMC-LIT: {bt.metrics()}")
logger.info(f"Estrategia IA: {ai_metrics}")
print("\n--- Resultados ---")
print("Estrategia SMC-LIT:", bt.metrics())
print("Estrategia IA:", ai_metrics) 