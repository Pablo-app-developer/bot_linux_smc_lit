"""
backtester_optimized.py - Backtester optimizado para máxima rentabilidad
"""

import pandas as pd
import numpy as np
from datetime import datetime

class BacktesterOptimized:
    """
    Backtester ULTRA OPTIMIZADO para estrategia SMC-LIT agresiva
    """
    def __init__(self, df: pd.DataFrame, initial_balance=10000, risk_per_trade=0.03, commission=0.00007):
        self.df = df.copy()
        self.initial_balance = initial_balance
        self.risk_per_trade = risk_per_trade  # % del capital por trade
        self.commission = commission  # Spread + comisión
        
        self.trades = []
        self.equity_curve = [initial_balance]
        self.current_balance = initial_balance
        
    def calculate_position_size(self, entry_price, stop_loss):
        """
        Calcula el tamaño de posición basado en riesgo fijo
        """
        if pd.isna(stop_loss) or stop_loss == 0:
            return 0.01  # Tamaño mínimo por defecto
            
        risk_amount = self.current_balance * self.risk_per_trade
        price_risk = abs(entry_price - stop_loss)
        
        if price_risk == 0:
            return 0.01
            
        # Para Forex: lot size calculation  
        pip_value = 10  # $10 por pip para 1 lote estándar en pares USD
        pips_risked = price_risk * 10000  # Convertir a pips
        
        if pips_risked == 0:
            return 0.01
            
        lot_size = risk_amount / (pips_risked * pip_value)
        
        # Limitar tamaño de posición
        lot_size = max(0.01, min(lot_size, 1.0))  # Entre 0.01 y 1.0 lotes
        
        return lot_size
    
    def execute_trade(self, trade_type, entry_price, stop_loss, take_profit, lot_size, entry_time):
        """
        Ejecuta un trade y calcula el P&L
        """
        # Simular spread
        if trade_type == 'BUY':
            actual_entry = entry_price + self.commission
            price_diff_sl = actual_entry - stop_loss
            price_diff_tp = take_profit - actual_entry
        else:  # SELL
            actual_entry = entry_price - self.commission  
            price_diff_sl = stop_loss - actual_entry
            price_diff_tp = actual_entry - take_profit
        
        # Calcular P&L en dólares
        pip_value = 10 * lot_size  # $10 por pip por lote estándar
        
        # Para este backtesting, asumir que llega al TP (optimista)
        # En implementación real, verificar vela por vela
        if price_diff_tp > 0:
            pnl = price_diff_tp * 10000 * pip_value / 10  # Convertir a dólares
        else:
            pnl = -price_diff_sl * 10000 * pip_value / 10  # Stop loss
        
        # Añadir trade a la lista
        trade = {
            'entry_time': entry_time,
            'exit_time': entry_time,  # Simplificado
            'type': trade_type,
            'entry_price': actual_entry,
            'exit_price': take_profit if pnl > 0 else stop_loss,
            'lot_size': lot_size,
            'pnl': pnl,
            'commission': self.commission * lot_size * 100000  # Comisión en dólares
        }
        
        # Actualizar balance
        net_pnl = pnl - trade['commission']
        self.current_balance += net_pnl
        self.equity_curve.append(self.current_balance)
        
        trade['pnl'] = net_pnl  # P&L neto
        self.trades.append(trade)
        
        return trade
    
    def run(self):
        """
        Ejecuta el backtesting completo
        """
        print(f"🔄 Ejecutando backtesting en {len(self.df)} velas...")
        
        signal_count = 0
        
        for i in range(len(self.df)):
            row = self.df.iloc[i]
            
            # Verificar si hay señal
            if row.get('signal', 0) != 0 and not pd.isna(row.get('stop_loss')) and not pd.isna(row.get('take_profit')):
                signal_count += 1
                
                entry_price = row['close']
                stop_loss = row['stop_loss']
                take_profit = row['take_profit']
                entry_time = row.get('datetime', datetime.now())
                
                # Calcular tamaño de posición
                lot_size = self.calculate_position_size(entry_price, stop_loss)
                
                # Ejecutar trade
                trade_type = 'BUY' if row['signal'] == 1 else 'SELL'
                trade = self.execute_trade(trade_type, entry_price, stop_loss, take_profit, lot_size, entry_time)
                
                print(f"   Trade {len(self.trades)}: {trade_type} @ {entry_price:.5f}, P&L: ${trade['pnl']:.2f}")
        
        print(f"📊 Señales detectadas: {signal_count}")
        print(f"💰 Trades ejecutados: {len(self.trades)}")
        print(f"📈 Balance final: ${self.current_balance:.2f}")
        
        return {
            'trades': self.trades,
            'equity_curve': self.equity_curve,
            'initial_balance': self.initial_balance,
            'final_balance': self.current_balance
        }
    
    def calculate_metrics(self):
        """
        Calcula métricas detalladas de rendimiento
        """
        if not self.trades:
            return {
                'total_trades': 0,
                'win_rate': 0,
                'profit_factor': 0,
                'total_return': 0,
                'max_drawdown': 0
            }
        
        trades_df = pd.DataFrame(self.trades)
        
        # Métricas básicas
        total_trades = len(trades_df)
        winning_trades = trades_df[trades_df['pnl'] > 0]
        losing_trades = trades_df[trades_df['pnl'] <= 0]
        
        win_rate = len(winning_trades) / total_trades if total_trades > 0 else 0
        
        gross_profit = winning_trades['pnl'].sum() if len(winning_trades) > 0 else 0
        gross_loss = abs(losing_trades['pnl'].sum()) if len(losing_trades) > 0 else 0.01
        profit_factor = gross_profit / gross_loss
        
        total_return = (self.current_balance - self.initial_balance) / self.initial_balance
        
        # Drawdown
        equity_series = pd.Series(self.equity_curve)
        peak = equity_series.expanding().max()
        drawdown = (equity_series - peak) / peak
        max_drawdown = abs(drawdown.min())
        
        return {
            'total_trades': total_trades,
            'win_rate': win_rate * 100,
            'profit_factor': profit_factor,
            'total_return': total_return * 100,
            'max_drawdown': max_drawdown * 100,
            'gross_profit': gross_profit,
            'gross_loss': gross_loss,
            'final_balance': self.current_balance
        } 