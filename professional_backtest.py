#!/usr/bin/env python3
"""
Professional Backtesting Suite para Bot SMC-LIT
Evaluación completa de rendimiento en múltiples pares y timeframes
"""

import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json
import warnings
warnings.filterwarnings('ignore')

# Configurar path
sys.path.append('src')

from src.mt5_connector import MT5Connector
from src.features import SMCFeatureExtractor  
from src.strategy import SMCStrategy
from src.backtester import Backtester

class ProfessionalBacktester:
    """
    Sistema de backtesting profesional para evaluar el bot SMC-LIT
    """
    
    def __init__(self):
        self.results = {}
        self.summary_metrics = {}
        
        # Configuración de testing profesional
        self.currency_pairs = [
            'EURUSD',  # Euro/Dollar - Par más líquido
            'GBPUSD',  # Libra/Dollar - Volatilidad media-alta
            'USDJPY',  # Dollar/Yen - Tendencias fuertes
            'AUDUSD',  # Aussie/Dollar - Correlación commodities
            'USDCAD'   # Dollar/Canadian - Estable
        ]
        
        self.timeframes = [
            'M15',  # 15 minutos - Scalping avanzado
            'M30',  # 30 minutos - Swing trading corto
            'H1',   # 1 hora - Trading intraday
            'H4'    # 4 horas - Swing trading
        ]
        
        # Período de prueba: 8 meses (suficiente para estadísticas)
        self.test_period_candles = {
            'M15': 15000,  # ~6 meses
            'M30': 8000,   # ~6 meses  
            'H1': 4000,    # ~6 meses
            'H4': 1000     # ~6 meses
        }
        
    def calculate_advanced_metrics(self, trades_df, equity_curve):
        """
        Calcula métricas avanzadas de trading profesional
        """
        if trades_df.empty or len(equity_curve) < 2:
            return {
                'total_trades': 0,
                'win_rate': 0,
                'profit_factor': 0,
                'sharpe_ratio': 0,
                'max_drawdown': 0,
                'calmar_ratio': 0,
                'average_win': 0,
                'average_loss': 0,
                'largest_win': 0,
                'largest_loss': 0,
                'consecutive_wins': 0,
                'consecutive_losses': 0,
                'total_return': 0,
                'annualized_return': 0,
                'volatility': 0,
                'total_pnl': 0
            }
        
        # Métricas básicas
        total_trades = len(trades_df)
        winning_trades = trades_df[trades_df['pnl'] > 0]
        losing_trades = trades_df[trades_df['pnl'] < 0]
        
        win_rate = len(winning_trades) / total_trades if total_trades > 0 else 0
        
        # Profit Factor
        gross_profit = winning_trades['pnl'].sum() if len(winning_trades) > 0 else 0
        gross_loss = abs(losing_trades['pnl'].sum()) if len(losing_trades) > 0 else 0.01
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0
        
        # Returns y Sharpe Ratio
        returns = pd.Series(equity_curve).pct_change().dropna()
        if len(returns) > 1:
            sharpe_ratio = returns.mean() / returns.std() * np.sqrt(252) if returns.std() > 0 else 0
            volatility = returns.std() * np.sqrt(252)
        else:
            sharpe_ratio = 0
            volatility = 0
        
        # Maximum Drawdown
        peak = pd.Series(equity_curve).expanding().max()
        drawdown = (pd.Series(equity_curve) - peak) / peak
        max_drawdown = abs(drawdown.min())
        
        # Total Return
        initial_balance = equity_curve[0] if len(equity_curve) > 0 else 10000
        final_balance = equity_curve[-1] if len(equity_curve) > 0 else 10000
        total_return = (final_balance - initial_balance) / initial_balance
        
        # Annualized Return (asumiendo 6 meses de datos)
        periods_per_year = 2  # 6 meses = 0.5 años
        annualized_return = (1 + total_return) ** periods_per_year - 1
        
        # Calmar Ratio
        calmar_ratio = annualized_return / max_drawdown if max_drawdown > 0 else 0
        
        # Promedios de ganancias/pérdidas
        avg_win = winning_trades['pnl'].mean() if len(winning_trades) > 0 else 0
        avg_loss = losing_trades['pnl'].mean() if len(losing_trades) > 0 else 0
        largest_win = winning_trades['pnl'].max() if len(winning_trades) > 0 else 0
        largest_loss = losing_trades['pnl'].min() if len(losing_trades) > 0 else 0
        
        # Rachas consecutivas
        consecutive_wins = self._calculate_consecutive_streak(trades_df, 'win')
        consecutive_losses = self._calculate_consecutive_streak(trades_df, 'loss')
        
        return {
            'total_trades': total_trades,
            'win_rate': win_rate,
            'profit_factor': profit_factor,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'calmar_ratio': calmar_ratio,
            'average_win': avg_win,
            'average_loss': avg_loss,
            'largest_win': largest_win,
            'largest_loss': largest_loss,
            'consecutive_wins': consecutive_wins,
            'consecutive_losses': consecutive_losses,
            'total_return': total_return,
            'annualized_return': annualized_return,
            'volatility': volatility,
            'total_pnl': gross_profit + losing_trades['pnl'].sum()
        }
    
    def _calculate_consecutive_streak(self, trades_df, streak_type):
        """Calcula rachas consecutivas máximas"""
        if trades_df.empty:
            return 0
            
        if streak_type == 'win':
            wins = (trades_df['pnl'] > 0).astype(int)
        else:
            wins = (trades_df['pnl'] <= 0).astype(int)
        
        max_streak = 0
        current_streak = 0
        
        for win in wins:
            if win:
                current_streak += 1
                max_streak = max(max_streak, current_streak)
            else:
                current_streak = 0
                
        return max_streak
    
    def run_single_backtest(self, symbol, timeframe):
        """
        Ejecuta un backtest individual para un par y timeframe específico
        """
        print(f"📊 Testing {symbol} {timeframe}...")
        
        try:
            # Conectar y obtener datos
            connector = MT5Connector(symbol=symbol, timeframe=timeframe)
            
            # Obtener datos históricos
            num_candles = self.test_period_candles[timeframe]
            df = connector.fetch_ohlc_data(num_candles=num_candles)
            
            if df is None or len(df) < 500:
                print(f"❌ Datos insuficientes para {symbol} {timeframe}")
                return None
            
            print(f"   📈 Datos: {len(df)} velas ({df['datetime'].iloc[0]} - {df['datetime'].iloc[-1]})")
            
            # Extraer features SMC
            features_extractor = SMCFeatureExtractor(df)
            df_features = features_extractor.extract_all()
            
            # Generar señales
            strategy = SMCStrategy(df_features)
            df_signals = strategy.run()
            
            # Obtener última vela con señal
            latest_candle = df_signals.iloc[-1]
            latest_signal = latest_candle['signal']
            
            # Ejecutar backtesting
            backtester = Backtester(df_signals)
            df_bt = backtester.simulate()
            
            # Calcular métricas básicas
            basic_metrics = backtester.metrics()
            
            # Extraer trades y equity curve
            trades = []
            equity_curve = [10000]  # Balance inicial
            current_balance = 10000
            
            for _, row in df_bt.iterrows():
                if pd.notna(row.get('trade_pnl', np.nan)):
                    trade_pnl = row['trade_pnl']
                    trades.append({
                        'datetime': row['datetime'],
                        'symbol': symbol,
                        'pnl': trade_pnl,
                        'entry_price': row.get('entry_price', 0),
                        'exit_price': row.get('exit_price', 0)
                    })
                    current_balance += trade_pnl
                    equity_curve.append(current_balance)
            
            trades_df = pd.DataFrame(trades)
            
            # Calcular métricas avanzadas
            advanced_metrics = self.calculate_advanced_metrics(trades_df, equity_curve)
            
            # Combinar métricas
            result = {
                'symbol': symbol,
                'timeframe': timeframe,
                'period': f"{df['datetime'].iloc[0].strftime('%Y-%m-%d')} to {df['datetime'].iloc[-1].strftime('%Y-%m-%d')}",
                'candles_analyzed': len(df),
                'trades_df': trades_df,
                'equity_curve': equity_curve,
                **basic_metrics,
                **advanced_metrics
            }
            
            print(f"   ✅ Completado: {advanced_metrics['total_trades']} trades, {advanced_metrics['win_rate']:.1%} win rate")
            
            connector.disconnect()
            return result
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            return None
    
    def run_comprehensive_backtest(self):
        """
        Ejecuta backtest completo en todos los pares y timeframes
        """
        print("🚀 INICIANDO BACKTESTING PROFESIONAL SMC-LIT")
        print("=" * 60)
        
        total_tests = len(self.currency_pairs) * len(self.timeframes)
        current_test = 0
        
        for symbol in self.currency_pairs:
            self.results[symbol] = {}
            
            for timeframe in self.timeframes:
                current_test += 1
                print(f"\n[{current_test}/{total_tests}] {symbol} - {timeframe}")
                
                result = self.run_single_backtest(symbol, timeframe)
                if result:
                    self.results[symbol][timeframe] = result
        
        print(f"\n✅ Backtesting completado!")
        
    def generate_summary_report(self):
        """
        Genera reporte resumido de todos los resultados
        """
        print("\n📊 GENERANDO REPORTE DE RENDIMIENTO...")
        
        summary_data = []
        
        for symbol in self.results:
            for timeframe in self.results[symbol]:
                data = self.results[symbol][timeframe]
                summary_data.append({
                    'Symbol': symbol,
                    'Timeframe': timeframe,
                    'Total Trades': data['total_trades'],
                    'Win Rate': f"{data['win_rate']:.1%}",
                    'Profit Factor': f"{data['profit_factor']:.2f}",
                    'Total Return': f"{data['total_return']:.1%}",
                    'Annual Return': f"{data['annualized_return']:.1%}",
                    'Max Drawdown': f"{data['max_drawdown']:.1%}",
                    'Sharpe Ratio': f"{data['sharpe_ratio']:.2f}",
                    'Calmar Ratio': f"{data['calmar_ratio']:.2f}"
                })
        
        summary_df = pd.DataFrame(summary_data)
        
        # Guardar reporte
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        summary_df.to_csv(f'backtest_summary_{timestamp}.csv', index=False)
        
        return summary_df
    
    def create_visualizations(self):
        """
        Crea visualizaciones profesionales de los resultados
        """
        print("📈 CREANDO VISUALIZACIONES...")
        
        # Configurar estilo
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
        # Crear figura con subplots
        fig = plt.figure(figsize=(20, 16))
        
        # 1. Heatmap de Win Rates
        plt.subplot(3, 3, 1)
        win_rates = []
        for symbol in self.currency_pairs:
            row = []
            for timeframe in self.timeframes:
                if symbol in self.results and timeframe in self.results[symbol]:
                    win_rate = self.results[symbol][timeframe]['win_rate']
                    row.append(win_rate * 100)
                else:
                    row.append(0)
            win_rates.append(row)
        
        sns.heatmap(win_rates, annot=True, fmt='.1f', 
                   xticklabels=self.timeframes, yticklabels=self.currency_pairs,
                   cmap='RdYlGn', center=50)
        plt.title('Win Rate % por Par y Timeframe')
        
        # 2. Heatmap de Profit Factor
        plt.subplot(3, 3, 2)
        profit_factors = []
        for symbol in self.currency_pairs:
            row = []
            for timeframe in self.timeframes:
                if symbol in self.results and timeframe in self.results[symbol]:
                    pf = self.results[symbol][timeframe]['profit_factor']
                    row.append(pf)
                else:
                    row.append(0)
            profit_factors.append(row)
        
        sns.heatmap(profit_factors, annot=True, fmt='.2f',
                   xticklabels=self.timeframes, yticklabels=self.currency_pairs,
                   cmap='RdYlGn', center=1.0)
        plt.title('Profit Factor por Par y Timeframe')
        
        # 3. Retornos anualizados
        plt.subplot(3, 3, 3)
        annual_returns = []
        for symbol in self.currency_pairs:
            row = []
            for timeframe in self.timeframes:
                if symbol in self.results and timeframe in self.results[symbol]:
                    ret = self.results[symbol][timeframe]['annualized_return']
                    row.append(ret * 100)
                else:
                    row.append(0)
            annual_returns.append(row)
        
        sns.heatmap(annual_returns, annot=True, fmt='.1f',
                   xticklabels=self.timeframes, yticklabels=self.currency_pairs,
                   cmap='RdYlGn', center=0)
        plt.title('Retorno Anualizado % por Par y Timeframe')
        
        # 4. Mejor equity curve por timeframe
        for i, timeframe in enumerate(self.timeframes):
            plt.subplot(3, 3, 5 + i)
            
            best_symbol = None
            best_return = -999
            
            for symbol in self.currency_pairs:
                if symbol in self.results and timeframe in self.results[symbol]:
                    ret = self.results[symbol][timeframe]['total_return']
                    if ret > best_return:
                        best_return = ret
                        best_symbol = symbol
            
            if best_symbol:
                equity = self.results[best_symbol][timeframe]['equity_curve']
                plt.plot(equity, label=f'{best_symbol} ({best_return:.1%})')
                plt.title(f'Mejor Equity Curve - {timeframe}')
                plt.ylabel('Balance ($)')
                plt.legend()
                plt.grid(True, alpha=0.3)
        
        # 5. Distribución de trades por resultado
        plt.subplot(3, 3, 9)
        all_pnls = []
        for symbol in self.results:
            for timeframe in self.results[symbol]:
                trades_df = self.results[symbol][timeframe]['trades_df']
                if not trades_df.empty:
                    all_pnls.extend(trades_df['pnl'].tolist())
        
        if all_pnls:
            plt.hist(all_pnls, bins=50, alpha=0.7, edgecolor='black')
            plt.axvline(x=0, color='red', linestyle='--', alpha=0.8)
            plt.title('Distribución de P&L por Trade')
            plt.xlabel('P&L ($)')
            plt.ylabel('Frecuencia')
        
        plt.tight_layout()
        
        # Guardar visualización
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        plt.savefig(f'backtest_analysis_{timestamp}.png', dpi=300, bbox_inches='tight')
        plt.show()
        
        print(f"📊 Visualizaciones guardadas como 'backtest_analysis_{timestamp}.png'")
    
    def print_executive_summary(self):
        """
        Imprime resumen ejecutivo de los resultados
        """
        print("\n" + "="*80)
        print("📋 RESUMEN EJECUTIVO - BOT SMC-LIT BACKTEST")
        print("="*80)
        
        # Calcular estadísticas generales
        all_results = []
        for symbol in self.results:
            for timeframe in self.results[symbol]:
                all_results.append(self.results[symbol][timeframe])
        
        if not all_results:
            print("❌ No hay resultados para mostrar")
            return
        
        # Mejores y peores performers
        best_return = max(all_results, key=lambda x: x['total_return'])
        worst_return = min(all_results, key=lambda x: x['total_return'])
        best_sharpe = max(all_results, key=lambda x: x['sharpe_ratio'])
        best_profit_factor = max(all_results, key=lambda x: x['profit_factor'])
        
        # Promedios
        avg_win_rate = np.mean([r['win_rate'] for r in all_results])
        avg_return = np.mean([r['total_return'] for r in all_results])
        avg_profit_factor = np.mean([r['profit_factor'] for r in all_results])
        avg_sharpe = np.mean([r['sharpe_ratio'] for r in all_results])
        avg_drawdown = np.mean([r['max_drawdown'] for r in all_results])
        
        print(f"🎯 RESULTADOS GENERALES:")
        print(f"   • Configuraciones probadas: {len(all_results)}")
        print(f"   • Win Rate promedio: {avg_win_rate:.1%}")
        print(f"   • Retorno promedio: {avg_return:.1%}")
        print(f"   • Profit Factor promedio: {avg_profit_factor:.2f}")
        print(f"   • Sharpe Ratio promedio: {avg_sharpe:.2f}")
        print(f"   • Drawdown promedio: {avg_drawdown:.1%}")
        
        print(f"\n🏆 MEJORES PERFORMERS:")
        print(f"   • Mejor retorno: {best_return['symbol']} {best_return['timeframe']} ({best_return['total_return']:.1%})")
        print(f"   • Mejor Sharpe: {best_sharpe['symbol']} {best_sharpe['timeframe']} ({best_sharpe['sharpe_ratio']:.2f})")
        print(f"   • Mejor Profit Factor: {best_profit_factor['symbol']} {best_profit_factor['timeframe']} ({best_profit_factor['profit_factor']:.2f})")
        
        print(f"\n⚠️  CONSIDERACIONES:")
        print(f"   • Peor retorno: {worst_return['symbol']} {worst_return['timeframe']} ({worst_return['total_return']:.1%})")
        print(f"   • Configuraciones rentables: {len([r for r in all_results if r['total_return'] > 0])}/{len(all_results)}")
        
        # Recomendaciones
        print(f"\n💡 RECOMENDACIONES:")
        profitable_configs = [r for r in all_results if r['total_return'] > 0.05 and r['profit_factor'] > 1.2]
        
        if profitable_configs:
            print(f"   ✅ Configuraciones recomendadas para deploy:")
            for config in sorted(profitable_configs, key=lambda x: x['sharpe_ratio'], reverse=True)[:3]:
                print(f"      • {config['symbol']} {config['timeframe']}: {config['total_return']:.1%} return, {config['profit_factor']:.2f} PF")
        else:
            print(f"   ⚠️  Ajustar parámetros - Pocas configuraciones rentables detectadas")
        
        print("="*80)

def main():
    """Función principal del backtesting"""
    backtester = ProfessionalBacktester()
    
    try:
        # Ejecutar backtesting completo
        backtester.run_comprehensive_backtest()
        
        # Generar reportes
        summary_df = backtester.generate_summary_report()
        print(f"\n📊 TABLA RESUMEN:")
        print(summary_df.to_string(index=False))
        
        # Crear visualizaciones
        backtester.create_visualizations()
        
        # Mostrar resumen ejecutivo
        backtester.print_executive_summary()
        
        print(f"\n✅ ¡Backtesting profesional completado!")
        print(f"📁 Archivos generados:")
        print(f"   • backtest_summary_*.csv")
        print(f"   • backtest_analysis_*.png")
        
    except Exception as e:
        print(f"❌ Error en backtesting: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 