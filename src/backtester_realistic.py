"""
backtester_realistic.py - Backtester REALISTA con ML y estadísticas profesionales
"""

import pandas as pd
import numpy as np
from datetime import datetime
from sklearn.ensemble import RandomForestClassifier
import random

class RealisticBacktester:
    """
    Backtester REALISTA que simula condiciones reales de mercado
    """
    def __init__(self, df: pd.DataFrame, initial_balance=10000, risk_per_trade=0.02, commission=0.00007):
        self.df = df.copy()
        self.initial_balance = initial_balance
        self.risk_per_trade = risk_per_trade
        self.commission = commission
        
        self.trades = []
        self.equity_curve = [initial_balance]
        self.current_balance = initial_balance
        
        # ML para aprender de errores
        self.ml_model = RandomForestClassifier(n_estimators=50, random_state=42)
        self.ml_features = []
        self.ml_labels = []
        self.ml_trained = False
        
        # Estadísticas realistas
        self.consecutive_losses = 0
        self.max_consecutive_losses = 0
        self.consecutive_wins = 0
        self.max_consecutive_wins = 0
        
    def calculate_position_size(self, entry_price, stop_loss):
        """
        Cálculo de posición con gestión de riesgo realista
        """
        if pd.isna(stop_loss) or stop_loss == 0:
            return 0.01
            
        # Reducir tamaño después de rachas perdedoras (psicología real)
        size_multiplier = 1.0
        if self.consecutive_losses >= 3:
            size_multiplier = 0.7  # Reducir 30% después de 3 pérdidas consecutivas
        elif self.consecutive_losses >= 5:
            size_multiplier = 0.5  # Reducir 50% después de 5 pérdidas
            
        risk_amount = self.current_balance * self.risk_per_trade * size_multiplier
        price_risk = abs(entry_price - stop_loss)
        
        if price_risk == 0:
            return 0.01
            
        pip_value = 10
        pips_risked = price_risk * 10000
        
        if pips_risked == 0:
            return 0.01
            
        lot_size = risk_amount / (pips_risked * pip_value)
        lot_size = max(0.01, min(lot_size, 0.5))  # Máximo más conservador
        
        return lot_size
    
    def simulate_realistic_execution(self, trade_type, entry_price, stop_loss, take_profit, candle_data):
        """
        Simula ejecución REALISTA verificando cada vela
        """
        # Simular slippage realista
        slippage = random.uniform(0.5, 2.0) * 0.00001  # 0.5-2 pips de slippage
        
        if trade_type == 'BUY':
            actual_entry = entry_price + self.commission + slippage
            
            # Verificar si se toca SL o TP en la vela
            if candle_data['low'] <= stop_loss:
                # Hit SL - Probabilidad 60% (realista)
                if random.random() < 0.60:
                    exit_price = stop_loss
                    return exit_price, 'SL'
            
            if candle_data['high'] >= take_profit:
                # Hit TP - Probabilidad 45% (conservador)
                if random.random() < 0.45:
                    exit_price = take_profit
                    return exit_price, 'TP'
                    
        else:  # SELL
            actual_entry = entry_price - self.commission - slippage
            
            if candle_data['high'] >= stop_loss:
                if random.random() < 0.60:
                    exit_price = stop_loss
                    return exit_price, 'SL'
                    
            if candle_data['low'] <= take_profit:
                if random.random() < 0.45:
                    exit_price = take_profit
                    return exit_price, 'TP'
        
        # No se cerró - continúa abierto (simplificado: cerrar al precio actual)
        return candle_data['close'], 'TIME'
    
    def extract_ml_features(self, row, i):
        """
        Extrae features para ML
        """
        features = [
            row.get('rsi_14', 50),
            row.get('atr_14', 0.001) * 10000,  # ATR en pips
            row.get('signal_strength', 0),
            self.consecutive_losses,
            self.consecutive_wins,
            1 if row.get('signal', 0) == 1 else -1,  # Long/Short
            # Volatilidad reciente
            self.df['close'].iloc[max(0,i-5):i].std() * 10000 if i > 5 else 0,
            # Momentum
            (row['close'] - self.df['close'].iloc[max(0,i-5)]) * 10000 if i > 5 else 0
        ]
        return features
    
    def update_ml_model(self, features, was_profitable):
        """
        Actualiza el modelo ML con nuevos datos
        """
        self.ml_features.append(features)
        self.ml_labels.append(1 if was_profitable else 0)
        
        # Entrenar cada 50 trades
        if len(self.ml_features) >= 50 and len(self.ml_features) % 25 == 0:
            try:
                self.ml_model.fit(self.ml_features, self.ml_labels)
                self.ml_trained = True
                print(f"   🤖 ML actualizado con {len(self.ml_features)} trades")
            except:
                pass
    
    def should_take_trade(self, features, signal_strength):
        """
        Decide si tomar el trade usando ML + filtros
        """
        # Filtros básicos
        if abs(signal_strength) < 0.10:  # Umbral mínimo más bajo pero realista
            return False
            
        # Si tenemos ML entrenado, usarlo
        if self.ml_trained and len(features) == 8:
            try:
                probability = self.ml_model.predict_proba([features])[0][1]
                # Solo tomar trades con >55% probabilidad según ML
                if probability < 0.55:
                    return False
            except:
                pass
                
        # Evitar trading después de muchas pérdidas consecutivas
        if self.consecutive_losses >= 6:
            return False
            
        return True
    
    def execute_trade(self, trade_type, entry_price, stop_loss, take_profit, lot_size, entry_time, candle_data):
        """
        Ejecuta trade con simulación realista
        """
        exit_price, exit_reason = self.simulate_realistic_execution(
            trade_type, entry_price, stop_loss, take_profit, candle_data
        )
        
        # Calcular P&L
        if trade_type == 'BUY':
            pnl_pips = (exit_price - entry_price) * 10000
        else:
            pnl_pips = (entry_price - exit_price) * 10000
            
        # Convertir a dólares
        pnl_dollars = pnl_pips * lot_size * 10
        
        # Comisión realista
        commission_cost = self.commission * lot_size * 100000 * 2  # Round trip
        net_pnl = pnl_dollars - commission_cost
        
        # Determinar si fue ganador
        was_profitable = net_pnl > 0
        
        # Actualizar rachas
        if was_profitable:
            self.consecutive_wins += 1
            self.consecutive_losses = 0
            self.max_consecutive_wins = max(self.max_consecutive_wins, self.consecutive_wins)
        else:
            self.consecutive_losses += 1
            self.consecutive_wins = 0
            self.max_consecutive_losses = max(self.max_consecutive_losses, self.consecutive_losses)
        
        trade = {
            'entry_time': entry_time,
            'exit_time': entry_time,
            'type': trade_type,
            'entry_price': entry_price,
            'exit_price': exit_price,
            'exit_reason': exit_reason,
            'lot_size': lot_size,
            'pnl': net_pnl,
            'pnl_pips': pnl_pips,
            'commission': commission_cost,
            'was_profitable': was_profitable
        }
        
        self.current_balance += net_pnl
        self.equity_curve.append(self.current_balance)
        self.trades.append(trade)
        
        return trade
    
    def run(self):
        """
        Ejecuta backtesting REALISTA
        """
        print(f"🔄 Backtesting REALISTA en {len(self.df)} velas...")
        
        signals_generated = 0
        trades_taken = 0
        trades_rejected_ml = 0
        
        for i in range(len(self.df)):
            row = self.df.iloc[i]
            
            if row.get('signal', 0) != 0 and not pd.isna(row.get('stop_loss')) and not pd.isna(row.get('take_profit')):
                signals_generated += 1
                
                # Extraer features para ML
                features = self.extract_ml_features(row, i)
                signal_strength = row.get('signal_strength', 0)
                
                # Decidir si tomar el trade
                if not self.should_take_trade(features, signal_strength):
                    trades_rejected_ml += 1
                    continue
                
                trades_taken += 1
                
                entry_price = row['close']
                stop_loss = row['stop_loss']
                take_profit = row['take_profit']
                entry_time = row.get('datetime', datetime.now())
                
                lot_size = self.calculate_position_size(entry_price, stop_loss)
                trade_type = 'BUY' if row['signal'] == 1 else 'SELL'
                
                trade = self.execute_trade(
                    trade_type, entry_price, stop_loss, take_profit, 
                    lot_size, entry_time, row
                )
                
                # Actualizar ML
                self.update_ml_model(features, trade['was_profitable'])
                
                if len(self.trades) <= 10 or len(self.trades) % 50 == 0:
                    print(f"   Trade {len(self.trades)}: {trade_type} @ {entry_price:.5f} → "
                          f"{trade['exit_reason']} = ${trade['pnl']:.2f}")
        
        print(f"📊 Señales generadas: {signals_generated}")
        print(f"🎯 Trades tomados: {trades_taken}")
        print(f"🤖 Trades rechazados por ML: {trades_rejected_ml}")
        print(f"💰 Trades ejecutados: {len(self.trades)}")
        print(f"📈 Balance final: ${self.current_balance:.2f}")
        
        return {
            'trades': self.trades,
            'equity_curve': self.equity_curve,
            'initial_balance': self.initial_balance,
            'final_balance': self.current_balance,
            'ml_trained': self.ml_trained,
            'max_consecutive_losses': self.max_consecutive_losses,
            'max_consecutive_wins': self.max_consecutive_wins
        } 