"""
TradingView Data Provider
Real-time market data and technical analysis from TradingView
"""

from tradingview_ta import TA_Handler, Interval, Exchange
import time
from datetime import datetime

class TradingViewProvider:
    def __init__(self):
        self.cache = {}
        self.cache_duration = 60  # Cache for 60 seconds
        
    def _get_handler(self, symbol, screener="america", exchange="", interval=Interval.INTERVAL_1_DAY):
        """Create TA_Handler for symbol"""
        return TA_Handler(
            symbol=symbol,
            screener=screener,
            exchange=exchange,
            interval=interval
        )
    
    def _get_cached_or_fetch(self, cache_key, fetch_func):
        """Get from cache or fetch new data"""
        current_time = time.time()
        
        if cache_key in self.cache:
            cached_data, cached_time = self.cache[cache_key]
            if current_time - cached_time < self.cache_duration:
                return cached_data
        
        # Fetch new data
        data = fetch_func()
        self.cache[cache_key] = (data, current_time)
        return data
    
    def get_gold_analysis(self):
        """Get Gold (GC) analysis"""
        cache_key = "gold_analysis"
        
        def fetch():
            try:
                # Try multiple symbol formats
                for symbol, exchange in [("XAUUSD", "FX_IDC"), ("GOLD", "TVC"), ("GC1!", "COMEX")]:
                    try:
                        handler = self._get_handler(
                            symbol=symbol,
                            screener="forex" if symbol == "XAUUSD" else "america",
                            exchange=exchange,
                            interval=Interval.INTERVAL_1_DAY
                        )
                        break
                    except:
                        continue
                analysis = handler.get_analysis()
                
                return {
                    'symbol': 'GOLD',
                    'price': analysis.indicators.get('close', 0),
                    'open': analysis.indicators.get('open', 0),
                    'high': analysis.indicators.get('high', 0),
                    'low': analysis.indicators.get('low', 0),
                    'change': analysis.indicators.get('change', 0),
                    'change_percent': analysis.indicators.get('change', 0) / analysis.indicators.get('close', 1) * 100 if analysis.indicators.get('close') else 0,
                    'volume': analysis.indicators.get('volume', 0),
                    'rsi': analysis.indicators.get('RSI', None),
                    'macd': analysis.indicators.get('MACD.macd', None),
                    'macd_signal': analysis.indicators.get('MACD.signal', None),
                    'ema_50': analysis.indicators.get('EMA50', None),
                    'ema_200': analysis.indicators.get('EMA200', None),
                    'sma_50': analysis.indicators.get('SMA50', None),
                    'sma_200': analysis.indicators.get('SMA200', None),
                    'recommendation': analysis.summary.get('RECOMMENDATION', 'NEUTRAL'),
                    'buy_signals': analysis.summary.get('BUY', 0),
                    'sell_signals': analysis.summary.get('SELL', 0),
                    'neutral_signals': analysis.summary.get('NEUTRAL', 0),
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            except Exception as e:
                print(f"❌ TradingView Gold Error: {str(e)}")
                return None
        
        return self._get_cached_or_fetch(cache_key, fetch)
    
    def get_silver_analysis(self):
        """Get Silver (SI) analysis"""
        cache_key = "silver_analysis"
        
        def fetch():
            try:
                # Try multiple symbol formats
                for symbol, exchange in [("XAGUSD", "FX_IDC"), ("SILVER", "TVC"), ("SI1!", "COMEX")]:
                    try:
                        handler = self._get_handler(
                            symbol=symbol,
                            screener="forex" if symbol == "XAGUSD" else "america",
                            exchange=exchange,
                            interval=Interval.INTERVAL_1_DAY
                        )
                        break
                    except:
                        continue
                analysis = handler.get_analysis()
                
                return {
                    'symbol': 'SILVER',
                    'price': analysis.indicators.get('close', 0),
                    'open': analysis.indicators.get('open', 0),
                    'high': analysis.indicators.get('high', 0),
                    'low': analysis.indicators.get('low', 0),
                    'change': analysis.indicators.get('change', 0),
                    'change_percent': analysis.indicators.get('change', 0) / analysis.indicators.get('close', 1) * 100 if analysis.indicators.get('close') else 0,
                    'rsi': analysis.indicators.get('RSI', None),
                    'macd': analysis.indicators.get('MACD.macd', None),
                    'ema_50': analysis.indicators.get('EMA50', None),
                    'recommendation': analysis.summary.get('RECOMMENDATION', 'NEUTRAL'),
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            except Exception as e:
                print(f"❌ TradingView Silver Error: {str(e)}")
                return None
        
        return self._get_cached_or_fetch(cache_key, fetch)
    
    def get_bitcoin_analysis(self):
        """Get Bitcoin (BTC/USD) analysis"""
        cache_key = "bitcoin_analysis"
        
        def fetch():
            try:
                handler = self._get_handler(
                    symbol="BTCUSD",
                    screener="crypto",
                    exchange="BINANCE",
                    interval=Interval.INTERVAL_1_DAY
                )
                analysis = handler.get_analysis()
                
                return {
                    'symbol': 'BITCOIN',
                    'price': analysis.indicators.get('close', 0),
                    'open': analysis.indicators.get('open', 0),
                    'high': analysis.indicators.get('high', 0),
                    'low': analysis.indicators.get('low', 0),
                    'change': analysis.indicators.get('change', 0),
                    'change_percent': analysis.indicators.get('change', 0) / analysis.indicators.get('close', 1) * 100 if analysis.indicators.get('close') else 0,
                    'volume': analysis.indicators.get('volume', 0),
                    'rsi': analysis.indicators.get('RSI', None),
                    'macd': analysis.indicators.get('MACD.macd', None),
                    'macd_signal': analysis.indicators.get('MACD.signal', None),
                    'ema_50': analysis.indicators.get('EMA50', None),
                    'ema_200': analysis.indicators.get('EMA200', None),
                    'recommendation': analysis.summary.get('RECOMMENDATION', 'NEUTRAL'),
                    'buy_signals': analysis.summary.get('BUY', 0),
                    'sell_signals': analysis.summary.get('SELL', 0),
                    'neutral_signals': analysis.summary.get('NEUTRAL', 0),
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            except Exception as e:
                print(f"❌ TradingView Bitcoin Error: {str(e)}")
                return None
        
        return self._get_cached_or_fetch(cache_key, fetch)
    
    def get_sp500_analysis(self):
        """Get S&P 500 analysis"""
        cache_key = "sp500_analysis"
        
        def fetch():
            try:
                handler = self._get_handler(
                    symbol="SPX",
                    screener="america",
                    exchange="SP",
                    interval=Interval.INTERVAL_1_DAY
                )
                analysis = handler.get_analysis()
                
                return {
                    'symbol': 'S&P 500',
                    'price': analysis.indicators.get('close', 0),
                    'change_percent': analysis.indicators.get('change', 0) / analysis.indicators.get('close', 1) * 100 if analysis.indicators.get('close') else 0,
                    'rsi': analysis.indicators.get('RSI', None),
                    'recommendation': analysis.summary.get('RECOMMENDATION', 'NEUTRAL'),
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            except Exception as e:
                print(f"❌ TradingView S&P 500 Error: {str(e)}")
                return None
        
        return self._get_cached_or_fetch(cache_key, fetch)
    
    def get_vix_analysis(self):
        """Get VIX (Volatility Index) analysis"""
        cache_key = "vix_analysis"
        
        def fetch():
            try:
                handler = self._get_handler(
                    symbol="VIX",
                    screener="america",
                    exchange="CBOE",
                    interval=Interval.INTERVAL_1_DAY
                )
                analysis = handler.get_analysis()
                
                vix_value = analysis.indicators.get('close', 0)
                
                # Interpret VIX
                if vix_value < 15:
                    sentiment = "COMPLACENCY"
                    risk_level = "LOW"
                elif vix_value < 20:
                    sentiment = "NORMAL"
                    risk_level = "MEDIUM"
                elif vix_value < 30:
                    sentiment = "FEAR"
                    risk_level = "HIGH"
                else:
                    sentiment = "PANIC"
                    risk_level = "CRITICAL"
                
                return {
                    'symbol': 'VIX',
                    'value': vix_value,
                    'sentiment': sentiment,
                    'risk_level': risk_level,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            except Exception as e:
                print(f"❌ TradingView VIX Error: {str(e)}")
                return None
        
        return self._get_cached_or_fetch(cache_key, fetch)
    
    def get_comprehensive_market_overview(self):
        """Get comprehensive market overview"""
        print("📊 Fetching comprehensive market data from TradingView...")
        
        gold = self.get_gold_analysis()
        silver = self.get_silver_analysis()
        bitcoin = self.get_bitcoin_analysis()
        sp500 = self.get_sp500_analysis()
        vix = self.get_vix_analysis()
        
        return {
            'gold': gold,
            'silver': silver,
            'bitcoin': bitcoin,
            'sp500': sp500,
            'vix': vix,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

if __name__ == "__main__":
    # Test the provider
    provider = TradingViewProvider()
    
    print("Testing TradingView Provider...")
    print("\n" + "="*50)
    
    # Test Gold
    print("\n💰 GOLD:")
    gold = provider.get_gold_analysis()
    if gold:
        print(f"Price: ${gold['price']:,.2f}")
        print(f"Change: {gold['change_percent']:+.2f}%")
        print(f"RSI: {gold['rsi']:.1f}" if gold['rsi'] else "RSI: N/A")
        print(f"Recommendation: {gold['recommendation']}")
    
    # Test Silver
    print("\n🥈 SILVER:")
    silver = provider.get_silver_analysis()
    if silver:
        print(f"Price: ${silver['price']:,.2f}")
        print(f"Change: {silver['change_percent']:+.2f}%")
        print(f"RSI: {silver['rsi']:.1f}" if silver['rsi'] else "RSI: N/A")
        print(f"Recommendation: {silver['recommendation']}")
    
    # Test Bitcoin
    print("\n₿ BITCOIN:")
    bitcoin = provider.get_bitcoin_analysis()
    if bitcoin:
        print(f"Price: ${bitcoin['price']:,.2f}")
        print(f"Change: {bitcoin['change_percent']:+.2f}%")
        print(f"RSI: {bitcoin['rsi']:.1f}" if bitcoin['rsi'] else "RSI: N/A")
        print(f"Recommendation: {bitcoin['recommendation']}")
    
    # Test VIX
    print("\n📊 VIX:")
    vix = provider.get_vix_analysis()
    if vix:
        print(f"Value: {vix['value']:.2f}")
        print(f"Sentiment: {vix['sentiment']}")
        print(f"Risk Level: {vix['risk_level']}")
    
    print("\n" + "="*50)
    print("✅ TradingView Provider Test Complete!")

