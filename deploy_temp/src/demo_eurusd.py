"""
demo_eurusd.py - Demostración del bot SMC-LIT con análisis completo de EUR/USD
"""

import sys
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from datetime import datetime, timedelta
import pytz
import MetaTrader5 as mt5
from dotenv import load_dotenv

# Importar componentes del bot
from src.features import SMCFeatureExtractor
from src.strategy import SMCStrategy
from src.backtester import Backtester
from src.trainer import SMCTrainer
from src.agent import SMCAgent
from src.utils import setup_logger

# Configurar logging
logger = setup_logger('demo_eurusd')

# Cargar variables de entorno
load_dotenv()

def connect_mt5():
    """Conectar a MetaTrader5 usando credenciales del .env"""
    if not mt5.initialize():
        logger.error(f"Error inicializando MT5: {mt5.last_error()}")
        return False
    
    login = int(os.getenv('MT5_LOGIN'))
    password = os.getenv('MT5_PASSWORD')
    server = os.getenv('MT5_SERVER')
    
    if not mt5.login(login=login, password=password, server=server):
        logger.error(f"Error de login en MT5: {mt5.last_error()}")
        return False
    
    logger.info(f"Conectado a MT5: {mt5.account_info().server}")
    return True

def get_eurusd_data(timeframe="M5", num_bars=1000):
    """Descargar datos de EUR/USD desde MT5"""
    symbol = "EURUSD"
    logger.info(f"Descargando {num_bars} velas de {symbol} {timeframe}")
    
    # Mapeo de timeframes
    tf_map = {
        "M1": mt5.TIMEFRAME_M1,
        "M5": mt5.TIMEFRAME_M5,
        "M15": mt5.TIMEFRAME_M15,
        "M30": mt5.TIMEFRAME_M30,
        "H1": mt5.TIMEFRAME_H1,
        "H4": mt5.TIMEFRAME_H4,
        "D1": mt5.TIMEFRAME_D1
    }
    
    mt5_tf = tf_map.get(timeframe, mt5.TIMEFRAME_M5)
    
    # Obtener datos desde MT5
    timezone = pytz.timezone("UTC")
    now = datetime.now(timezone)
    rates = mt5.copy_rates_from_pos(symbol, mt5_tf, 0, num_bars)
    
    if rates is None or len(rates) == 0:
        logger.error(f"Error descargando datos: {mt5.last_error()}")
        return None
    
    # Convertir a DataFrame
    df = pd.DataFrame(rates)
    df['time'] = pd.to_datetime(df['time'], unit='s')
    df.rename(columns={
        'time': 'datetime',
        'open': 'open',
        'high': 'high',
        'low': 'low',
        'close': 'close',
        'tick_volume': 'volume'
    }, inplace=True)
    
    # Añadir columnas necesarias para análisis
    df['symbol'] = symbol
    
    logger.info(f"Descargadas {len(df)} velas de {symbol}")
    return df

def prepare_data(df):
    """Preparar datos para análisis SMC-LIT"""
    # Calcular indicadores básicos
    df['body_size'] = abs(df['close'] - df['open'])
    df['upper_wick'] = df['high'] - df[['open', 'close']].max(axis=1)
    df['lower_wick'] = df[['open', 'close']].min(axis=1) - df['low']
    df['range'] = df['high'] - df['low']
    df['bullish'] = df['close'] > df['open']
    
    # Calcular medias móviles
    for period in [20, 50, 200]:
        df[f'sma_{period}'] = df['close'].rolling(window=period).mean()
    
    # Calcular ATR
    df['tr'] = np.maximum(
        df['high'] - df['low'],
        np.maximum(
            abs(df['high'] - df['close'].shift(1)),
            abs(df['low'] - df['close'].shift(1))
        )
    )
    df['atr_14'] = df['tr'].rolling(window=14).mean()
    
    # Análisis de volumen
    df['volume_sma_20'] = df['volume'].rolling(window=20).mean()
    df['volume_ratio'] = df['volume'] / df['volume_sma_20']
    
    # Datos para análisis de estructura
    df['prev_high'] = df['high'].shift(1)
    df['prev_low'] = df['low'].shift(1)
    df['prev_close'] = df['close'].shift(1)
    df['pct_change'] = df['close'].pct_change()
    
    return df.fillna(0)

def plot_results(df, title="EUR/USD Análisis SMC-LIT"):
    """Crear gráfico con resultados del análisis"""
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(15, 12), gridspec_kw={'height_ratios': [4, 1, 1]})
    
    # Gráfico de precios y señales
    ax1.plot(df['datetime'], df['close'], label='EUR/USD', color='blue', alpha=0.7)
    ax1.plot(df['datetime'], df['sma_20'], label='SMA 20', color='orange', alpha=0.6)
    ax1.plot(df['datetime'], df['sma_50'], label='SMA 50', color='green', alpha=0.6)
    
    # Marcar estructuras SMC
    for i in range(len(df)):
        if df['order_block'].iloc[i]:
            ax1.axvspan(df['datetime'].iloc[i], df['datetime'].iloc[i+1] if i+1 < len(df) else df['datetime'].iloc[i], 
                        alpha=0.3, color='green', label='Order Block' if i == 0 else "")
        if df['choch'].iloc[i]:
            ax1.scatter(df['datetime'].iloc[i], df['high'].iloc[i], marker='^', color='purple', s=100, 
                     label='Change of Character' if i == 0 else "")
        if df['bos'].iloc[i]:
            ax1.scatter(df['datetime'].iloc[i], df['low'].iloc[i], marker='v', color='red', s=100,
                     label='Break of Structure' if i == 0 else "")
        if df['liquidity_trap'].iloc[i]:
            ax1.axvspan(df['datetime'].iloc[i], df['datetime'].iloc[i+1] if i+1 < len(df) else df['datetime'].iloc[i],
                     alpha=0.3, color='red', label='Liquidity Trap' if i == 0 else "")
    
    # Marcar señales de trading
    buy_signals = df[df['signal'] == 1]
    sell_signals = df[df['signal'] == -1]
    
    if not buy_signals.empty:
        ax1.scatter(buy_signals['datetime'], buy_signals['close'], marker='^', color='green', s=200, label='Buy Signal')
    if not sell_signals.empty:
        ax1.scatter(sell_signals['datetime'], sell_signals['close'], marker='v', color='red', s=200, label='Sell Signal')
    
    # Graficar curva de equity
    if 'equity_curve' in df.columns:
        ax2.plot(df['datetime'], df['equity_curve'], color='green', label='Equity Curve')
        ax2.set_title('Curva de Capital')
        ax2.legend()
    
    # Graficar volumen y señales
    ax3.bar(df['datetime'], df['volume'], color='blue', alpha=0.3, label='Volume')
    ax3.plot(df['datetime'], df['volume_sma_20'], color='orange', label='Volume SMA 20')
    
    # Formatear eje X
    for ax in [ax1, ax2, ax3]:
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %H:%M'))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    
    ax1.set_title(title)
    ax1.legend()
    fig.tight_layout()
    
    # Guardar gráfico
    plt.savefig('eurusd_analysis.png')
    logger.info("Gráfico guardado como 'eurusd_analysis.png'")
    
    # Mostrar gráfico
    plt.show()

def run_demo():
    """Ejecutar demostración completa"""
    # 1. Conectar a MT5
    if not connect_mt5():
        logger.error("No se pudo conectar a MT5. Abortando.")
        return
    
    # 2. Descargar datos EUR/USD
    df = get_eurusd_data(timeframe="M5", num_bars=1000)
    if df is None:
        logger.error("No se pudieron obtener datos. Abortando.")
        return
    
    # 3. Preparar datos
    df = prepare_data(df)
    
    # 4. Extraer features SMC-LIT
    logger.info("Extrayendo features SMC-LIT...")
    features = SMCFeatureExtractor(df).extract_all()
    
    # 5. Generar señales
    logger.info("Generando señales de trading...")
    strategy = SMCStrategy(features)
    signals = strategy.run()
    
    # 6. Ejecutar backtesting
    logger.info("Ejecutando backtesting...")
    bt = Backtester(signals)
    df_bt = bt.simulate()
    metrics = bt.metrics()
    
    # 7. Entrenar modelo IA
    logger.info("Entrenando modelo IA...")
    trainer = SMCTrainer(df_bt)
    model = trainer.train()
    
    # 8. Aplicar modelo IA
    logger.info("Aplicando modelo IA...")
    agent = SMCAgent(model, features)
    ai_df = agent.act()
    
    # 9. Backtesting con IA
    ai_signals = df_bt.copy()
    ai_signals['signal'] = ai_df['ai_signal']
    bt_ai = Backtester(ai_signals)
    bt_ai.simulate()
    ai_metrics = bt_ai.metrics()
    
    # 10. Mostrar resultados
    logger.info("\n--- RESULTADOS DEL ANÁLISIS EUR/USD ---")
    logger.info(f"Periodo analizado: {df['datetime'].iloc[0]} a {df['datetime'].iloc[-1]}")
    logger.info(f"Total candles: {len(df)}")
    logger.info(f"Order Blocks detectados: {features['order_block'].sum()}")
    logger.info(f"Trampas de liquidez: {features['liquidity_trap'].sum()}")
    logger.info(f"Cambios de carácter (CHoCH): {features['choch'].sum()}")
    logger.info(f"Rupturas de estructura (BOS): {features['bos'].sum()}")
    
    logger.info("\n--- MÉTRICAS ESTRATEGIA SMC-LIT ---")
    logger.info(f"Señales generadas: {(signals['signal'] != 0).sum()}")
    logger.info(f"Operaciones: {metrics['num_trades']}")
    logger.info(f"Winrate: {metrics['winrate']:.2%}")
    logger.info(f"Profit Factor: {metrics['profit_factor']:.2f}")
    logger.info(f"Drawdown máximo: {metrics['max_drawdown']:.2%}")
    
    logger.info("\n--- MÉTRICAS ESTRATEGIA CON IA ---")
    logger.info(f"Señales generadas: {(ai_signals['signal'] != 0).sum()}")
    logger.info(f"Operaciones: {ai_metrics['num_trades']}")
    logger.info(f"Winrate: {ai_metrics['winrate']:.2%}")
    logger.info(f"Profit Factor: {ai_metrics['profit_factor']:.2f}")
    logger.info(f"Drawdown máximo: {ai_metrics['max_drawdown']:.2%}")
    
    # 11. Visualizar resultados
    plot_results(df_bt, "EUR/USD Análisis SMC-LIT")
    
    # 12. Cerrar conexión MT5
    mt5.shutdown()
    logger.info("Demostración completada exitosamente.")

if __name__ == "__main__":
    run_demo() 