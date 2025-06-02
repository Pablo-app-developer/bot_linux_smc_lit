#!/usr/bin/env python3
"""
Quick Backtesting para Bot SMC-LIT
Versión optimizada para resultados rápidos
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
from src.backtester import Backtester

class QuickBacktester:
    """
    Backtesting rápido para evaluación inicial del bot SMC-LIT
    """
    
    def __init__(self):
        self.results = {}
        
        # Configuración optimizada para velocidad
        self.currency_pairs = [
            'EURUSD',  # Par principal
            'GBPUSD',  # Par volátil
            'USDJPY'   # Par trending
        ]
        
        self.timeframes = [
            'M15',  # 15 minutos
            'H1',   # 1 hora
        ]
        
        # Períodos más cortos para testing rápido
        self.test_period_candles = {
            'M15': 2000,  # ~3 semanas
            'M30': 1000,  # ~3 semanas  
            'H1': 500,    # ~3 semanas
            'H4': 200     # ~1 mes
        }
        
    def calculate_metrics(self, trades_df, equity_curve):
        """
        Calcula métricas esenciales de trading
        """
        if trades_df.empty or len(equity_curve) < 2:
            return {
                'total_trades': 0,
                'win_rate': 0,
                'profit_factor': 0,
                'total_return': 0,
                'max_drawdown': 0,
                'total_pnl': 0,
                'avg_trade': 0,
                'best_trade': 0,
                'worst_trade': 0
            }
        
        # Métricas básicas
        total_trades = len(trades_df)
        winning_trades = trades_df[trades_df['pnl'] > 0]
        losing_trades = trades_df[trades_df['pnl'] <= 0]
        
        win_rate = len(winning_trades) / total_trades if total_trades > 0 else 0
        
        # Profit Factor
        gross_profit = winning_trades['pnl'].sum() if len(winning_trades) > 0 else 0
        gross_loss = abs(losing_trades['pnl'].sum()) if len(losing_trades) > 0 else 0.01
        profit_factor = gross_profit / gross_loss if gross_loss > 0 else 0
        
        # Returns
        initial_balance = equity_curve[0]
        final_balance = equity_curve[-1]
        total_return = (final_balance - initial_balance) / initial_balance
        
        # Drawdown
        peak = pd.Series(equity_curve).expanding().max()
        drawdown = (pd.Series(equity_curve) - peak) / peak
        max_drawdown = abs(drawdown.min())
        
        # Trade statistics
        total_pnl = trades_df['pnl'].sum()
        avg_trade = trades_df['pnl'].mean()
        best_trade = trades_df['pnl'].max()
        worst_trade = trades_df['pnl'].min()
        
        return {
            'total_trades': total_trades,
            'win_rate': win_rate,
            'profit_factor': profit_factor,
            'total_return': total_return,
            'max_drawdown': max_drawdown,
            'total_pnl': total_pnl,
            'avg_trade': avg_trade,
            'best_trade': best_trade,
            'worst_trade': worst_trade
        }
    
    def run_single_test(self, symbol, timeframe):
        """
        Ejecuta un test individual optimizado
        """
        print(f"⚡ Testing {symbol} {timeframe}...")
        
        try:
            # Conectar
            connector = MT5Connector(symbol=symbol, timeframe=timeframe)
            
            # Obtener datos
            num_candles = self.test_period_candles[timeframe]
            df = connector.fetch_ohlc_data(num_candles=num_candles)
            
            if df is None or len(df) < 200:
                print(f"   ❌ Datos insuficientes")
                connector.disconnect()
                return None
            
            print(f"   📊 {len(df)} velas | {df['datetime'].iloc[0].strftime('%m-%d')} - {df['datetime'].iloc[-1].strftime('%m-%d')}")
            
            # Extraer features SMC
            features_extractor = SMCFeatureExtractor(df)
            df_features = features_extractor.extract_all()
            
            if df_features is None or len(df_features) < 100:
                print(f"   ❌ Error en features")
                connector.disconnect()
                return None
            
            # Generar señales
            strategy = SMCStrategy(df_features)
            df_signals = strategy.run()
            
            if df_signals is None or len(df_signals) < 50:
                print(f"   ❌ Error en estrategia")
                connector.disconnect()
                return None
            
            # Contar señales generadas
            buy_signals = (df_signals['signal'] == 1).sum()
            sell_signals = (df_signals['signal'] == -1).sum()
            print(f"   📈 Señales: {buy_signals} BUY, {sell_signals} SELL")
            
            # Ejecutar backtesting
            backtester = Backtester(df_signals)
            df_bt = backtester.simulate()
            
            # Extraer trades
            trades = []
            equity_curve = [10000]
            current_balance = 10000
            
            trade_count = 0
            for _, row in df_bt.iterrows():
                if pd.notna(row.get('trade_pnl', np.nan)):
                    trade_pnl = row['trade_pnl']
                    trade_count += 1
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
            
            # Calcular métricas
            metrics = self.calculate_metrics(trades_df, equity_curve)
            
            print(f"   ✅ {metrics['total_trades']} trades | Win: {metrics['win_rate']:.1%} | Return: {metrics['total_return']:.1%} | PF: {metrics['profit_factor']:.2f}")
            
            connector.disconnect()
            
            return {
                'symbol': symbol,
                'timeframe': timeframe,
                'trades_df': trades_df,
                'equity_curve': equity_curve,
                **metrics
            }
            
        except Exception as e:
            print(f"   ❌ Error: {str(e)}")
            return None
    
    def run_quick_analysis(self):
        """
        Ejecuta análisis rápido en configuraciones seleccionadas
        """
        print("⚡ QUICK BACKTESTING SMC-LIT")
        print("=" * 50)
        
        total_tests = len(self.currency_pairs) * len(self.timeframes)
        current_test = 0
        
        for symbol in self.currency_pairs:
            self.results[symbol] = {}
            
            for timeframe in self.timeframes:
                current_test += 1
                print(f"\n[{current_test}/{total_tests}] {symbol} - {timeframe}")
                
                result = self.run_single_test(symbol, timeframe)
                if result:
                    self.results[symbol][timeframe] = result
        
        print(f"\n✅ Testing completado!")
        
    def print_summary(self):
        """
        Imprime resumen rápido de resultados
        """
        print("\n" + "="*60)
        print("📊 RESUMEN RÁPIDO DE RESULTADOS")
        print("="*60)
        
        # Recopilar resultados
        all_results = []
        for symbol in self.results:
            for timeframe in self.results[symbol]:
                all_results.append(self.results[symbol][timeframe])
        
        if not all_results:
            print("❌ No hay resultados para mostrar")
            return
        
        # Mostrar tabla de resultados
        print(f"\n{'Par':<8} {'TF':<4} {'Trades':<7} {'Win%':<6} {'Return%':<8} {'PF':<6} {'DD%':<6}")
        print("-" * 50)
        
        for result in all_results:
            print(f"{result['symbol']:<8} {result['timeframe']:<4} {result['total_trades']:<7} "
                  f"{result['win_rate']:.1%}  {result['total_return']:.1%}    "
                  f"{result['profit_factor']:.2f}   {result['max_drawdown']:.1%}")
        
        # Estadísticas generales
        profitable_configs = [r for r in all_results if r['total_return'] > 0]
        avg_return = np.mean([r['total_return'] for r in all_results])
        avg_trades = np.mean([r['total_trades'] for r in all_results])
        avg_win_rate = np.mean([r['win_rate'] for r in all_results])
        
        print(f"\n🎯 ESTADÍSTICAS GENERALES:")
        print(f"   • Configuraciones probadas: {len(all_results)}")
        print(f"   • Configuraciones rentables: {len(profitable_configs)}/{len(all_results)} ({len(profitable_configs)/len(all_results):.1%})")
        print(f"   • Retorno promedio: {avg_return:.1%}")
        print(f"   • Trades promedio: {avg_trades:.0f}")
        print(f"   • Win rate promedio: {avg_win_rate:.1%}")
        
        # Mejores performers
        if profitable_configs:
            best_return = max(profitable_configs, key=lambda x: x['total_return'])
            best_trades = max(all_results, key=lambda x: x['total_trades'])
            
            print(f"\n🏆 MEJORES RESULTADOS:")
            print(f"   • Mejor retorno: {best_return['symbol']} {best_return['timeframe']} ({best_return['total_return']:.1%})")
            print(f"   • Más trades: {best_trades['symbol']} {best_trades['timeframe']} ({best_trades['total_trades']} trades)")
        
        # Recomendaciones
        print(f"\n💡 RECOMENDACIONES RÁPIDAS:")
        good_configs = [r for r in all_results if r['total_return'] > 0.02 and r['total_trades'] > 5]
        
        if good_configs:
            print(f"   ✅ Configuraciones prometedoras para deploy:")
            for config in sorted(good_configs, key=lambda x: x['total_return'], reverse=True)[:3]:
                print(f"      • {config['symbol']} {config['timeframe']}: {config['total_return']:.1%} return con {config['total_trades']} trades")
        else:
            print(f"   ⚠️  Se requiere optimización de parámetros")
            print(f"   💡 Sugerencias:")
            print(f"      - Ajustar umbrales de señales SMC")
            print(f"      - Revisar filtros de LIT")
            print(f"      - Considerar timeframes diferentes")
        
        print("="*60)
    
    def create_quick_chart(self):
        """
        Crea gráfico rápido de los mejores resultados
        """
        try:
            # Encontrar mejor resultado
            best_result = None
            best_return = -999
            
            for symbol in self.results:
                for timeframe in self.results[symbol]:
                    result = self.results[symbol][timeframe]
                    if result['total_return'] > best_return and result['total_trades'] > 0:
                        best_return = result['total_return']
                        best_result = result
            
            if best_result is None:
                print("📈 No hay datos suficientes para gráfico")
                return
            
            # Crear gráfico
            plt.figure(figsize=(12, 8))
            
            # Equity curve
            plt.subplot(2, 1, 1)
            equity = best_result['equity_curve']
            plt.plot(equity, 'b-', linewidth=2, label=f"Equity Curve")
            plt.title(f"Mejor Resultado: {best_result['symbol']} {best_result['timeframe']} ({best_result['total_return']:.1%})")
            plt.ylabel('Balance ($)')
            plt.grid(True, alpha=0.3)
            plt.legend()
            
            # Trade distribution
            plt.subplot(2, 1, 2)
            if not best_result['trades_df'].empty:
                trades_pnl = best_result['trades_df']['pnl']
                plt.hist(trades_pnl, bins=20, alpha=0.7, edgecolor='black')
                plt.axvline(x=0, color='red', linestyle='--', alpha=0.8)
                plt.title('Distribución de P&L por Trade')
                plt.xlabel('P&L ($)')
                plt.ylabel('Frecuencia')
                plt.grid(True, alpha=0.3)
            
            plt.tight_layout()
            
            # Guardar
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f'quick_backtest_{timestamp}.png'
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"📊 Gráfico guardado como '{filename}'")
            
        except Exception as e:
            print(f"❌ Error creando gráfico: {str(e)}")

def main():
    """Función principal del quick backtesting"""
    backtester = QuickBacktester()
    
    try:
        # Ejecutar análisis rápido
        backtester.run_quick_analysis()
        
        # Mostrar resumen
        backtester.print_summary()
        
        # Crear gráfico
        backtester.create_quick_chart()
        
        print(f"\n✅ ¡Quick backtesting completado!")
        
    except Exception as e:
        print(f"❌ Error en quick backtesting: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 