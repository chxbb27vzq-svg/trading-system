"""
Hybrid Market Data Provider
Combines TradingView (for crypto, indices) and yfinance (for commodities)
Best of both worlds!
"""

from tradingview_ta import TA_Handler, Interval
import yfinance as yf
from datetime import datetime
import time

class HybridMarketProvider:
    def __init__(self):
        self.cache = {}
        self.cache_duration = 60  # 60 seconds
        
    def _get_cached_or_fetch(self, cache_key, fetch_func):
        """Get from cache or fetch new data"""
        current_time = time.time()
        
        if cache_key in self.cache:
            cached_data, cached_time = self.cache[cache_key]
            if current_time - cached_time < self.cache_duration:
                return cached_data
        
        data = fetch_func()
        self.cache[cache_key] = (data, current_time)
        return data
    
    def get_gold_analysis(self):
        """Get Gold analysis (yfinance for price + TradingView for indicators)"""
        cache_key = "gold_analysis"
        
        def fetch():
            try:
                # Get price from yfinance (reliable for commodities)
                ticker = yf.Ticker("GC=F")
                hist = ticker.history(period="5d")
                
                if hist.empty:
                    return None
                
                current_price = hist['Close'].iloc[-1]
                prev_price = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
                change_pct = ((current_price - prev_price) / prev_price) * 100
                
                # Try to get technical indicators from TradingView
                rsi = None
                macd = None
                recommendation = "NEUTRAL"
                
                try:
                    handler = TA_Handler(
                        symbol="XAUUSD",
                        screener="forex",
                        exchange="FX_IDC",
                        interval=Interval.INTERVAL_1_DAY
                    )
                    analysis = handler.get_analysis()
                    rsi = analysis.indicators.get('RSI', None)
                    macd = analysis.indicators.get('MACD.macd', None)
                    recommendation = analysis.summary.get('RECOMMENDATION', 'NEUTRAL')
                except:
                    pass  # Use price data only if TradingView fails
                
                return {
                    'symbol': 'GOLD',
                    'price': current_price,
                    'change_percent': change_pct,
                    'high': hist['High'].iloc[-1],
                    'low': hist['Low'].iloc[-1],
                    'rsi': rsi,
                    'macd': macd,
                    'recommendation': recommendation,
                    'source': 'yfinance + TradingView',
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            except Exception as e:
                print(f"❌ Gold Error: {str(e)}")
                return None
        
        return self._get_cached_or_fetch(cache_key, fetch)
    
    def get_silver_analysis(self):
        """Get Silver analysis (yfinance)"""
        cache_key = "silver_analysis"
        
        def fetch():
            try:
                ticker = yf.Ticker("SI=F")
                hist = ticker.history(period="5d")
                
                if hist.empty:
                    return None
                
                current_price = hist['Close'].iloc[-1]
                prev_price = hist['Close'].iloc[-2] if len(hist) > 1 else current_price
                change_pct = ((current_price - prev_price) / prev_price) * 100
                
                # Try TradingView for indicators
                rsi = None
                recommendation = "NEUTRAL"
                
                try:
                    handler = TA_Handler(
                        symbol="XAGUSD",
                        screener="forex",
                        exchange="FX_IDC",
                        interval=Interval.INTERVAL_1_DAY
                    )
                    analysis = handler.get_analysis()
                    rsi = analysis.indicators.get('RSI', None)
                    recommendation = analysis.summary.get('RECOMMENDATION', 'NEUTRAL')
                except:
                    pass
                
                return {
                    'symbol': 'SILVER',
                    'price': current_price,
                    'change_percent': change_pct,
                    'high': hist['High'].iloc[-1],
                    'low': hist['Low'].iloc[-1],
                    'rsi': rsi,
                    'recommendation': recommendation,
                    'source': 'yfinance + TradingView',
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            except Exception as e:
                print(f"❌ Silver Error: {str(e)}")
                return None
        
        return self._get_cached_or_fetch(cache_key, fetch)
    
    def get_bitcoin_analysis(self):
        """Get Bitcoin analysis (TradingView - best for crypto)"""
        cache_key = "bitcoin_analysis"
        
        def fetch():
            try:
                handler = TA_Handler(
                    symbol="BTCUSD",
                    screener="crypto",
                    exchange="BINANCE",
                    interval=Interval.INTERVAL_1_DAY
                )
                analysis = handler.get_analysis()
                
                return {
                    'symbol': 'BITCOIN',
                    'price': analysis.indicators.get('close', 0),
                    'change_percent': analysis.indicators.get('change', 0) / analysis.indicators.get('close', 1) * 100 if analysis.indicators.get('close') else 0,
                    'high': analysis.indicators.get('high', 0),
                    'low': analysis.indicators.get('low', 0),
                    'rsi': analysis.indicators.get('RSI', None),
                    'macd': analysis.indicators.get('MACD.macd', None),
                    'ema_50': analysis.indicators.get('EMA50', None),
                    'recommendation': analysis.summary.get('RECOMMENDATION', 'NEUTRAL'),
                    'buy_signals': analysis.summary.get('BUY', 0),
                    'sell_signals': analysis.summary.get('SELL', 0),
                    'source': 'TradingView',
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            except Exception as e:
                print(f"❌ Bitcoin Error: {str(e)}")
                # Fallback to yfinance
                try:
                    ticker = yf.Ticker("BTC-USD")
                    hist = ticker.history(period="5d")
                    current = hist['Close'].iloc[-1]
                    prev = hist['Close'].iloc[-2]
                    change = ((current - prev) / prev) * 100
                    
                    return {
                        'symbol': 'BITCOIN',
                        'price': current,
                        'change_percent': change,
                        'source': 'yfinance (fallback)',
                        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    }
                except:
                    return None
        
        return self._get_cached_or_fetch(cache_key, fetch)
    
    def get_sp500_analysis(self):
        """Get S&P 500 analysis (TradingView)"""
        cache_key = "sp500_analysis"
        
        def fetch():
            try:
                handler = TA_Handler(
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
                    'source': 'TradingView',
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            except Exception as e:
                print(f"❌ S&P 500 Error: {str(e)}")
                return None
        
        return self._get_cached_or_fetch(cache_key, fetch)
    
    def get_vix_analysis(self):
        """Get VIX analysis (TradingView)"""
        cache_key = "vix_analysis"
        
        def fetch():
            try:
                handler = TA_Handler(
                    symbol="VIX",
                    screener="america",
                    exchange="CBOE",
                    interval=Interval.INTERVAL_1_DAY
                )
                analysis = handler.get_analysis()
                
                vix_value = analysis.indicators.get('close', 0)
                
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
                    'source': 'TradingView',
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            except Exception as e:
                print(f"❌ VIX Error: {str(e)}")
                return None
        
        return self._get_cached_or_fetch(cache_key, fetch)
    
    def get_comprehensive_market_overview(self):
        """Get comprehensive market overview"""
        print("📊 Fetching market data (Hybrid: TradingView + yfinance)...")
        
        return {
            'gold': self.get_gold_analysis(),
            'silver': self.get_silver_analysis(),
            'bitcoin': self.get_bitcoin_analysis(),
            'sp500': self.get_sp500_analysis(),
            'vix': self.get_vix_analysis(),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

if __name__ == "__main__":
    # Test the hybrid provider
    provider = HybridMarketProvider()
    
    print("Testing Hybrid Market Provider...")
    print("="*60)
    
    # Test Gold
    print("\n💰 GOLD (yfinance + TradingView):")
    gold = provider.get_gold_analysis()
    if gold:
        print(f"   Price: ${gold['price']:,.2f}")
        print(f"   Change: {gold['change_percent']:+.2f}%")
        print(f"   RSI: {gold['rsi']:.1f}" if gold.get('rsi') else "   RSI: N/A")
        print(f"   Recommendation: {gold['recommendation']}")
        print(f"   Source: {gold['source']}")
    
    # Test Silver
    print("\n🥈 SILVER (yfinance + TradingView):")
    silver = provider.get_silver_analysis()
    if silver:
        print(f"   Price: ${silver['price']:,.2f}")
        print(f"   Change: {silver['change_percent']:+.2f}%")
        print(f"   RSI: {silver['rsi']:.1f}" if silver.get('rsi') else "   RSI: N/A")
        print(f"   Recommendation: {silver['recommendation']}")
        print(f"   Source: {silver['source']}")
    
    # Test Bitcoin
    print("\n₿ BITCOIN (TradingView):")
    bitcoin = provider.get_bitcoin_analysis()
    if bitcoin:
        print(f"   Price: ${bitcoin['price']:,.2f}")
        print(f"   Change: {bitcoin['change_percent']:+.2f}%")
        print(f"   RSI: {bitcoin['rsi']:.1f}" if bitcoin.get('rsi') else "   RSI: N/A")
        print(f"   Recommendation: {bitcoin['recommendation']}")
        print(f"   Source: {bitcoin['source']}")
    
    # Test VIX
    print("\n📊 VIX (TradingView):")
    vix = provider.get_vix_analysis()
    if vix:
        print(f"   Value: {vix['value']:.2f}")
        print(f"   Sentiment: {vix['sentiment']}")
        print(f"   Risk Level: {vix['risk_level']}")
        print(f"   Source: {vix['source']}")
    
    print("\n" + "="*60)
    print("✅ Hybrid Provider Test Complete!")
    print("\n💡 Best of both worlds:")
    print("   • TradingView: Bitcoin, VIX, S&P 500")
    print("   • yfinance: Gold, Silver (more reliable for commodities)")

