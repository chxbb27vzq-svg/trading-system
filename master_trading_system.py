#!/usr/bin/env python3
"""
Master Trading System - Lessons Learned Integration
Combines all modules with lessons from Oil Sanctions, S&P 500, and historical analysis
"""

import sys
sys.path.append('/home/ubuntu/trading_agents')

from geopolitical.geopolitical_risk_tracker import GeopoliticalRiskTracker
from analysis.multi_factor_analyzer import MultiFactorAnalyzer
from oil.oil_tracker import OilTracker
from performance.enhanced_performance_tracker import EnhancedPerformanceTracker
from alerts.enhanced_alert_system import EnhancedAlertSystem
from contrarian.enhanced_contrarian_dashboard import EnhancedContrarianDashboard
from monte_carlo.enhanced_portfolio_simulator import EnhancedPortfolioSimulator
from lessons_learned.weekly_lessons_report import WeeklyLessonsReport

from datetime import datetime
from typing import Dict, List
import json

class MasterTradingSystem:
    """
    Master Trading System integrating all lessons learned
    """
    
    def __init__(self):
        print("Initializing Master Trading System...")
        
        # Core modules
        self.geopolitical = GeopoliticalRiskTracker()
        self.multi_factor = MultiFactorAnalyzer()
        self.oil_tracker = OilTracker()
        self.performance = EnhancedPerformanceTracker()
        self.alerts = EnhancedAlertSystem()
        self.contrarian = EnhancedContrarianDashboard()
        self.monte_carlo = EnhancedPortfolioSimulator()
        self.lessons = WeeklyLessonsReport()
        
        # Lessons learned database
        self.lessons_db = {
            "oil_sanctions": {
                "lesson": "Umgehungen sind teuer (+$20-35/barrel), Preis steigt trotzdem",
                "confidence": 0.80,
                "historical_evidence": ["Iran 2018", "Venezuela 2019", "Russia 2022"]
            },
            "sp500_near_high": {
                "lesson": "Nicht kaufen bei <3% vom Hoch, auch mit Put/Call Signal",
                "confidence": 0.75,
                "historical_evidence": ["Oct 2025 S&P 500"]
            },
            "multi_factor_required": {
                "lesson": "Minimum 3 von 5 Faktoren erforderlich für Signal",
                "confidence": 0.85,
                "historical_evidence": ["S&P 500 Oct 2025", "Gold Oct 2025"]
            },
            "geopolitical_critical": {
                "lesson": "Geopolitik ist nicht optional - größter Markt-Mover",
                "confidence": 0.90,
                "historical_evidence": ["Oil Sanctions Oct 2025"]
            }
        }
        
        print("✅ Master Trading System initialized\n")
    
    def run_full_analysis(self, assets: List[str] = None) -> Dict:
        """
        Run comprehensive analysis across all systems
        
        Args:
            assets: List of assets to analyze (default: ['SPY', 'GC=F', 'BZ=F', 'BTC-USD'])
        
        Returns:
            Dict with comprehensive analysis
        """
        if assets is None:
            assets = ['SPY', 'GC=F', 'BZ=F', 'BTC-USD']
        
        print("="*70)
        print("MASTER TRADING SYSTEM - FULL ANALYSIS")
        print(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}")
        print("="*70 + "\n")
        
        results = {
            "timestamp": datetime.now().isoformat(),
            "geopolitical_risks": {},
            "asset_analysis": {},
            "contrarian_signals": {},
            "portfolio_optimization": {},
            "active_alerts": {},
            "recommendations": {}
        }
        
        # 1. Geopolitical Risk Assessment
        print("1. GEOPOLITICAL RISK ASSESSMENT")
        print("-"*70)
        risks = self.geopolitical.get_active_risks(30)
        results["geopolitical_risks"] = {
            "active_risks": len(risks),
            "critical": len([r for r in risks if r["severity"] == "CRITICAL"]),
            "high": len([r for r in risks if r["severity"] == "HIGH"]),
            "risks": risks
        }
        print(f"Active Risks: {len(risks)}")
        print(f"Critical: {results['geopolitical_risks']['critical']}")
        print(f"High: {results['geopolitical_risks']['high']}\n")
        
        # 2. Multi-Factor Asset Analysis
        print("2. MULTI-FACTOR ASSET ANALYSIS")
        print("-"*70)
        for asset in assets:
            print(f"Analyzing {asset}...")
            analysis = self.multi_factor.analyze_asset(asset)
            results["asset_analysis"][asset] = analysis
            
            rec = analysis['recommendation']
            print(f"  {rec['action']} - {rec['positive_factors']}/5 factors")
            print(f"  Confidence: {rec['confidence']*100:.0f}%\n")
        
        # 3. Contrarian Signals
        print("3. CONTRARIAN SIGNALS")
        print("-"*70)
        contrarian_data = self.contrarian.get_all_indicators()
        signals = self.contrarian.generate_signals(contrarian_data)
        results["contrarian_signals"] = signals
        
        strong_signals = [s for s in signals if s['confidence'] >= 0.65]
        print(f"Strong Contrarian Signals: {len(strong_signals)}\n")
        for signal in strong_signals:
            print(f"  {signal['indicator']}: {signal['signal']}")
            print(f"  Confidence: {signal['confidence']*100:.0f}%\n")
        
        # 4. Active Alerts
        print("4. ACTIVE ALERTS")
        print("-"*70)
        alert_summary = self.alerts.get_alert_summary()
        results["active_alerts"] = alert_summary
        print(f"Total Alerts: {alert_summary['total_alerts']}")
        print(f"Critical: {alert_summary['critical']}\n")
        
        # 5. Portfolio Optimization
        print("5. PORTFOLIO OPTIMIZATION")
        print("-"*70)
        
        # Build portfolio based on recommendations
        portfolio = {}
        for asset, analysis in results["asset_analysis"].items():
            rec = analysis['recommendation']
            if rec['action'] == "BUY" and rec['position_size'] > 0:
                portfolio[asset] = rec['position_size']
        
        if portfolio:
            # Normalize to 100%
            total = sum(portfolio.values())
            portfolio = {k: v/total for k, v in portfolio.items()}
            
            # Run Monte Carlo
            print("Running Monte Carlo simulation...")
            sim_result = self.monte_carlo.run_simulation(
                list(portfolio.keys()),
                list(portfolio.values()),
                iterations=10000
            )
            results["portfolio_optimization"] = sim_result
            
            print(f"Expected Return: {sim_result['expected_return']*100:.2f}%")
            print(f"Sharpe Ratio: {sim_result['sharpe_ratio']:.3f}")
            print(f"VaR(95%): {sim_result['var_95']*100:.2f}%\n")
        else:
            print("No BUY recommendations - Portfolio: 100% Cash\n")
            results["portfolio_optimization"] = {"cash": 1.0}
        
        # 6. Generate Master Recommendations
        print("6. MASTER RECOMMENDATIONS")
        print("-"*70)
        recommendations = self._generate_master_recommendations(results)
        results["recommendations"] = recommendations
        
        for rec in recommendations:
            print(f"• {rec['asset']}: {rec['action']}")
            print(f"  Reason: {rec['reason']}")
            print(f"  Confidence: {rec['confidence']*100:.0f}%\n")
        
        print("="*70)
        print("✅ FULL ANALYSIS COMPLETE\n")
        
        return results
    
    def _generate_master_recommendations(self, results: Dict) -> List[Dict]:
        """
        Generate master recommendations considering all factors
        """
        recommendations = []
        
        # Check geopolitical risks
        geo_risks = results["geopolitical_risks"]
        high_risk_environment = geo_risks["critical"] > 0 or geo_risks["high"] > 2
        
        # Analyze each asset
        for asset, analysis in results["asset_analysis"].items():
            rec = analysis['recommendation']
            
            # Apply lessons learned
            if rec['action'] == "BUY":
                # Lesson 1: Check multi-factor requirement
                if rec['positive_factors'] < 3:
                    recommendations.append({
                        "asset": asset,
                        "action": "WAIT",
                        "reason": f"Only {rec['positive_factors']}/5 factors (need 3+)",
                        "confidence": 0.0,
                        "lesson_applied": "multi_factor_required"
                    })
                    continue
                
                # Lesson 2: Check if near high
                context = analysis['factors']['price_context']
                if context['dist_from_high'] > -3:
                    recommendations.append({
                        "asset": asset,
                        "action": "WAIT",
                        "reason": f"Too close to high ({context['dist_from_high']:.1f}%)",
                        "confidence": 0.0,
                        "lesson_applied": "sp500_near_high"
                    })
                    continue
                
                # Lesson 3: Check risk/reward
                if rec['risk_reward'] and rec['risk_reward'] < 2.0:
                    recommendations.append({
                        "asset": asset,
                        "action": "WAIT",
                        "reason": f"Risk/Reward too low ({rec['risk_reward']:.2f})",
                        "confidence": 0.0,
                        "lesson_applied": "risk_reward_minimum"
                    })
                    continue
                
                # Lesson 4: Adjust for geopolitical risks
                confidence = rec['confidence']
                if high_risk_environment:
                    confidence *= 0.8  # Reduce confidence in high-risk environment
                
                recommendations.append({
                    "asset": asset,
                    "action": "BUY",
                    "reason": f"{rec['positive_factors']}/5 factors, R/R {rec['risk_reward']:.2f}",
                    "confidence": confidence,
                    "position_size": rec['position_size'],
                    "entry": rec['entry'],
                    "target": rec['target'],
                    "stop": rec['stop']
                })
            
            elif rec['action'] == "WAIT":
                recommendations.append({
                    "asset": asset,
                    "action": "WAIT",
                    "reason": rec.get('reason', 'Insufficient factors'),
                    "confidence": rec['confidence']
                })
        
        # Add contrarian signals
        contrarian_signals = results["contrarian_signals"]
        strong_signals = [s for s in contrarian_signals if s['confidence'] >= 0.70]
        
        for signal in strong_signals:
            recommendations.append({
                "asset": signal['indicator'],
                "action": signal['signal'],
                "reason": f"Contrarian: {signal['reason']}",
                "confidence": signal['confidence'],
                "source": "contrarian"
            })
        
        return recommendations
    
    def generate_master_report(self) -> str:
        """Generate comprehensive master report"""
        results = self.run_full_analysis()
        
        report = "="*70 + "\n"
        report += "MASTER TRADING SYSTEM REPORT\n"
        report += f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M UTC')}\n"
        report += "="*70 + "\n\n"
        
        # Geopolitical Risks
        report += "🌍 GEOPOLITICAL RISKS\n"
        report += "-"*70 + "\n"
        geo = results["geopolitical_risks"]
        report += f"Active Risks: {geo['active_risks']}\n"
        report += f"Critical: {geo['critical']} | High: {geo['high']}\n\n"
        
        # Asset Analysis Summary
        report += "📊 ASSET ANALYSIS\n"
        report += "-"*70 + "\n"
        for asset, analysis in results["asset_analysis"].items():
            rec = analysis['recommendation']
            report += f"{asset}: {rec['action']} ({rec['positive_factors']}/5 factors)\n"
        report += "\n"
        
        # Master Recommendations
        report += "🎯 MASTER RECOMMENDATIONS\n"
        report += "-"*70 + "\n"
        for rec in results["recommendations"]:
            report += f"• {rec['asset']}: {rec['action']}\n"
            report += f"  {rec['reason']}\n"
            report += f"  Confidence: {rec['confidence']*100:.0f}%\n\n"
        
        # Portfolio
        report += "💼 RECOMMENDED PORTFOLIO\n"
        report += "-"*70 + "\n"
        buy_recs = [r for r in results["recommendations"] if r['action'] == "BUY"]
        if buy_recs:
            for rec in buy_recs:
                if 'position_size' in rec:
                    report += f"{rec['asset']}: {rec['position_size']*100:.0f}%\n"
            
            cash = 100 - sum(r.get('position_size', 0)*100 for r in buy_recs)
            report += f"Cash: {cash:.0f}%\n"
        else:
            report += "Cash: 100% (No positions recommended)\n"
        
        report += "\n" + "="*70 + "\n"
        
        return report


if __name__ == "__main__":
    # Initialize system
    system = MasterTradingSystem()
    
    # Run full analysis
    print(system.generate_master_report())
    
    print("\n✅ MASTER TRADING SYSTEM OPERATIONAL")
    print("\nLESSONS LEARNED INTEGRATED:")
    for lesson_name, lesson_data in system.lessons_db.items():
        print(f"• {lesson_data['lesson']}")
        print(f"  Confidence: {lesson_data['confidence']*100:.0f}%")
        print(f"  Evidence: {', '.join(lesson_data['historical_evidence'])}\n")

