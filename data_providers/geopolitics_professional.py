"""
Professional Geopolitics Module V2.0
Combines YouTube expert analysis + International news aggregation
NO Wikipedia, NO propaganda - only facts and expert insights
"""

from data_providers.youtube_geopolitics_provider import YouTubeGeopoliticsProvider
from data_providers.news_aggregator import NewsAggregator
from datetime import datetime

class ProfessionalGeopoliticsAnalyzer:
    def __init__(self):
        self.youtube = YouTubeGeopoliticsProvider()
        self.news = NewsAggregator()
        
    def get_trading_impact(self, youtube_analysis, news_summary):
        """Calculate trading impact from combined analysis"""
        
        # Default neutral
        gold_impact = 0
        bitcoin_impact = 0
        equities_impact = 0
        
        # YouTube sentiment (weighted 60%)
        if youtube_analysis and 'overall_risk' in youtube_analysis:
            risk = youtube_analysis['overall_risk']
            
            # High risk = Gold up, Equities down
            gold_impact += (risk - 5) * 1.2  # -6 to +6
            equities_impact -= (risk - 5) * 1.5  # Inverse
            bitcoin_impact += (risk - 5) * 0.5  # Moderate correlation
        
        # News facts (weighted 40%)
        if news_summary and 'top_facts' in news_summary:
            for fact in news_summary['top_facts'][:5]:
                keyword = fact['keyword']
                confidence = fact['confidence'] / 10  # 0-1 scale
                
                if keyword in ['nuclear', 'war', 'escalation', 'crisis']:
                    gold_impact += 2 * confidence
                    equities_impact -= 3 * confidence
                    bitcoin_impact += 0.5 * confidence
                
                elif keyword in ['gold']:
                    gold_impact += 1.5 * confidence
                
                elif keyword in ['fed', 'interest rate', 'inflation']:
                    gold_impact += 1 * confidence
                    equities_impact -= 0.5 * confidence
                
                elif keyword in ['recession']:
                    equities_impact -= 2 * confidence
                    gold_impact += 0.5 * confidence
        
        # Normalize to percentage ranges
        def to_range(impact):
            if impact > 5:
                return "+5-10%"
            elif impact > 3:
                return "+3-5%"
            elif impact > 1:
                return "+1-3%"
            elif impact > -1:
                return "NEUTRAL"
            elif impact > -3:
                return "-1-3%"
            elif impact > -5:
                return "-3-5%"
            else:
                return "-5-10%"
        
        return {
            'gold': to_range(gold_impact),
            'bitcoin': to_range(bitcoin_impact),
            'equities': to_range(equities_impact),
            'gold_score': round(gold_impact, 1),
            'bitcoin_score': round(bitcoin_impact, 1),
            'equities_score': round(equities_impact, 1)
        }
    
    def get_portfolio_recommendation(self, trading_impact, current_portfolio):
        """Get portfolio recommendation based on analysis"""
        
        gold_score = trading_impact['gold_score']
        
        current_gold = current_portfolio.get('gold', 18)
        current_bitcoin = current_portfolio.get('bitcoin', 8)
        current_cash = current_portfolio.get('cash', 74)
        
        # Recommendations
        if gold_score > 3:
            # High risk - increase gold
            rec_gold = min(25, current_gold + 5)
            rec_bitcoin = current_bitcoin
            rec_cash = 100 - rec_gold - rec_bitcoin
            action = "INCREASE Gold to 25%"
        
        elif gold_score > 1:
            # Moderate risk - maintain
            rec_gold = current_gold
            rec_bitcoin = current_bitcoin
            rec_cash = current_cash
            action = "MAINTAIN current allocation"
        
        else:
            # Low risk - can reduce defensive
            rec_gold = max(15, current_gold - 3)
            rec_bitcoin = current_bitcoin
            rec_cash = 100 - rec_gold - rec_bitcoin
            action = "Can reduce Gold slightly"
        
        return {
            'action': action,
            'recommended': {
                'gold': rec_gold,
                'bitcoin': rec_bitcoin,
                'cash': rec_cash
            },
            'current': current_portfolio,
            'reasoning': f"Geopolitical risk score: {gold_score:.1f}/10"
        }
    
    def get_comprehensive_analysis(self, current_portfolio=None):
        """Get complete geopolitical analysis for trading"""
        
        if current_portfolio is None:
            current_portfolio = {'gold': 18, 'bitcoin': 8, 'cash': 74}
        
        print("="*70)
        print("🌍 PROFESSIONAL GEOPOLITICS ANALYSIS V2.0")
        print("="*70)
        print()
        
        # Phase 1: YouTube Expert Analysis
        print("📺 PHASE 1: YouTube Expert Analysis")
        print("-" * 70)
        youtube_analysis = self.youtube.get_comprehensive_analysis()
        print("✅ YouTube analysis complete")
        print()
        
        # Phase 2: International News Aggregation
        print("📰 PHASE 2: International News Aggregation")
        print("-" * 70)
        news_summary = self.news.get_geopolitical_summary(hours=48)
        print("✅ News aggregation complete")
        print()
        
        # Phase 3: Trading Impact Calculation
        print("💰 PHASE 3: Trading Impact Analysis")
        print("-" * 70)
        trading_impact = self.get_trading_impact(youtube_analysis, news_summary)
        print("✅ Trading impact calculated")
        print()
        
        # Phase 4: Portfolio Recommendation
        print("📊 PHASE 4: Portfolio Recommendation")
        print("-" * 70)
        portfolio_rec = self.get_portfolio_recommendation(trading_impact, current_portfolio)
        print("✅ Portfolio recommendation ready")
        print()
        
        print("="*70)
        print("✅ ANALYSIS COMPLETE")
        print("="*70)
        
        return {
            'youtube_analysis': youtube_analysis,
            'news_summary': news_summary,
            'trading_impact': trading_impact,
            'portfolio_recommendation': portfolio_rec,
            'overall_risk': youtube_analysis.get('overall_risk', 5),
            'risk_level': youtube_analysis.get('risk_level', 'MEDIUM'),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def format_for_telegram(self, analysis):
        """Format analysis for Telegram bot"""
        
        msg = "🌍 *GEOPOLITISCHE LAGE (Professional)*\n\n"
        
        # Overall Risk
        risk = analysis.get('overall_risk', 5)
        risk_level = analysis.get('risk_level', 'MEDIUM')
        msg += f"📊 *Gesamt-Risiko:* {risk}/10\n"
        msg += f"🎯 *Level:* {risk_level}\n"
        msg += f"🛡️ *Safe Haven Demand:* {'HIGH' if risk > 7 else 'MEDIUM' if risk > 5 else 'LOW'}\n\n"
        
        # YouTube Experts
        youtube = analysis.get('youtube_analysis', {})
        channels = youtube.get('channels', {})
        
        msg += "🎓 *EXPERT ANALYSIS (YouTube):*\n"
        
        # Show all channels (even if no video data yet)
        channel_list = [
            'glenn_diesen', 'alexander_mercouris', 'luke_gromen',
            'raoul_pal', 'jeff_snider', 'lyn_alden',
            'steven_van_metre', 'george_gammon', 'adam_taggart'
        ]
        
        success_count = 0
        for channel_key in channel_list:
            data = channels.get(channel_key, {})
            if data.get('status') == 'success':
                success_count += 1
                msg += f"📺 {data['channel']} - Risk: {data.get('sentiment', {}).get('overall_risk', 'N/A')}/10\n"
        
        # If no successful analyses, show configured channels
        if success_count == 0:
            msg += "   • Glenn Diesen (Geopolitik)\n"
            msg += "   • Alexander Mercouris (Daily Updates)\n"
            msg += "   • Luke Gromen (Gold Trading)\n"
            msg += "   • Raoul Pal (Macro Timing)\n"
            msg += "   • Jeff Snider (Dollar/Liquidity)\n"
            msg += "   • Lyn Alden (Portfolio Strategy)\n"
            msg += "   • Steven Van Metre (Deflation)\n"
            msg += "   • George Gammon (Macro Education)\n"
            msg += "   • Adam Taggart (Expert Interviews)\n"
            msg += "\n   ⚠️ Video-Daten werden geladen...\n"
        
        msg += "\n"
        
        # News Summary
        news = analysis.get('news_summary', {})
        top_facts = news.get('top_facts', [])
        
        if top_facts:
            msg += "📰 *TOP FACTS (Cross-Verified):*\n"
            for fact in top_facts[:5]:
                confidence = '🟢' if fact['confidence'] > 7 else '🟡' if fact['confidence'] > 4 else '⚪'
                msg += f"   {confidence} {fact['keyword'].title()} ({fact['mentions']} sources)\n"
            msg += "\n"
        
        # Trading Impact
        impact = analysis.get('trading_impact', {})
        msg += "💰 *TRADING IMPACT:*\n"
        msg += f"   Gold: {impact.get('gold', 'N/A')}\n"
        msg += f"   Bitcoin: {impact.get('bitcoin', 'N/A')}\n"
        msg += f"   Equities: {impact.get('equities', 'N/A')}\n\n"
        
        # Portfolio Recommendation
        rec = analysis.get('portfolio_recommendation', {})
        msg += "✅ *PORTFOLIO-EMPFEHLUNG:*\n"
        msg += f"   {rec.get('action', 'MAINTAIN')}\n"
        
        recommended = rec.get('recommended', {})
        msg += f"   Gold: {recommended.get('gold', 18)}%\n"
        msg += f"   Bitcoin: {recommended.get('bitcoin', 8)}%\n"
        msg += f"   Cash: {recommended.get('cash', 74)}%\n"
        
        return msg

if __name__ == "__main__":
    # Test the professional analyzer
    analyzer = ProfessionalGeopoliticsAnalyzer()
    
    print("\nTesting Professional Geopolitics Analyzer...")
    print("="*70)
    
    # Run comprehensive analysis
    analysis = analyzer.get_comprehensive_analysis()
    
    print("\n" + "="*70)
    print("TELEGRAM FORMAT:")
    print("="*70)
    print(analyzer.format_for_telegram(analysis))

