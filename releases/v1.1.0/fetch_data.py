"""
Data Fetcher Module for SMC-LIT Trading Bot.

Este módulo maneja la descarga y preparación de datos de mercado desde diversas fuentes
para Smart Money Concepts (SMC) y Liquidity Inducement Theorem (LIT), incluyendo FXCM.
"""

import os
import logging
from typing import Dict, List, Optional, Tuple, Union
from datetime import datetime, timedelta

import pandas as pd
import numpy as np
import yfinance as yf
import ccxt
from dotenv import load_dotenv

# FXCM
try:
    import fxcmpy
except ImportError:
    fxcmpy = None

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('fetch_data')

# Load environment variables
load_dotenv()


class MarketDataFetcher:
    """
    Class for fetching and preparing market data from different sources.
    
    Supports multiple data sources including Yahoo Finance, Binance, FXCM, and other 
    exchanges through CCXT.
    """
    
    def __init__(
        self, 
        ticker: str = None, 
        start_date: str = None, 
        end_date: str = None, 
        interval: str = '1d',
        data_dir: str = "../data"
    ):
        """
        Initialize the MarketDataFetcher.
        
        Args:
            ticker: The market symbol to fetch, e.g., 'AAPL'
            start_date: The start date for fetching data in 'YYYY-MM-DD'
            end_date: The end date for fetching data in 'YYYY-MM-DD'
            interval: The data interval, e.g., '1d', '1h'
            data_dir: Directory to store downloaded data
        """
        self.ticker = ticker
        self.start_date = start_date
        self.end_date = end_date
        self.interval = interval
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialize exchange connections if API keys are provided
        self.exchanges: Dict[str, Optional[ccxt.Exchange]] = {}
        self._setup_exchanges()
        
    def _setup_exchanges(self) -> None:
        """Set up connections to cryptocurrency exchanges using CCXT."""
        # Binance setup
        binance_api_key = os.getenv('BINANCE_API_KEY')
        binance_secret = os.getenv('BINANCE_SECRET_KEY')
        
        if binance_api_key and binance_secret:
            try:
                self.exchanges['binance'] = ccxt.binance({
                    'apiKey': binance_api_key,
                    'secret': binance_secret,
                    'enableRateLimit': True
                })
                logger.info("Binance exchange initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Binance: {str(e)}")
                self.exchanges['binance'] = None
        else:
            logger.warning("Binance API credentials not found")
            self.exchanges['binance'] = None
            
        # Add more exchanges as needed

    def fetch_ohlc_data(self) -> pd.DataFrame:
        """
        Fetch OHLC market data using yfinance for the specified ticker and date range.

        Returns:
            DataFrame containing OHLC data
        """
        logger.info(f"Fetching {self.ticker} data: {self.interval} interval from {self.start_date} to {self.end_date}")
        
        data = yf.download(
            tickers=self.ticker,
            start=self.start_date,
            end=self.end_date,
            interval=self.interval,
            progress=False
        )

        # Ensuring the index is a DateTimeIndex
        data.index = pd.to_datetime(data.index)
        
        # Add symbol column
        data['symbol'] = self.ticker
            
        # Add datetime index as column for easier handling
        data['datetime'] = data.index

        # Logging the data fetching result
        logger.info(f"Fetched {len(data)} rows of data for {self.ticker}.")

        return data
    
    def fetch_yfinance_data(
        self, 
        symbol: str, 
        period: str = "2y", 
        interval: str = "1d",
        save: bool = True
    ) -> pd.DataFrame:
        """
        Fetch historical data from Yahoo Finance with period parameter.
        
        Args:
            symbol: Stock or asset symbol (e.g., 'AAPL', 'BTC-USD')
            period: Time period to fetch (e.g., '1d', '5d', '1mo', '3mo', '1y', '2y', 'max')
            interval: Data interval (e.g., '1m', '5m', '15m', '30m', '1h', '1d', '1wk', '1mo')
            save: Whether to save data to file
            
        Returns:
            DataFrame with OHLCV data and additional columns for analysis
        """
        logger.info(f"Fetching {symbol} data from Yahoo Finance: {interval} interval, {period} period")
        
        try:
            ticker = yf.Ticker(symbol)
            df = ticker.history(period=period, interval=interval)
            
            # Standardize column names
            df.columns = [col.lower() for col in df.columns]
            if 'adj close' in df.columns:
                df.rename(columns={'adj close': 'adj_close'}, inplace=True)
            
            # Add symbol column
            df['symbol'] = symbol
            
            # Add datetime index as column for easier handling
            df['datetime'] = df.index
            
            # Calculate log returns for analysis
            if len(df) > 1:
                df['log_return'] = np.log(df['close'] / df['close'].shift(1))
            
            if save:
                self._save_data(df, symbol, interval, 'yfinance')
                
            logger.info(f"Successfully fetched {len(df)} records for {symbol}")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching data for {symbol}: {str(e)}")
            raise
    
    def fetch_crypto_data(
        self,
        symbol: str,
        exchange: str = 'binance',
        timeframe: str = '1d',
        since: Optional[str] = None,
        limit: int = 1000,
        save: bool = True
    ) -> pd.DataFrame:
        """
        Fetch cryptocurrency data using CCXT.
        
        Args:
            symbol: Trading pair (e.g., 'BTC/USDT')
            exchange: Exchange name (e.g., 'binance', 'coinbase')
            timeframe: Data timeframe (e.g., '1m', '5m', '1h', '1d')
            since: Start date as ISO string or timestamp
            limit: Maximum number of candles to fetch
            save: Whether to save data to file
            
        Returns:
            DataFrame with OHLCV data
        """
        if exchange not in self.exchanges or self.exchanges[exchange] is None:
            raise ValueError(f"Exchange {exchange} not initialized")
        
        logger.info(f"Fetching {symbol} data from {exchange}: {timeframe} timeframe")
        
        try:
            # Convert since to timestamp if provided as string
            if since and isinstance(since, str):
                since = int(datetime.fromisoformat(since).timestamp() * 1000)
            
            # Fetch OHLCV data
            ex = self.exchanges[exchange]
            ohlcv = ex.fetch_ohlcv(symbol, timeframe, since, limit)
            
            # Convert to DataFrame
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['datetime'] = pd.to_datetime(df['timestamp'], unit='ms')
            df['symbol'] = symbol
            
            # Calculate log returns
            if len(df) > 1:
                df['log_return'] = np.log(df['close'] / df['close'].shift(1))
            
            if save:
                self._save_data(df, symbol.replace('/', '-'), timeframe, exchange)
                
            logger.info(f"Successfully fetched {len(df)} records for {symbol} from {exchange}")
            return df
            
        except Exception as e:
            logger.error(f"Error fetching {symbol} from {exchange}: {str(e)}")
            raise
    
    def fetch_fxcm_data(self, symbol: str, period: str = 'D1', n: int = 1000, save: bool = True) -> pd.DataFrame:
        """
        Fetch historical OHLC data from FXCM using fxcmpy.
        Args:
            symbol: FXCM symbol (e.g., 'EUR/USD')
            period: Timeframe (e.g., 'm1', 'm5', 'H1', 'D1')
            n: Number of candles
            save: Whether to save data to file
        Returns:
            DataFrame with OHLCV data
        """
        if fxcmpy is None:
            raise ImportError("fxcmpy is not installed. Please install it to use FXCM data.")
        fxcm_user = os.getenv('FXCM_USER')
        fxcm_password = os.getenv('FXCM_PASSWORD')
        fxcm_token = os.getenv('FXCM_TOKEN')
        fxcm_url = os.getenv('FXCM_URL', 'https://api-demo.fxcm.com')
        if not fxcm_token:
            raise ValueError("FXCM_TOKEN no encontrado en .env o variables de entorno.")
        logger.info(f"Conectando a FXCM para {symbol} periodo {period}...")
        con = fxcmpy.fxcmpy(access_token=fxcm_token, log_level='error', server='demo' if 'demo' in fxcm_url else 'real')
        df = con.get_candles(symbol, period=period, number=n)
        df['symbol'] = symbol
        df['datetime'] = df.index
        if save:
            self._save_data(df, symbol.replace('/', '-'), period, 'fxcm')
        logger.info(f"Descargadas {len(df)} velas de FXCM para {symbol}")
        con.close()
        return df
    
    def _save_data(
        self, 
        df: pd.DataFrame, 
        symbol: str, 
        interval: str, 
        source: str
    ) -> None:
        """
        Save data to CSV file.
        
        Args:
            df: DataFrame to save
            symbol: Trading symbol
            interval: Data interval/timeframe
            source: Data source name
        """
        # Create filename with relevant information
        safe_symbol = symbol.replace('/', '-').replace('\\', '-')
        filename = f"{safe_symbol}_{interval}_{source}_{datetime.now().strftime('%Y%m%d')}.csv"
        filepath = os.path.join(self.data_dir, filename)
        
        # Save to CSV
        df.to_csv(filepath, index=False)
        logger.info(f"Data saved to {filepath}")
    
    def load_data(
        self, 
        symbol: str, 
        interval: str = '1d', 
        source: str = 'yfinance',
        latest: bool = True
    ) -> pd.DataFrame:
        """
        Load previously saved data from file.
        
        Args:
            symbol: Trading symbol
            interval: Data interval/timeframe
            source: Data source name
            latest: Whether to load the latest file or search by exact match
            
        Returns:
            DataFrame with market data
        """
        safe_symbol = symbol.replace('/', '-').replace('\\', '-')
        
        if latest:
            # Find the latest file matching the pattern
            pattern = f"{safe_symbol}_{interval}_{source}_"
            matching_files = [f for f in os.listdir(self.data_dir) if f.startswith(pattern) and f.endswith('.csv')]
            
            if not matching_files:
                raise FileNotFoundError(f"No data files found for {symbol}, {interval}, {source}")
            
            # Sort by date (filename contains date at the end)
            latest_file = sorted(matching_files)[-1]
            filepath = os.path.join(self.data_dir, latest_file)
        else:
            # Find exact match for current date
            current_date = datetime.now().strftime('%Y%m%d')
            filename = f"{safe_symbol}_{interval}_{source}_{current_date}.csv"
            filepath = os.path.join(self.data_dir, filename)
            
            if not os.path.exists(filepath):
                raise FileNotFoundError(f"Data file not found: {filepath}")
        
        # Load data
        df = pd.read_csv(filepath)
        
        # Convert datetime column to pandas datetime
        if 'datetime' in df.columns:
            df['datetime'] = pd.to_datetime(df['datetime'])
            
        logger.info(f"Loaded data from {filepath}")
        return df

    def prepare_for_analysis(self, ohlc_data: pd.DataFrame) -> pd.DataFrame:
        """
        Prepares the OHLC data for SMC and LIT analysis by adding necessary derived columns.

        Args:
            ohlc_data: DataFrame containing raw OHLC data
            
        Returns:
            Enhanced DataFrame with additional columns for technical analysis
        """
        # Make a copy to avoid modifying the original
        df = ohlc_data.copy()
        
        # Standardize column names to lowercase
        df.columns = [col.lower() for col in df.columns]
        if 'adj close' in df.columns:
            df.rename(columns={'adj close': 'adj_close'}, inplace=True)
        
        # Ensure we have OHLCV columns standardized
        required_cols = ['open', 'high', 'low', 'close', 'volume']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        # Sorting the data by date in ascending order
        if isinstance(df.index, pd.DatetimeIndex):
            df.sort_index(ascending=True, inplace=True)
        elif 'datetime' in df.columns:
            df.sort_values('datetime', ascending=True, inplace=True)
            
        # Calculate basic price metrics for structure analysis
        df['body_size'] = abs(df['close'] - df['open'])
        df['upper_wick'] = df['high'] - df[['open', 'close']].max(axis=1)
        df['lower_wick'] = df[['open', 'close']].min(axis=1) - df['low']
        df['range'] = df['high'] - df['low']
        
        # Identify candle direction (important for SMC pattern recognition)
        df['bullish'] = df['close'] > df['open']
        
        # Calculate moving averages (useful for trend identification)
        for period in [20, 50, 200]:
            df[f'sma_{period}'] = df['close'].rolling(window=period).mean()
            
        # Calculate Average True Range (ATR) for volatility and stop loss determination
        df['tr'] = np.maximum(
            df['high'] - df['low'],
            np.maximum(
                abs(df['high'] - df['close'].shift(1)),
                abs(df['low'] - df['close'].shift(1))
            )
        )
        df['atr_14'] = df['tr'].rolling(window=14).mean()
        
        # Volume analysis (important for SMC confirmation)
        df['volume_sma_20'] = df['volume'].rolling(window=20).mean()
        df['volume_ratio'] = df['volume'] / df['volume_sma_20']
        
        # Add swing detection indicators (for Change of Character detection)
        # These will be enriched in the features.py module
        df['swing_high'] = False
        df['swing_low'] = False
        
        # Keep track of prior highs and lows for Order Block identification
        df['prev_high'] = df['high'].shift(1)
        df['prev_low'] = df['low'].shift(1)
        df['prev_close'] = df['close'].shift(1)
        
        # Calculate percentage moves for range analysis
        df['pct_change'] = df['close'].pct_change()
        
        return df


# Utility functions for direct usage
def get_market_data(
    symbol: str,
    interval: str = '1d',
    period: str = '2y',
    source: str = 'yfinance',
    save: bool = True
) -> pd.DataFrame:
    """
    Convenience function to quickly fetch market data.
    
    Args:
        symbol: Trading symbol
        interval: Data interval
        period: Time period to fetch
        source: Data source ('yfinance', 'crypto', 'fxcm')
        save: Whether to save data to file
        
    Returns:
        Prepared DataFrame with market data
    """
    fetcher = MarketDataFetcher(data_dir="../data")
    if source == 'yfinance':
        df = fetcher.fetch_yfinance_data(symbol, period, interval, save)
    elif source == 'crypto':
        period_map = {
            '1d': 1, '1w': 7, '1mo': 30, '3mo': 90,
            '6mo': 180, '1y': 365, '2y': 730, '5y': 1825
        }
        days = period_map.get(period, 365)
        since = (datetime.now() - timedelta(days=days)).isoformat()
        df = fetcher.fetch_crypto_data(symbol, timeframe=interval, since=since, save=save)
    elif source == 'fxcm':
        df = fetcher.fetch_fxcm_data(symbol, period=interval, n=1000, save=save)
    else:
        raise ValueError(f"Unsupported data source: {source}")
    return fetcher.prepare_for_analysis(df)


if __name__ == "__main__":
    # Example usage
    try:
        # Example 1: Fetch stock data
        spy_data = get_market_data('SPY', interval='1d', period='1y')
        print(f"Fetched {len(spy_data)} records for SPY")
        print(spy_data.head())
        
        # Example 2: Fetch crypto data
        # Note: This requires API keys set in .env file
        # btc_data = get_market_data('BTC/USDT', interval='1h', period='1mo', source='crypto')
        # print(f"Fetched {len(btc_data)} records for BTC/USDT")
        # print(btc_data.head())
        
    except Exception as e:
        logger.error(f"Error in example: {str(e)}")
