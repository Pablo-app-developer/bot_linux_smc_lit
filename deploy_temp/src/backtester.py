"""
backtester.py - Simulador de backtesting profesional para SMC-LIT
"""

import pandas as pd
import numpy as np

class Backtester:
    """
    Simula la ejecución de señales y calcula métricas clave.
    """
    def __init__(self, df: pd.DataFrame):
        self.df = df.copy()
        self.results = []

    def simulate(self):
        capital = 10000
        position = 0
        entry_price = 0
        equity_curve = [capital]
        trades = []
        for i in range(len(self.df)):
            row = self.df.iloc[i]
            if row['signal'] == 1 and position == 0:
                position = 1
                entry_price = row['close']
                sl = row['stop_loss']
                tp = row['take_profit']
            elif row['signal'] == -1 and position == 0:
                position = -1
                entry_price = row['close']
                sl = row['stop_loss']
                tp = row['take_profit']
            if position != 0:
                # Check SL/TP
                if position == 1:
                    if row['low'] <= sl:
                        pnl = sl - entry_price
                        capital += pnl
                        trades.append(pnl)
                        position = 0
                    elif row['high'] >= tp:
                        pnl = tp - entry_price
                        capital += pnl
                        trades.append(pnl)
                        position = 0
                elif position == -1:
                    if row['high'] >= sl:
                        pnl = entry_price - sl
                        capital += pnl
                        trades.append(pnl)
                        position = 0
                    elif row['low'] <= tp:
                        pnl = entry_price - tp
                        capital += pnl
                        trades.append(pnl)
                        position = 0
            equity_curve.append(capital)
        self.df['equity_curve'] = equity_curve[:len(self.df)]
        self.results = trades
        return self.df

    def metrics(self):
        trades = np.array(self.results)
        winrate = np.mean(trades > 0) if len(trades) > 0 else 0
        profit_factor = trades[trades > 0].sum() / abs(trades[trades < 0].sum()) if trades[trades < 0].sum() != 0 else np.nan
        max_drawdown = self._max_drawdown(self.df['equity_curve'])
        return {
            'winrate': winrate,
            'profit_factor': profit_factor,
            'max_drawdown': max_drawdown,
            'num_trades': len(trades)
        }

    def _max_drawdown(self, equity_curve):
        roll_max = np.maximum.accumulate(equity_curve)
        drawdown = (equity_curve - roll_max) / roll_max
        return drawdown.min()

# Uso:
# backtester = Backtester(df_signals)
# df_bt = backtester.simulate()
# metrics = backtester.metrics() 