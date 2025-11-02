"""
Oil Tactical Trading Module
Small capital (€300-500) with high leverage (10-15x)
Focus: Geopolitical spikes and OPEC+ events
"""

from datetime import datetime
import yfinance as yf

class OilTacticalTrader:
    def __init__(self):
        self.symbols = {
            'brent': 'BZ=F',  # Brent Crude Futures
            'wti': 'CL=F'      # WTI Crude Futures
        }
        
        # Tactical trading parameters
        self.capital = 400  # €400 (4% of €10K)
        self.leverage = 12  # 12x leverage
        self.exposure = self.capital * self.leverage  # €4,800
        
        # Risk management
        self.stop_loss_pct = 5.0  # -5% stop loss
        self.take_profit_pct = 15.0  # +15% take profit
        self.max_loss = self.capital * (self.stop_loss_pct / 100)  # €20 max loss
        self.target_profit = self.capital * (self.take_profit_pct / 100)  # €60 target
        
        # Geopolitical triggers
        self.bullish_triggers = [
            'iran war', 'saudi attack', 'opec cut',
            'middle east conflict', 'strait hormuz',
            'russia embargo', 'venezuela crisis'
        ]
        
        self.bearish_triggers = [
            'recession', 'china slowdown', 'demand collapse',
            'opec increase', 'shale boom', 'ev adoption'
        ]
    
    def get_oil_prices(self):
        """Get current oil prices"""
        try:
            brent = yf.Ticker(self.symbols['brent'])
            wti = yf.Ticker(self.symbols['wti'])
            
            brent_hist = brent.history(period='5d')
            wti_hist = wti.history(period='5d')
            
            if len(brent_hist) == 0 or len(wti_hist) == 0:
                return None
            
            brent_price = brent_hist['Close'].iloc[-1]
            brent_prev = brent_hist['Close'].iloc[-2] if len(brent_hist) > 1 else brent_price
            brent_change = ((brent_price - brent_prev) / brent_prev) * 100
            
            wti_price = wti_hist['Close'].iloc[-1]
            wti_prev = wti_hist['Close'].iloc[-2] if len(wti_hist) > 1 else wti_price
            wti_change = ((wti_price - wti_prev) / wti_prev) * 100
            
            return {
                'brent': {
                    'price': brent_price,
                    'change': brent_change,
                    'high': brent_hist['High'].iloc[-1],
                    'low': brent_hist['Low'].iloc[-1]
                },
                'wti': {
                    'price': wti_price,
                    'change': wti_change,
                    'high': wti_hist['High'].iloc[-1],
                    'low': wti_hist['Low'].iloc[-1]
                },
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception as e:
            print(f"Error fetching oil prices: {e}")
            return None
    
    def analyze_geopolitical_impact(self, geopolitics_data):
        """Analyze geopolitical impact on oil"""
        if not geopolitics_data:
            return {'impact': 'NEUTRAL', 'score': 0}
        
        # Extract keywords from geopolitics analysis
        risk_score = geopolitics_data.get('overall_risk', 5)
        
        # High geopolitical risk = bullish for oil (supply concerns)
        if risk_score >= 8:
            return {
                'impact': 'VERY BULLISH',
                'score': 8,
                'reason': 'Critical geopolitical tensions → Supply risk'
            }
        elif risk_score >= 7:
            return {
                'impact': 'BULLISH',
                'score': 6,
                'reason': 'High geopolitical risk → Moderate supply concerns'
            }
        elif risk_score >= 5:
            return {
                'impact': 'NEUTRAL',
                'score': 3,
                'reason': 'Medium risk → Balanced outlook'
            }
        else:
            return {
                'impact': 'BEARISH',
                'score': -2,
                'reason': 'Low geopolitical risk → Demand concerns dominate'
            }
    
    def calculate_technical_score(self, oil_data):
        """Calculate technical score"""
        if not oil_data:
            return 0
        
        brent = oil_data['brent']
        score = 0
        
        # Price momentum
        if brent['change'] > 2:
            score += 3
        elif brent['change'] > 0:
            score += 1
        elif brent['change'] < -2:
            score -= 3
        else:
            score -= 1
        
        # Volatility (high-low range)
        volatility = ((brent['high'] - brent['low']) / brent['price']) * 100
        if volatility > 3:
            score += 2  # High volatility = opportunity
        
        return score
    
    def get_trading_recommendation(self, oil_data, geopolitics_data=None):
        """Get tactical trading recommendation"""
        if not oil_data:
            return {
                'action': 'WAIT',
                'confidence': 0,
                'reason': 'No data available'
            }
        
        # Calculate scores
        geo_analysis = self.analyze_geopolitical_impact(geopolitics_data)
        tech_score = self.calculate_technical_score(oil_data)
        
        # Combined score
        total_score = geo_analysis['score'] + tech_score
        
        # Trading decision
        if total_score >= 8:
            action = 'STRONG BUY'
            confidence = 9
        elif total_score >= 5:
            action = 'BUY'
            confidence = 7
        elif total_score >= 2:
            action = 'HOLD'
            confidence = 5
        elif total_score >= -2:
            action = 'WAIT'
            confidence = 3
        else:
            action = 'AVOID'
            confidence = 2
        
        # Calculate entry/exit levels
        brent_price = oil_data['brent']['price']
        entry_price = brent_price
        stop_loss = entry_price * (1 - self.stop_loss_pct / 100)
        take_profit = entry_price * (1 + self.take_profit_pct / 100)
        
        return {
            'action': action,
            'confidence': confidence,
            'total_score': total_score,
            'geopolitical': geo_analysis,
            'technical_score': tech_score,
            'entry_price': entry_price,
            'stop_loss': stop_loss,
            'take_profit': take_profit,
            'risk_reward': self.take_profit_pct / self.stop_loss_pct,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def get_position_details(self, oil_data):
        """Get current position details"""
        if not oil_data:
            return None
        
        brent_price = oil_data['brent']['price']
        
        # Position sizing
        contracts = self.exposure / brent_price
        
        # Risk calculation
        stop_loss_price = brent_price * (1 - self.stop_loss_pct / 100)
        take_profit_price = brent_price * (1 + self.take_profit_pct / 100)
        
        potential_loss = (brent_price - stop_loss_price) * contracts
        potential_profit = (take_profit_price - brent_price) * contracts
        
        return {
            'capital': self.capital,
            'leverage': self.leverage,
            'exposure': self.exposure,
            'contracts': contracts,
            'entry_price': brent_price,
            'stop_loss': stop_loss_price,
            'take_profit': take_profit_price,
            'potential_loss': potential_loss,
            'potential_profit': potential_profit,
            'risk_reward': potential_profit / potential_loss if potential_loss > 0 else 0,
            'max_loss_eur': self.max_loss,
            'target_profit_eur': self.target_profit
        }
    
    def get_comprehensive_analysis(self, geopolitics_data=None):
        """Get comprehensive oil analysis"""
        print("🛢️ Analyzing Oil Markets...")
        
        # Get prices
        oil_data = self.get_oil_prices()
        
        if not oil_data:
            return {
                'status': 'error',
                'message': 'Could not fetch oil data'
            }
        
        # Get recommendation
        recommendation = self.get_trading_recommendation(oil_data, geopolitics_data)
        
        # Get position details
        position = self.get_position_details(oil_data)
        
        return {
            'status': 'success',
            'prices': oil_data,
            'recommendation': recommendation,
            'position': position,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def format_for_telegram(self, analysis):
        """Format analysis for Telegram"""
        if analysis.get('status') != 'success':
            return "❌ Öl-Daten nicht verfügbar"
        
        prices = analysis['prices']
        rec = analysis['recommendation']
        pos = analysis['position']
        
        msg = "🛢️ *ÖL TACTICAL ANALYSIS*\n\n"
        
        # Prices
        msg += f"📈 *Brent:* ${prices['brent']['price']:.2f}\n"
        msg += f"   24h: {prices['brent']['change']:+.2f}%\n"
        msg += f"   Range: ${prices['brent']['low']:.2f} - ${prices['brent']['high']:.2f}\n\n"
        
        msg += f"📈 *WTI:* ${prices['wti']['price']:.2f}\n"
        msg += f"   24h: {prices['wti']['change']:+.2f}%\n\n"
        
        # Geopolitical Impact
        geo = rec['geopolitical']
        msg += f"🌍 *Geopolitik-Impact:* {geo['impact']}\n"
        msg += f"   Score: {geo['score']}/10\n"
        if 'reason' in geo:
            msg += f"   Grund: {geo['reason']}\n"
        msg += "\n"
        
        # Recommendation
        action_emoji = {
            'STRONG BUY': '🟢🟢',
            'BUY': '🟢',
            'HOLD': '🟡',
            'WAIT': '⚪',
            'AVOID': '🔴'
        }
        
        msg += f"{action_emoji.get(rec['action'], '⚪')} *EMPFEHLUNG:* {rec['action']}\n"
        msg += f"   Confidence: {rec['confidence']}/10\n"
        msg += f"   Total Score: {rec['total_score']}\n\n"
        
        # Position Details
        msg += f"💼 *TACTICAL POSITION:*\n"
        msg += f"   Kapital: €{pos['capital']}\n"
        msg += f"   Leverage: {pos['leverage']}x\n"
        msg += f"   Exposure: €{pos['exposure']:,.0f}\n\n"
        
        msg += f"🎯 *Entry:* ${pos['entry_price']:.2f}\n"
        msg += f"🛑 *Stop Loss:* ${pos['stop_loss']:.2f} (-{self.stop_loss_pct}%)\n"
        msg += f"✅ *Take Profit:* ${pos['take_profit']:.2f} (+{self.take_profit_pct}%)\n\n"
        
        msg += f"💰 *P&L Potential:*\n"
        msg += f"   Max Loss: €{pos['max_loss_eur']:.0f}\n"
        msg += f"   Target Profit: €{pos['target_profit_eur']:.0f}\n"
        msg += f"   R/R: 1:{pos['risk_reward']:.1f}\n\n"
        
        # Risk Warning
        msg += "⚠️ *RISIKO:*\n"
        msg += f"   Hoher Hebel ({pos['leverage']}x)\n"
        msg += "   Nur für taktisches Trading\n"
        msg += "   Max. €20 Verlust pro Trade"
        
        return msg

if __name__ == "__main__":
    # Test the oil trader
    trader = OilTacticalTrader()
    
    print("Testing Oil Tactical Trader...")
    print("="*60)
    
    # Get analysis
    analysis = trader.get_comprehensive_analysis()
    
    if analysis['status'] == 'success':
        print("\n" + trader.format_for_telegram(analysis))
    else:
        print(f"Error: {analysis['message']}")
    
    print("\n" + "="*60)
    print("✅ Oil Tactical Trader Ready!")

