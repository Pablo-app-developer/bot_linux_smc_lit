#!/usr/bin/env python3
"""
BACKTESTING ULTRA OPTIMIZADO - Bot SMC-LIT
Configuración agresiva para máxima rentabilidad
"""

import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configurar path
sys.path.append('src')

from src.mt5_connector import MT5Connector
from src.features import SMCFeatureExtractor  
from src.strategy import SMCStrategy
from src.backtester_optimized import BacktesterOptimized

class UltraOptimizedBacktest:
    """
    Backtesting con parámetros ULTRA AGRESIVOS para máxima rentabilidad
    """
    
    def __init__(self):
        self.initial_balance = 10000
        self.results = {}
        
        # Configuración AGRESIVA
        self.pairs = ['EURUSD', 'GBPUSD', 'USDJPY', 'AUDUSD']
        self.timeframes = ['M15', 'H1'] 
        self.test_candles = {'M15': 5000, 'H1': 2000}  # Período más corto para testing rápido
        
    def run_aggressive_backtest(self, symbol, timeframe):
        """
        Ejecuta backtesting con configuración ULTRA AGRESIVA
        """
        print(f"🚀 TESTING AGRESIVO {symbol} {timeframe}...")
        
        try:
            # Conectar y obtener datos
            connector = MT5Connector(symbol=symbol, timeframe=timeframe)
            num_candles = self.test_candles[timeframe]
            df = connector.fetch_ohlc_data(num_candles=num_candles)
            
            if df is None or len(df) < 100:
                print(f"❌ Datos insuficientes para {symbol} {timeframe}")
                return None
            
            print(f"   📊 Datos: {len(df)} velas")
            
            # Extraer features SMC OPTIMIZADAS
            features_extractor = SMCFeatureExtractor(df)
            df_features = features_extractor.extract_all()
            
            # Generar señales AGRESIVAS
            strategy = SMCStrategy(df_features)
            df_signals = strategy.run()
            
            # Ejecutar backtesting
            backtester = BacktesterOptimized(
                df_signals, 
                initial_balance=self.initial_balance,
                risk_per_trade=0.03,  # 3% por trade (MUY AGRESIVO)
                commission=0.00007    # Spread típico
            )
            
            results = backtester.run()
            
            # Calcular métricas detalladas
            metrics = self.calculate_detailed_metrics(results)
            
            print(f"   💰 Trades: {metrics['total_trades']}")
            print(f"   📈 Win Rate: {metrics['win_rate']:.1f}%")
            print(f"   💵 P&L Total: ${metrics['total_pnl']:.2f}")
            print(f"   📊 Retorno: {metrics['total_return']:.1f}%")
            
            return {
                'symbol': symbol,
                'timeframe': timeframe,
                'results': results,
                'metrics': metrics,
                'df_signals': df_signals
            }
            
        except Exception as e:
            print(f"❌ Error en {symbol} {timeframe}: {e}")
            return None
    
    def calculate_detailed_metrics(self, results):
        """
        Calcula métricas financieras detalladas
        """
        if not results['trades'] or len(results['trades']) == 0:
            return {
                'total_trades': 0,
                'winning_trades': 0,
                'losing_trades': 0,
                'win_rate': 0,
                'total_pnl': 0,
                'gross_profit': 0,
                'gross_loss': 0,
                'profit_factor': 0,
                'average_win': 0,
                'average_loss': 0,
                'max_win': 0,
                'max_loss': 0,
                'total_return': 0,
                'max_drawdown': 0,
                'final_balance': self.initial_balance
            }
        
        trades_df = pd.DataFrame(results['trades'])
        equity_curve = results['equity_curve']
        
        # Métricas básicas
        total_trades = len(trades_df)
        winning_trades = trades_df[trades_df['pnl'] > 0]
        losing_trades = trades_df[trades_df['pnl'] <= 0]
        
        win_count = len(winning_trades)
        loss_count = len(losing_trades)
        win_rate = (win_count / total_trades * 100) if total_trades > 0 else 0
        
        # P&L
        total_pnl = trades_df['pnl'].sum()
        gross_profit = winning_trades['pnl'].sum() if win_count > 0 else 0
        gross_loss = abs(losing_trades['pnl'].sum()) if loss_count > 0 else 0
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')
        
        # Promedios
        avg_win = winning_trades['pnl'].mean() if win_count > 0 else 0
        avg_loss = losing_trades['pnl'].mean() if loss_count > 0 else 0
        max_win = winning_trades['pnl'].max() if win_count > 0 else 0
        max_loss = losing_trades['pnl'].min() if loss_count > 0 else 0
        
        # Retorno y drawdown
        final_balance = equity_curve[-1] if equity_curve else self.initial_balance
        total_return = ((final_balance - self.initial_balance) / self.initial_balance * 100)
        
        # Drawdown máximo
        peak = pd.Series(equity_curve).expanding().max()
        drawdown = (pd.Series(equity_curve) - peak) / peak * 100
        max_drawdown = abs(drawdown.min()) if len(drawdown) > 0 else 0
        
        return {
            'total_trades': total_trades,
            'winning_trades': win_count,
            'losing_trades': loss_count,
            'win_rate': win_rate,
            'total_pnl': total_pnl,
            'gross_profit': gross_profit,
            'gross_loss': gross_loss,
            'profit_factor': profit_factor,
            'average_win': avg_win,
            'average_loss': avg_loss,
            'max_win': max_win,
            'max_loss': max_loss,
            'total_return': total_return,
            'max_drawdown': max_drawdown,
            'final_balance': final_balance
        }
    
    def run_comprehensive_test(self):
        """
        Ejecuta testing completo en todos los pares y timeframes
        """
        print("🚀 INICIANDO BACKTESTING ULTRA OPTIMIZADO")
        print("=" * 60)
        
        all_results = []
        total_profit = 0
        total_trades = 0
        
        for symbol in self.pairs:
            for timeframe in self.timeframes:
                result = self.run_aggressive_backtest(symbol, timeframe)
                if result:
                    all_results.append(result)
                    total_profit += result['metrics']['total_pnl']
                    total_trades += result['metrics']['total_trades']
        
        # Resumen ejecutivo
        self.print_executive_summary(all_results, total_profit, total_trades)
        
        return all_results
    
    def print_executive_summary(self, results, total_profit, total_trades):
        """
        Imprime resumen ejecutivo con resultados financieros
        """
        print("\n" + "=" * 80)
        print("💰 RESUMEN FINANCIERO - CONFIGURACIÓN ULTRA OPTIMIZADA")
        print("=" * 80)
        
        if not results:
            print("❌ No se generaron trades con la configuración actual")
            print("\n🔧 RECOMENDACIONES:")
            print("   • Los parámetros son demasiado restrictivos")
            print("   • Reducir umbrales de señales")
            print("   • Revisar detección de features SMC")
            return
        
        # Totales generales
        print(f"💼 CAPITAL INICIAL: ${self.initial_balance:,.2f}")
        print(f"💰 GANANCIA/PÉRDIDA TOTAL: ${total_profit:,.2f}")
        print(f"📊 TRADES EJECUTADOS: {total_trades}")
        
        if total_trades > 0:
            print(f"📈 RETORNO TOTAL: {(total_profit / self.initial_balance * 100):+.2f}%")
            print(f"💵 GANANCIA POR TRADE: ${total_profit / total_trades:.2f}")
        
        # Mejores performers
        profitable_configs = [r for r in results if r['metrics']['total_pnl'] > 0]
        
        if profitable_configs:
            best_config = max(profitable_configs, key=lambda x: x['metrics']['total_pnl'])
            print(f"\n🏆 MEJOR CONFIGURACIÓN:")
            print(f"   Par: {best_config['symbol']} {best_config['timeframe']}")
            print(f"   Ganancia: ${best_config['metrics']['total_pnl']:.2f}")
            print(f"   Win Rate: {best_config['metrics']['win_rate']:.1f}%")
            print(f"   Trades: {best_config['metrics']['total_trades']}")
            
            if best_config['metrics']['profit_factor'] != float('inf'):
                print(f"   Profit Factor: {best_config['metrics']['profit_factor']:.2f}")
        
        # Tabla detallada
        print(f"\n📋 DETALLE POR CONFIGURACIÓN:")
        print("-" * 80)
        print(f"{'Par':<8} {'TF':<4} {'Trades':<7} {'Win%':<6} {'P&L':<10} {'Retorno%':<9}")
        print("-" * 80)
        
        for result in results:
            m = result['metrics']
            print(f"{result['symbol']:<8} {result['timeframe']:<4} "
                  f"{m['total_trades']:<7} {m['win_rate']:<6.1f} "
                  f"${m['total_pnl']:<9.2f} {m['total_return']:<8.1f}%")
        
        print("-" * 80)
        print(f"{'TOTAL':<8} {'':<4} {total_trades:<7} {'':<6} "
              f"${total_profit:<9.2f} {(total_profit/self.initial_balance*100):<8.1f}%")

def main():
    """
    Función principal del backtesting optimizado
    """
    print("🎯 Bot SMC-LIT - Backtesting Ultra Optimizado")
    print("Configuración: Parámetros agresivos para máxima rentabilidad\n")
    
    backtester = UltraOptimizedBacktest()
    results = backtester.run_comprehensive_test()
    
    print("\n✅ Backtesting completado!")
    
    # Guardar resultados
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if results:
        # Crear resumen en CSV
        summary_data = []
        for result in results:
            row = {
                'Symbol': result['symbol'],
                'Timeframe': result['timeframe'],
                'Total_Trades': result['metrics']['total_trades'],
                'Win_Rate': result['metrics']['win_rate'],
                'Total_PnL': result['metrics']['total_pnl'],
                'Total_Return': result['metrics']['total_return'],
                'Profit_Factor': result['metrics']['profit_factor'],
                'Max_Drawdown': result['metrics']['max_drawdown']
            }
            summary_data.append(row)
        
        df_summary = pd.DataFrame(summary_data)
        csv_filename = f"ultra_optimized_results_{timestamp}.csv"
        df_summary.to_csv(csv_filename, index=False)
        print(f"📁 Resultados guardados en: {csv_filename}")

if __name__ == "__main__":
    main() 