"""
Alpha Vantage Data Provider
Enhanced market data with technical indicators
"""

import requests
import pandas as pd
from datetime import datetime
import time

class AlphaVantageProvider:
    def __init__(self, api_key="6POZJ38W61I4MR9H"):
        self.api_key = api_key
        self.base_url = "https://www.alphavantage.co/query"
        self.cache = {}
        self.last_call_time = 0
        self.call_delay = 12  # 5 calls per minute = 12 seconds between calls
        
    def _rate_limit(self):
        """Enforce rate limiting"""
        current_time = time.time()
        time_since_last_call = current_time - self.last_call_time
        if time_since_last_call < self.call_delay:
            time.sleep(self.call_delay - time_since_last_call)
        self.last_call_time = time.time()
    
    def _make_request(self, params):
        """Make API request with rate limiting"""
        self._rate_limit()
        params['apikey'] = self.api_key
        
        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            # Check for API errors
            if "Error Message" in data:
                raise Exception(f"API Error: {data['Error Message']}")
            if "Note" in data:
                raise Exception(f"API Limit: {data['Note']}")
                
            return data
        except Exception as e:
            print(f"❌ Alpha Vantage Error: {str(e)}")
            return None
    
    def get_quote(self, symbol):
        """Get real-time quote"""
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': symbol
        }
        
        data = self._make_request(params)
        if not data or 'Global Quote' not in data:
            return None
            
        quote = data['Global Quote']
        return {
            'symbol': quote.get('01. symbol'),
            'price': float(quote.get('05. price', 0)),
            'change': float(quote.get('09. change', 0)),
            'change_percent': quote.get('10. change percent', '0%').replace('%', ''),
            'volume': int(quote.get('06. volume', 0)),
            'latest_trading_day': quote.get('07. latest trading day'),
            'previous_close': float(quote.get('08. previous close', 0)),
            'open': float(quote.get('02. open', 0)),
            'high': float(quote.get('03. high', 0)),
            'low': float(quote.get('04. low', 0))
        }
    
    def get_rsi(self, symbol, interval='daily', time_period=14):
        """Get RSI indicator"""
        params = {
            'function': 'RSI',
            'symbol': symbol,
            'interval': interval,
            'time_period': time_period,
            'series_type': 'close'
        }
        
        data = self._make_request(params)
        if not data or 'Technical Analysis: RSI' not in data:
            return None
            
        rsi_data = data['Technical Analysis: RSI']
        latest_date = list(rsi_data.keys())[0]
        rsi_value = float(rsi_data[latest_date]['RSI'])
        
        # Interpret RSI
        if rsi_value > 70:
            signal = "OVERBOUGHT"
            sentiment = "bearish"
        elif rsi_value < 30:
            signal = "OVERSOLD"
            sentiment = "bullish"
        else:
            signal = "NEUTRAL"
            sentiment = "neutral"
        
        return {
            'value': rsi_value,
            'signal': signal,
            'sentiment': sentiment,
            'date': latest_date
        }
    
    def get_macd(self, symbol, interval='daily'):
        """Get MACD indicator"""
        params = {
            'function': 'MACD',
            'symbol': symbol,
            'interval': interval,
            'series_type': 'close'
        }
        
        data = self._make_request(params)
        if not data or 'Technical Analysis: MACD' not in data:
            return None
            
        macd_data = data['Technical Analysis: MACD']
        latest_date = list(macd_data.keys())[0]
        latest = macd_data[latest_date]
        
        macd = float(latest['MACD'])
        signal = float(latest['MACD_Signal'])
        histogram = float(latest['MACD_Hist'])
        
        # Interpret MACD
        if macd > signal and histogram > 0:
            trend = "BULLISH"
            sentiment = "bullish"
        elif macd < signal and histogram < 0:
            trend = "BEARISH"
            sentiment = "bearish"
        else:
            trend = "NEUTRAL"
            sentiment = "neutral"
        
        return {
            'macd': macd,
            'signal': signal,
            'histogram': histogram,
            'trend': trend,
            'sentiment': sentiment,
            'date': latest_date
        }
    
    def get_ema(self, symbol, interval='daily', time_period=50):
        """Get EMA (Exponential Moving Average)"""
        params = {
            'function': 'EMA',
            'symbol': symbol,
            'interval': interval,
            'time_period': time_period,
            'series_type': 'close'
        }
        
        data = self._make_request(params)
        if not data or 'Technical Analysis: EMA' not in data:
            return None
            
        ema_data = data['Technical Analysis: EMA']
        latest_date = list(ema_data.keys())[0]
        ema_value = float(ema_data[latest_date]['EMA'])
        
        return {
            'value': ema_value,
            'period': time_period,
            'date': latest_date
        }
    
    def get_bbands(self, symbol, interval='daily', time_period=20):
        """Get Bollinger Bands"""
        params = {
            'function': 'BBANDS',
            'symbol': symbol,
            'interval': interval,
            'time_period': time_period,
            'series_type': 'close'
        }
        
        data = self._make_request(params)
        if not data or 'Technical Analysis: BBANDS' not in data:
            return None
            
        bbands_data = data['Technical Analysis: BBANDS']
        latest_date = list(bbands_data.keys())[0]
        latest = bbands_data[latest_date]
        
        return {
            'upper': float(latest['Real Upper Band']),
            'middle': float(latest['Real Middle Band']),
            'lower': float(latest['Real Lower Band']),
            'date': latest_date
        }
    
    def get_comprehensive_analysis(self, symbol):
        """Get comprehensive technical analysis"""
        print(f"📊 Analyzing {symbol} with Alpha Vantage...")
        
        # Get quote
        quote = self.get_quote(symbol)
        if not quote:
            return None
        
        # Get technical indicators (with delays)
        rsi = self.get_rsi(symbol)
        macd = self.get_macd(symbol)
        ema_50 = self.get_ema(symbol, time_period=50)
        bbands = self.get_bbands(symbol)
        
        # Calculate overall sentiment
        sentiments = []
        if rsi:
            sentiments.append(rsi['sentiment'])
        if macd:
            sentiments.append(macd['sentiment'])
        
        bullish_count = sentiments.count('bullish')
        bearish_count = sentiments.count('bearish')
        
        if bullish_count > bearish_count:
            overall_sentiment = "BULLISH"
        elif bearish_count > bullish_count:
            overall_sentiment = "BEARISH"
        else:
            overall_sentiment = "NEUTRAL"
        
        return {
            'symbol': symbol,
            'quote': quote,
            'rsi': rsi,
            'macd': macd,
            'ema_50': ema_50,
            'bbands': bbands,
            'overall_sentiment': overall_sentiment,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

# Symbol mapping for different assets
SYMBOL_MAP = {
    'gold': 'GLD',  # SPDR Gold Trust ETF
    'silver': 'SLV',  # iShares Silver Trust
    'bitcoin': 'GBTC',  # Grayscale Bitcoin Trust (proxy)
    'sp500': 'SPY',  # S&P 500 ETF
    'oil': 'USO'  # United States Oil Fund
}

def get_symbol(asset_name):
    """Get Alpha Vantage symbol for asset"""
    return SYMBOL_MAP.get(asset_name.lower(), asset_name)

if __name__ == "__main__":
    # Test the provider
    provider = AlphaVantageProvider()
    
    # Test Gold analysis
    print("Testing Gold analysis...")
    analysis = provider.get_comprehensive_analysis('GLD')
    
    if analysis:
        print(f"\n✅ {analysis['symbol']} Analysis:")
        print(f"Price: ${analysis['quote']['price']:.2f}")
        print(f"Change: {analysis['quote']['change_percent']}%")
        if analysis['rsi']:
            print(f"RSI: {analysis['rsi']['value']:.2f} ({analysis['rsi']['signal']})")
        if analysis['macd']:
            print(f"MACD: {analysis['macd']['trend']}")
        print(f"Overall: {analysis['overall_sentiment']}")
    else:
        print("❌ Analysis failed")

