#!/usr/bin/env python3
"""
Multi-Factor Analysis System
Implements lessons learned from S&P 500 and Oil analysis
Requires minimum 3 of 5 factors for signal
"""

from typing import Dict, List, Tuple
from datetime import datetime
import yfinance as yf

class MultiFactorAnalyzer:
    """
    Multi-factor analysis system with context awareness
    Based on lessons learned from failed S&P 500 analysis
    """
    
    def __init__(self):
        self.min_factors_required = 3  # Minimum 3 of 5 for signal
        self.min_risk_reward = 2.0  # Minimum 1:2 risk/reward
    
    def analyze_asset(self, symbol: str, asset_type: str = "stock") -> Dict:
        """
        Comprehensive multi-factor analysis
        
        Args:
            symbol: Asset symbol (e.g., 'SPY', 'GC=F' for gold)
            asset_type: Type of asset (stock, commodity, crypto)
        
        Returns:
            Dict with analysis results
        """
        # Fetch data
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="3mo")
        
        if hist.empty:
            return {"error": "No data available"}
        
        current_price = hist['Close'].iloc[-1]
        
        # Calculate 5 factors
        factors = {}
        
        # Factor 1: RSI (Oversold/Overbought)
        rsi = self._calculate_rsi(hist['Close'])
        factors['rsi'] = {
            "value": rsi,
            "signal": self._evaluate_rsi(rsi),
            "weight": 1.0
        }
        
        # Factor 2: Price vs. High/Low (Context)
        high_1m = hist['High'].tail(20).max()
        low_1m = hist['Low'].tail(20).min()
        dist_from_high = ((current_price - high_1m) / high_1m) * 100
        dist_from_low = ((current_price - low_1m) / low_1m) * 100
        
        factors['price_context'] = {
            "dist_from_high": dist_from_high,
            "dist_from_low": dist_from_low,
            "signal": self._evaluate_price_context(dist_from_high, dist_from_low),
            "weight": 1.0
        }
        
        # Factor 3: Moving Average Trend
        ma20 = hist['Close'].tail(20).mean()
        ma50 = hist['Close'].tail(50).mean()
        
        factors['ma_trend'] = {
            "ma20": ma20,
            "ma50": ma50,
            "price_vs_ma20": ((current_price - ma20) / ma20) * 100,
            "signal": self._evaluate_ma_trend(current_price, ma20, ma50),
            "weight": 1.0
        }
        
        # Factor 4: Volatility
        volatility = hist['Close'].pct_change().std() * 100
        factors['volatility'] = {
            "value": volatility,
            "signal": self._evaluate_volatility(volatility),
            "weight": 0.5  # Lower weight
        }
        
        # Factor 5: Momentum (1-week change)
        momentum = ((current_price - hist['Close'].iloc[-5]) / hist['Close'].iloc[-5]) * 100
        factors['momentum'] = {
            "value": momentum,
            "signal": self._evaluate_momentum(momentum),
            "weight": 0.5  # Lower weight
        }
        
        # Calculate total score
        total_score = sum(f['signal'] * f['weight'] for f in factors.values())
        max_score = sum(f['weight'] for f in factors.values())
        
        # Count positive factors (signal > 0)
        positive_factors = sum(1 for f in factors.values() if f['signal'] > 0)
        
        # Generate recommendation
        recommendation = self._generate_recommendation(
            total_score, max_score, positive_factors, 
            current_price, factors
        )
        
        return {
            "symbol": symbol,
            "current_price": current_price,
            "factors": factors,
            "total_score": total_score,
            "max_score": max_score,
            "normalized_score": total_score / max_score if max_score > 0 else 0,
            "positive_factors": positive_factors,
            "recommendation": recommendation,
            "timestamp": datetime.now().isoformat()
        }
    
    def _calculate_rsi(self, prices, period: int = 14) -> float:
        """Calculate RSI"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        
        return rsi.iloc[-1]
    
    def _evaluate_rsi(self, rsi: float) -> int:
        """
        Evaluate RSI signal
        Returns: -1 (overbought), 0 (neutral), +1 (oversold)
        """
        if rsi < 30:
            return 1  # Oversold - BUY signal
        elif rsi > 70:
            return -1  # Overbought - SELL signal
        else:
            return 0  # Neutral
    
    def _evaluate_price_context(self, dist_from_high: float, dist_from_low: float) -> int:
        """
        Evaluate price context (CRITICAL LESSON from S&P 500 analysis)
        Returns: -1 (near high), 0 (middle), +1 (near low)
        """
        if dist_from_high > -3:  # Within 3% of high
            return -1  # Too high - AVOID
        elif dist_from_low < 5:  # Within 5% of low
            return 1  # Near low - BUY signal
        else:
            return 0  # Middle - Neutral
    
    def _evaluate_ma_trend(self, price: float, ma20: float, ma50: float) -> int:
        """
        Evaluate moving average trend
        Returns: -1 (bearish), 0 (neutral), +1 (bullish)
        """
        if price > ma20 > ma50:
            return 1  # Bullish trend
        elif price < ma20 < ma50:
            return -1  # Bearish trend
        else:
            return 0  # Neutral/Mixed
    
    def _evaluate_volatility(self, volatility: float) -> int:
        """
        Evaluate volatility
        Returns: -1 (too high), 0 (normal), +1 (low)
        """
        if volatility > 3.0:
            return -1  # Too volatile - RISKY
        elif volatility < 1.0:
            return 1  # Low volatility - SAFE
        else:
            return 0  # Normal
    
    def _evaluate_momentum(self, momentum: float) -> int:
        """
        Evaluate momentum
        Returns: -1 (negative), 0 (flat), +1 (positive)
        """
        if momentum > 2:
            return 1  # Strong positive momentum
        elif momentum < -2:
            return -1  # Strong negative momentum
        else:
            return 0  # Flat
    
    def _generate_recommendation(self, total_score: float, max_score: float,
                                 positive_factors: int, current_price: float,
                                 factors: Dict) -> Dict:
        """
        Generate trading recommendation based on multi-factor analysis
        CRITICAL: Requires minimum 3 of 5 factors positive
        """
        normalized_score = total_score / max_score if max_score > 0 else 0
        
        # Check minimum factors requirement
        if positive_factors < self.min_factors_required:
            return {
                "action": "WAIT",
                "reason": f"Only {positive_factors}/5 factors positive (need {self.min_factors_required})",
                "confidence": 0.0,
                "position_size": 0.0,
                "entry": None,
                "target": None,
                "stop": None
            }
        
        # Calculate entry, target, stop based on factors
        rsi_value = factors['rsi']['value']
        dist_from_high = factors['price_context']['dist_from_high']
        
        # Determine action
        if normalized_score > 0.4 and positive_factors >= 3:
            action = "BUY"
            confidence = min(0.7 + (positive_factors - 3) * 0.1, 0.9)
            
            # Position sizing based on confidence and factors
            if positive_factors >= 4:
                position_size = 0.15  # 15%
            elif positive_factors == 3:
                position_size = 0.10  # 10%
            else:
                position_size = 0.05  # 5%
            
            # Calculate entry, target, stop
            entry = current_price
            target = current_price * 1.05  # +5% target
            stop = current_price * 0.97  # -3% stop
            
            # Adjust based on context
            if dist_from_high > -10:  # Near high
                position_size *= 0.5  # Reduce size
                confidence *= 0.8  # Reduce confidence
        
        elif normalized_score < -0.4 and positive_factors <= 1:
            action = "AVOID"
            confidence = 0.7
            position_size = 0.0
            entry = None
            target = None
            stop = None
        
        else:
            action = "WAIT"
            confidence = 0.5
            position_size = 0.0
            entry = None
            target = None
            stop = None
        
        # Calculate risk/reward
        risk_reward = None
        if entry and target and stop:
            risk = entry - stop
            reward = target - entry
            risk_reward = reward / risk if risk > 0 else 0
            
            # Check minimum risk/reward
            if risk_reward < self.min_risk_reward:
                action = "WAIT"
                reason = f"Risk/Reward too low ({risk_reward:.2f} < {self.min_risk_reward})"
                confidence = 0.0
                position_size = 0.0
        
        return {
            "action": action,
            "confidence": confidence,
            "position_size": position_size,
            "entry": entry,
            "target": target,
            "stop": stop,
            "risk_reward": risk_reward,
            "positive_factors": positive_factors,
            "normalized_score": normalized_score
        }
    
    def generate_report(self, analysis: Dict) -> str:
        """Generate human-readable analysis report"""
        report = "="*70 + "\n"
        report += f"MULTI-FACTOR ANALYSIS: {analysis['symbol']}\n"
        report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}\n"
        report += "="*70 + "\n\n"
        
        report += f"Current Price: ${analysis['current_price']:.2f}\n\n"
        
        report += "FACTOR ANALYSIS:\n"
        report += "-"*70 + "\n"
        
        factors = analysis['factors']
        
        # RSI
        rsi = factors['rsi']
        signal_emoji = "✅" if rsi['signal'] > 0 else "❌" if rsi['signal'] < 0 else "⚪"
        report += f"{signal_emoji} RSI: {rsi['value']:.1f} "
        if rsi['signal'] > 0:
            report += "(Oversold - BUY)\n"
        elif rsi['signal'] < 0:
            report += "(Overbought - SELL)\n"
        else:
            report += "(Neutral)\n"
        
        # Price Context
        context = factors['price_context']
        signal_emoji = "✅" if context['signal'] > 0 else "❌" if context['signal'] < 0 else "⚪"
        report += f"{signal_emoji} Price Context: {context['dist_from_high']:.1f}% from high, "
        report += f"{context['dist_from_low']:.1f}% from low "
        if context['signal'] > 0:
            report += "(Near low - BUY)\n"
        elif context['signal'] < 0:
            report += "(Near high - AVOID)\n"
        else:
            report += "(Middle)\n"
        
        # MA Trend
        ma = factors['ma_trend']
        signal_emoji = "✅" if ma['signal'] > 0 else "❌" if ma['signal'] < 0 else "⚪"
        report += f"{signal_emoji} MA Trend: Price {ma['price_vs_ma20']:.1f}% vs MA(20) "
        if ma['signal'] > 0:
            report += "(Bullish)\n"
        elif ma['signal'] < 0:
            report += "(Bearish)\n"
        else:
            report += "(Neutral)\n"
        
        # Volatility
        vol = factors['volatility']
        signal_emoji = "✅" if vol['signal'] > 0 else "❌" if vol['signal'] < 0 else "⚪"
        report += f"{signal_emoji} Volatility: {vol['value']:.2f}% "
        if vol['signal'] > 0:
            report += "(Low - Safe)\n"
        elif vol['signal'] < 0:
            report += "(High - Risky)\n"
        else:
            report += "(Normal)\n"
        
        # Momentum
        mom = factors['momentum']
        signal_emoji = "✅" if mom['signal'] > 0 else "❌" if mom['signal'] < 0 else "⚪"
        report += f"{signal_emoji} Momentum: {mom['value']:.1f}% (1-week) "
        if mom['signal'] > 0:
            report += "(Positive)\n"
        elif mom['signal'] < 0:
            report += "(Negative)\n"
        else:
            report += "(Flat)\n"
        
        report += "\n"
        report += f"SCORE: {analysis['positive_factors']}/5 factors positive\n"
        report += f"Normalized Score: {analysis['normalized_score']:.2f}\n\n"
        
        # Recommendation
        rec = analysis['recommendation']
        report += "RECOMMENDATION:\n"
        report += "-"*70 + "\n"
        report += f"Action: {rec['action']}\n"
        report += f"Confidence: {rec['confidence']*100:.0f}%\n"
        
        if rec['action'] == "BUY":
            report += f"Position Size: {rec['position_size']*100:.0f}%\n"
            report += f"Entry: ${rec['entry']:.2f}\n"
            report += f"Target: ${rec['target']:.2f}\n"
            report += f"Stop: ${rec['stop']:.2f}\n"
            report += f"Risk/Reward: 1:{rec['risk_reward']:.2f}\n"
        elif rec['action'] == "WAIT":
            report += f"Reason: {rec.get('reason', 'Insufficient factors')}\n"
        
        report += "="*70 + "\n"
        
        return report


if __name__ == "__main__":
    # Example usage
    analyzer = MultiFactorAnalyzer()
    
    print("=== MULTI-FACTOR ANALYZER - DEMO ===\n")
    
    # Analyze S&P 500
    print("Analyzing S&P 500 (SPY)...\n")
    analysis = analyzer.analyze_asset("SPY", "stock")
    print(analyzer.generate_report(analysis))
    
    # Analyze Gold
    print("\nAnalyzing Gold (GC=F)...\n")
    analysis = analyzer.analyze_asset("GC=F", "commodity")
    print(analyzer.generate_report(analysis))
    
    print("\n✅ MULTI-FACTOR ANALYZER OPERATIONAL")

