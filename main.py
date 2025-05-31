"""
main.py - Script principal para el bot de trading SMC-LIT con MetaTrader 5

Este script inicia el bot de trading automático SMC-LIT que:
1. Conecta con MetaTrader 5 usando las credenciales del archivo .env
2. Analiza patrones de mercado usando Smart Money Concepts (SMC) y Liquidity Inducement Theorem (LIT)
3. Ejecuta operaciones según señales generadas
4. Gestiona el riesgo y optimiza resultados usando IA
"""

import os
import sys
import time
import logging
import argparse
from datetime import datetime
import threading
import pandas as pd
import json
from dotenv import load_dotenv

# Asegurar que podemos importar módulos desde el directorio actual
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

# Importar componentes del bot
from src.mt5_connector import MT5Connector
from src.mt5_trader import MT5Trader
from src.features import SMCFeatureExtractor
from src.strategy import SMCStrategy
from src.backtester import Backtester
from src.trainer import SMCTrainer
from src.agent import SMCAgent
from src.utils import setup_logger

# Cargar variables de entorno (.env)
load_dotenv()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(f"smc_lit_bot_{datetime.now().strftime('%Y%m%d')}.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger('main')

def load_model(model_path):
    """
    Carga un modelo pre-entrenado.
    
    Args:
        model_path: Ruta al modelo
        
    Returns:
        model: Modelo cargado
    """
    try:
        import pickle
        with open(model_path, 'rb') as f:
            model = pickle.load(f)
        logger.info(f"Modelo cargado desde {model_path}")
        return model
    except Exception as e:
        logger.error(f"Error cargando modelo: {str(e)}")
        return None

def save_model(model, model_path):
    """
    Guarda un modelo entrenado.
    
    Args:
        model: Modelo a guardar
        model_path: Ruta donde guardar
    """
    try:
        os.makedirs(os.path.dirname(model_path), exist_ok=True)
        import pickle
        with open(model_path, 'wb') as f:
            pickle.dump(model, f)
        logger.info(f"Modelo guardado en {model_path}")
    except Exception as e:
        logger.error(f"Error guardando modelo: {str(e)}")

def train_model():
    """
    Entrena un nuevo modelo con datos históricos.
    
    Returns:
        model: Modelo entrenado
    """
    logger.info("Iniciando entrenamiento de modelo...")
    
    # Conectar a MT5
    connector = MT5Connector()
    
    try:
        # Descargar datos históricos
        df = connector.fetch_ohlc_data(num_candles=5000)
        
        # Extraer features
        features_extractor = SMCFeatureExtractor(df)
        df_features = features_extractor.extract_all()
        
        # Generar señales
        strategy = SMCStrategy(df_features)
        df_signals = strategy.run()
        
        # Simular backtesting
        backtester = Backtester(df_signals)
        df_bt = backtester.simulate()
        metrics = backtester.metrics()
        
        logger.info(f"Resultados del backtesting: {metrics}")
        
        # Entrenar modelo
        trainer = SMCTrainer(df_bt)
        model = trainer.train()
        
        # Guardar modelo
        save_model(model, 'models/smc_lit_model.pkl')
        
        return model
    
    except Exception as e:
        logger.error(f"Error entrenando modelo: {str(e)}")
        return None
    finally:
        # Desconectar
        connector.disconnect()

def run_bot(args):
    """
    Ejecuta el bot en modo de trading live.
    
    Args:
        args: Argumentos de línea de comandos
    """
    logger.info("Iniciando bot SMC-LIT en modo trading...")
    
    # Cargar modelo o entrenar nuevo
    model = None
    # NOTA: Entrenamiento deshabilitado temporalmente por errores de tipos
    # if args.train or not os.path.exists('models/smc_lit_model.pkl'):
    #     model = train_model()
    # else:
    #     model = load_model('models/smc_lit_model.pkl')
    
    # Por ahora usar sin modelo IA (solo SMC puro)
    logger.info("Ejecutando con estrategia SMC pura (sin modelo IA)")
    
    # Crear trader
    trader = MT5Trader(
        model=model,
        symbol=args.symbol,
        timeframe=args.timeframe,
        risk_percent=args.risk,
        max_trades=args.max_trades,
        update_interval=args.interval,
        use_ai=not args.no_ai,
        use_trailing=not args.no_trailing
    )
    
    # Iniciar trader
    if trader.start():
        try:
            logger.info(f"Bot SMC-LIT iniciado para {args.symbol} en {args.timeframe}")
            logger.info("Presiona Ctrl+C para detener")
            
            # Loop principal para mantener el proceso vivo
            while True:
                time.sleep(60)
                
                # Mostrar estadísticas cada minuto
                stats = trader.get_stats()
                logger.info(f"Estadísticas: {stats}")
                
        except KeyboardInterrupt:
            logger.info("Bot detenido por usuario")
        finally:
            # Detener trader
            trader.stop()

def run_backtest(args):
    """
    Ejecuta un backtest con los parámetros especificados.
    
    Args:
        args: Argumentos de línea de comandos
    """
    logger.info(f"Iniciando backtest para {args.symbol} en {args.timeframe}")
    
    # Conectar a MT5
    connector = MT5Connector(symbol=args.symbol, timeframe=args.timeframe)
    
    try:
        # Descargar datos históricos
        df = connector.fetch_ohlc_data(num_candles=args.candles)
        
        # Extraer features
        features_extractor = SMCFeatureExtractor(df)
        df_features = features_extractor.extract_all()
        
        # Generar señales
        strategy = SMCStrategy(df_features)
        df_signals = strategy.run()
        
        # Simular backtesting
        backtester = Backtester(df_signals)
        df_bt = backtester.simulate()
        metrics = backtester.metrics()
        
        logger.info(f"Resultados del backtesting para {args.symbol}:")
        logger.info(f"Periodo: {df['datetime'].iloc[0]} a {df['datetime'].iloc[-1]}")
        logger.info(f"Operaciones: {metrics['num_trades']}")
        logger.info(f"Winrate: {metrics['winrate']:.2%}")
        logger.info(f"Profit Factor: {metrics['profit_factor']:.2f}")
        logger.info(f"Drawdown máximo: {metrics['max_drawdown']:.2%}")
        
        # Guardar resultados
        os.makedirs('results', exist_ok=True)
        df_bt.to_csv(f"results/backtest_{args.symbol}_{args.timeframe}_{datetime.now().strftime('%Y%m%d')}.csv")
        
        # ¿Entrenar modelo con estos datos?
        if args.train:
            trainer = SMCTrainer(df_bt)
            model = trainer.train()
            save_model(model, f"models/smc_lit_{args.symbol}_{args.timeframe}.pkl")
    
    except Exception as e:
        logger.error(f"Error en backtest: {str(e)}")
    finally:
        # Desconectar
        connector.disconnect()

def parse_args():
    """
    Parsea los argumentos de línea de comandos.
    
    Returns:
        args: Argumentos parseados
    """
    parser = argparse.ArgumentParser(description='Bot de trading SMC-LIT con MetaTrader 5')
    
    subparsers = parser.add_subparsers(dest='command', help='Comando a ejecutar')
    
    # Comando: trade
    trade_parser = subparsers.add_parser('trade', help='Iniciar bot en modo trading')
    trade_parser.add_argument('--symbol', type=str, default='EURUSD', help='Símbolo a operar')
    trade_parser.add_argument('--timeframe', type=str, default='M5', help='Timeframe a utilizar')
    trade_parser.add_argument('--risk', type=float, default=1.0, help='Porcentaje de riesgo por operación')
    trade_parser.add_argument('--max-trades', type=int, default=5, help='Número máximo de operaciones simultáneas')
    trade_parser.add_argument('--interval', type=int, default=60, help='Intervalo de actualización en segundos')
    trade_parser.add_argument('--no-ai', action='store_true', help='Desactivar uso de IA')
    trade_parser.add_argument('--no-trailing', action='store_true', help='Desactivar trailing stop')
    trade_parser.add_argument('--train', action='store_true', help='Entrenar modelo antes de iniciar')
    
    # Comando: backtest
    backtest_parser = subparsers.add_parser('backtest', help='Ejecutar backtest')
    backtest_parser.add_argument('--symbol', type=str, default='EURUSD', help='Símbolo a testear')
    backtest_parser.add_argument('--timeframe', type=str, default='M5', help='Timeframe a utilizar')
    backtest_parser.add_argument('--candles', type=int, default=5000, help='Número de velas a analizar')
    backtest_parser.add_argument('--train', action='store_true', help='Entrenar modelo con los resultados')
    
    # Comando: train
    train_parser = subparsers.add_parser('train', help='Entrenar modelo')
    
    args = parser.parse_args()
    
    # Si no se especifica comando, usar 'trade'
    if not args.command:
        args.command = 'trade'
        args.symbol = 'EURUSD'
        args.timeframe = 'M5'
        args.risk = 1.0
        args.max_trades = 5
        args.interval = 60
        args.no_ai = False
        args.no_trailing = False
        args.train = False
    
    return args

def main():
    """
    Función principal que inicia el bot.
    """
    # Verificar credenciales en .env
    required_vars = ['MT5_LOGIN', 'MT5_PASSWORD', 'MT5_SERVER']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        logger.error(f"Faltan variables de entorno: {', '.join(missing_vars)}")
        logger.error("Asegúrate de crear un archivo .env con las credenciales de MT5")
        return
    
    # Parsear argumentos
    args = parse_args()
    
    # Ejecutar según el comando
    if args.command == 'trade':
        run_bot(args)
    elif args.command == 'backtest':
        run_backtest(args)
    elif args.command == 'train':
        train_model()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.error(f"Error crítico: {str(e)}")
        import traceback
        logger.error(traceback.format_exc()) 