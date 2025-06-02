#!/usr/bin/env python3
"""
BACKTESTING REALISTA - Bot SMC-LIT
Win rates profesionales y simulación de mercado real
"""

import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Configurar path
sys.path.append('src')

from src.mt5_connector import MT5Connector
from src.features import SMCFeatureExtractor  
from src.strategy import SMCStrategy
from src.backtester_realistic import RealisticBacktester

class ProfessionalBacktest:
    """
    Backtesting con estándares profesionales y win rates realistas
    """
    
    def __init__(self):
        self.initial_balance = 10000
        
        # Configuración REALISTA
        self.pairs = ['EURUSD', 'GBPUSD']  # Menos pares para testing más profundo
        self.timeframes = ['H1'] 
        self.test_candles = {'H1': 3000}
        
    def run_realistic_backtest(self, symbol, timeframe):
        """
        Ejecuta backtesting con simulación REALISTA
        """
        print(f"📊 TESTING REALISTA {symbol} {timeframe}...")
        
        try:
            # Obtener datos
            connector = MT5Connector(symbol=symbol, timeframe=timeframe)
            num_candles = self.test_candles[timeframe]
            df = connector.fetch_ohlc_data(num_candles=num_candles)
            
            if df is None or len(df) < 500:
                print(f"❌ Datos insuficientes para {symbol} {timeframe}")
                return None
            
            print(f"   📈 Analizando {len(df)} velas...")
            
            # Extraer features SMC
            features_extractor = SMCFeatureExtractor(df)
            df_features = features_extractor.extract_all()
            
            # Generar señales
            strategy = SMCStrategy(df_features)
            df_signals = strategy.run()
            
            # BACKTESTING REALISTA
            backtester = RealisticBacktester(
                df_signals, 
                initial_balance=self.initial_balance,
                risk_per_trade=0.02,  # 2% riesgo (conservador)
                commission=0.00007    # Spread típico
            )
            
            results = backtester.run()
            
            # Calcular métricas profesionales
            metrics = self.calculate_professional_metrics(results)
            
            self.print_trade_analysis(results, metrics)
            
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
    
    def calculate_professional_metrics(self, results):
        """
        Calcula métricas con estándares profesionales
        """
        if not results['trades'] or len(results['trades']) == 0:
            return self.empty_metrics()
        
        trades_df = pd.DataFrame(results['trades'])
        
        # Separar winners y losers
        winners = trades_df[trades_df['was_profitable'] == True]
        losers = trades_df[trades_df['was_profitable'] == False]
        
        # Métricas básicas
        total_trades = len(trades_df)
        win_count = len(winners)
        loss_count = len(losers)
        win_rate = (win_count / total_trades * 100) if total_trades > 0 else 0
        
        # P&L
        total_pnl = trades_df['pnl'].sum()
        gross_profit = winners['pnl'].sum() if win_count > 0 else 0
        gross_loss = abs(losers['pnl'].sum()) if loss_count > 0 else 0.01
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0
        
        # Promedios
        avg_win = winners['pnl'].mean() if win_count > 0 else 0
        avg_loss = losers['pnl'].mean() if loss_count > 0 else 0
        avg_win_pips = winners['pnl_pips'].mean() if win_count > 0 else 0
        avg_loss_pips = abs(losers['pnl_pips'].mean()) if loss_count > 0 else 0
        
        # Risk-Reward Ratio
        risk_reward = avg_win_pips / avg_loss_pips if avg_loss_pips > 0 else 0
        
        # Equity curve analysis
        equity_series = pd.Series(results['equity_curve'])
        peak = equity_series.expanding().max()
        drawdown = (equity_series - peak) / peak * 100
        max_drawdown = abs(drawdown.min()) if len(drawdown) > 0 else 0
        
        # Retornos
        final_balance = results['final_balance']
        total_return = ((final_balance - self.initial_balance) / self.initial_balance * 100)
        
        # Sharpe Ratio aproximado (usando retornos diarios)
        if len(equity_series) > 1:
            returns = equity_series.pct_change().dropna()
            sharpe = returns.mean() / returns.std() * np.sqrt(252) if returns.std() > 0 else 0
        else:
            sharpe = 0
            
        # Calmar Ratio (retorno anual / max drawdown)
        calmar = abs(total_return / max_drawdown) if max_drawdown > 0 else 0
        
        return {
            # Básicas
            'total_trades': total_trades,
            'winning_trades': win_count,
            'losing_trades': loss_count,
            'win_rate': win_rate,
            
            # P&L
            'total_pnl': total_pnl,
            'gross_profit': gross_profit,
            'gross_loss': gross_loss,
            'profit_factor': profit_factor,
            
            # Promedios
            'avg_win': avg_win,
            'avg_loss': avg_loss,
            'avg_win_pips': avg_win_pips,
            'avg_loss_pips': avg_loss_pips,
            'risk_reward': risk_reward,
            
            # Retornos y riesgo
            'total_return': total_return,
            'max_drawdown': max_drawdown,
            'sharpe_ratio': sharpe,
            'calmar_ratio': calmar,
            'final_balance': final_balance,
            
            # Rachas
            'max_consecutive_wins': results.get('max_consecutive_wins', 0),
            'max_consecutive_losses': results.get('max_consecutive_losses', 0),
            
            # ML
            'ml_trained': results.get('ml_trained', False)
        }
    
    def empty_metrics(self):
        """Métricas vacías para cuando no hay trades"""
        return {k: 0 for k in [
            'total_trades', 'winning_trades', 'losing_trades', 'win_rate',
            'total_pnl', 'gross_profit', 'gross_loss', 'profit_factor',
            'avg_win', 'avg_loss', 'avg_win_pips', 'avg_loss_pips', 'risk_reward',
            'total_return', 'max_drawdown', 'sharpe_ratio', 'calmar_ratio',
            'final_balance', 'max_consecutive_wins', 'max_consecutive_losses'
        ]} | {'ml_trained': False, 'final_balance': self.initial_balance}
    
    def print_trade_analysis(self, results, metrics):
        """
        Análisis detallado de trades
        """
        if metrics['total_trades'] == 0:
            print("   ❌ NO se generaron trades")
            return
            
        print(f"\n📊 ANÁLISIS DE RESULTADOS:")
        print(f"   💼 Trades Totales: {metrics['total_trades']}")
        print(f"   ✅ Ganadores: {metrics['winning_trades']} ({metrics['win_rate']:.1f}%)")
        print(f"   ❌ Perdedores: {metrics['losing_trades']}")
        print(f"   💰 P&L Total: ${metrics['total_pnl']:+.2f}")
        print(f"   📈 Retorno: {metrics['total_return']:+.1f}%")
        print(f"   🎯 Profit Factor: {metrics['profit_factor']:.2f}")
        print(f"   📉 Max Drawdown: {metrics['max_drawdown']:.1f}%")
        print(f"   ⚡ Risk-Reward: 1:{metrics['risk_reward']:.2f}")
        
        # Clasificación de calidad
        self.classify_performance(metrics)
        
        # Mostrar algunos trades
        if len(results['trades']) > 0:
            print(f"\n🔍 ÚLTIMOS 5 TRADES:")
            for trade in results['trades'][-5:]:
                status = "✅WIN" if trade['was_profitable'] else "❌LOSS"
                print(f"   {status} {trade['type']} @ {trade['entry_price']:.5f} → "
                      f"{trade['exit_reason']} = ${trade['pnl']:+.2f}")
    
    def classify_performance(self, metrics):
        """
        Clasifica el rendimiento según estándares profesionales
        """
        win_rate = metrics['win_rate']
        profit_factor = metrics['profit_factor']
        sharpe = metrics['sharpe_ratio']
        max_dd = metrics['max_drawdown']
        
        print(f"\n🏆 EVALUACIÓN PROFESIONAL:")
        
        # Win Rate
        if win_rate >= 60:
            print(f"   📊 Win Rate: EXCELENTE ({win_rate:.1f}% - Profesional)")
        elif win_rate >= 45:
            print(f"   📊 Win Rate: BUENO ({win_rate:.1f}% - Aceptable)")
        elif win_rate >= 30:
            print(f"   📊 Win Rate: PROMEDIO ({win_rate:.1f}% - Mejorable)")
        else:
            print(f"   📊 Win Rate: BAJO ({win_rate:.1f}% - Necesita optimización)")
            
        # Profit Factor
        if profit_factor >= 2.0:
            print(f"   💰 Profit Factor: EXCELENTE ({profit_factor:.2f})")
        elif profit_factor >= 1.5:
            print(f"   💰 Profit Factor: BUENO ({profit_factor:.2f})")
        elif profit_factor >= 1.2:
            print(f"   💰 Profit Factor: ACEPTABLE ({profit_factor:.2f})")
        else:
            print(f"   💰 Profit Factor: BAJO ({profit_factor:.2f})")
            
        # Drawdown
        if max_dd <= 10:
            print(f"   📉 Drawdown: EXCELENTE ({max_dd:.1f}% - Bajo riesgo)")
        elif max_dd <= 20:
            print(f"   📉 Drawdown: BUENO ({max_dd:.1f}% - Riesgo moderado)")
        elif max_dd <= 30:
            print(f"   📉 Drawdown: ALTO ({max_dd:.1f}% - Cuidado)")
        else:
            print(f"   📉 Drawdown: CRÍTICO ({max_dd:.1f}% - Muy arriesgado)")
    
    def run_comprehensive_test(self):
        """
        Ejecuta testing profesional completo
        """
        print("🎯 BACKTESTING PROFESIONAL - Bot SMC-LIT")
        print("Estándares realistas de la industria")
        print("=" * 60)
        
        all_results = []
        
        for symbol in self.pairs:
            for timeframe in self.timeframes:
                result = self.run_realistic_backtest(symbol, timeframe)
                if result:
                    all_results.append(result)
        
        # Resumen final
        self.print_professional_summary(all_results)
        
        return all_results
    
    def print_professional_summary(self, results):
        """
        Resumen con estándares profesionales
        """
        print("\n" + "=" * 80)
        print("🏆 RESUMEN PROFESIONAL - ESTÁNDARES DE LA INDUSTRIA")
        print("=" * 80)
        
        if not results:
            print("❌ No se pudieron generar resultados válidos")
            return
        
        # Combinar métricas
        total_trades = sum(r['metrics']['total_trades'] for r in results)
        total_pnl = sum(r['metrics']['total_pnl'] for r in results)
        
        if total_trades == 0:
            print("❌ La estrategia no genera trades suficientes")
            print("\n🔧 RECOMENDACIONES PROFESIONALES:")
            print("   • Reducir filtros de entrada")
            print("   • Ajustar parámetros SMC/LIT")
            print("   • Considerar timeframes más bajos")
            print("   • Revisar umbrales de señales")
            return
        
        # Calcular métricas agregadas
        all_wins = sum(r['metrics']['winning_trades'] for r in results)
        combined_win_rate = (all_wins / total_trades * 100) if total_trades > 0 else 0
        combined_return = (total_pnl / self.initial_balance * 100)
        
        print(f"💼 CAPITAL INICIAL: ${self.initial_balance:,.2f}")
        print(f"💰 P&L TOTAL: ${total_pnl:+,.2f}")
        print(f"📊 TRADES TOTALES: {total_trades}")
        print(f"📈 WIN RATE PROMEDIO: {combined_win_rate:.1f}%")
        print(f"🎯 RETORNO TOTAL: {combined_return:+.1f}%")
        
        # Comparación con estándares
        print(f"\n📋 COMPARACIÓN CON ESTÁNDARES PROFESIONALES:")
        print(f"   • Bots Excelentes: 60-75% win rate")
        print(f"   • Bots Buenos: 50-65% win rate") 
        print(f"   • Bots Promedio: 40-55% win rate")
        print(f"   • Tu Bot: {combined_win_rate:.1f}% win rate")
        
        if combined_win_rate >= 60:
            print(f"   🏆 EVALUACIÓN: EXCELENTE - Nivel profesional")
        elif combined_win_rate >= 50:
            print(f"   🥈 EVALUACIÓN: BUENO - Comercializable")
        elif combined_win_rate >= 40:
            print(f"   🥉 EVALUACIÓN: PROMEDIO - Necesita mejoras")
        else:
            print(f"   ⚠️  EVALUACIÓN: BAJO - Requiere optimización")
        
        # Mostrar resultados por configuración
        print(f"\n📊 DETALLE POR CONFIGURACIÓN:")
        print("-" * 70)
        print(f"{'Par':<8} {'TF':<4} {'Trades':<7} {'Win%':<6} {'P&L':<12} {'Calidad':<12}")
        print("-" * 70)
        
        for result in results:
            m = result['metrics']
            quality = self.get_quality_rating(m['win_rate'], m['profit_factor'])
            print(f"{result['symbol']:<8} {result['timeframe']:<4} "
                  f"{m['total_trades']:<7} {m['win_rate']:<6.1f} "
                  f"${m['total_pnl']:<11.2f} {quality:<12}")
        
        print("-" * 70)
    
    def get_quality_rating(self, win_rate, profit_factor):
        """
        Califica la calidad de la estrategia
        """
        if win_rate >= 60 and profit_factor >= 1.5:
            return "EXCELENTE"
        elif win_rate >= 50 and profit_factor >= 1.3:
            return "BUENO"
        elif win_rate >= 40 and profit_factor >= 1.1:
            return "PROMEDIO"
        else:
            return "BAJO"

def main():
    """
    Función principal del backtesting profesional
    """
    print("🎯 Bot SMC-LIT - Backtesting con Estándares Profesionales")
    print("Win rates realistas, ML, y simulación de mercado real\n")
    
    backtester = ProfessionalBacktest()
    results = backtester.run_comprehensive_test()
    
    print(f"\n✅ Backtesting profesional completado!")
    print(f"📚 Referencia: Win rates según AlgoBot.com")
    
    # Guardar resultados
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    if results:
        summary_data = []
        for result in results:
            m = result['metrics']
            row = {
                'Symbol': result['symbol'],
                'Timeframe': result['timeframe'],
                'Total_Trades': m['total_trades'],
                'Win_Rate': m['win_rate'],
                'Total_PnL': m['total_pnl'],
                'Profit_Factor': m['profit_factor'],
                'Max_Drawdown': m['max_drawdown'],
                'Sharpe_Ratio': m['sharpe_ratio'],
                'Risk_Reward': m['risk_reward'],
                'ML_Trained': m['ml_trained']
            }
            summary_data.append(row)
        
        df_summary = pd.DataFrame(summary_data)
        csv_filename = f"professional_results_{timestamp}.csv"
        df_summary.to_csv(csv_filename, index=False)
        print(f"📁 Resultados guardados en: {csv_filename}")

if __name__ == "__main__":
    main() 