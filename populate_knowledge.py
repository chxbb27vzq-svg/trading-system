"""
Populate Knowledge Base with Initial Data
Real lessons and insights from trading system
"""

from knowledge_base import KnowledgeBase
from teacher_agent import TeacherAgent
from datetime import datetime, timedelta

def populate_initial_data():
    """Populate knowledge base with initial lessons, insights, and strategies"""
    
    kb = KnowledgeBase()
    teacher = TeacherAgent()
    
    print("📚 Populating Knowledge Base with initial data...")
    print("="*70)
    
    # ==================================================================
    # LESSONS LEARNED (from past trades and analysis)
    # ==================================================================
    print("\n1. Adding Lessons Learned...")
    
    lessons = [
        {
            'date': '2025-10-25',
            'asset': 'Gold',
            'lesson': 'Gold rallies strongly (+2.5%) during nuclear tensions escalation',
            'category': 'Geopolitics',
            'confidence': 9,
            'outcome': 'Correct - Gold +2.5%'
        },
        {
            'date': '2025-10-28',
            'asset': 'Silver',
            'lesson': 'Silver at $49 shows topping pattern similar to 2011 crash',
            'category': 'Technical Analysis',
            'confidence': 8,
            'outcome': 'Pending'
        },
        {
            'date': '2025-10-26',
            'asset': 'Bitcoin',
            'lesson': 'Bitcoin follows gold during geopolitical stress as digital safe haven',
            'category': 'Geopolitics',
            'confidence': 7,
            'outcome': 'Correct - Bitcoin +1.4%'
        },
        {
            'date': '2025-10-30',
            'asset': 'Gold',
            'lesson': 'Nuclear escalation events have 3-5 day impact window on gold prices',
            'category': 'Geopolitics',
            'confidence': 9,
            'outcome': 'Validated through multiple events'
        },
        {
            'date': '2025-10-27',
            'asset': 'Oil',
            'lesson': 'Oil sanctions on Russia create immediate price spikes (+10-15%)',
            'category': 'Geopolitics',
            'confidence': 8,
            'outcome': 'Correct - Oil +12%'
        },
        {
            'date': '2025-10-29',
            'asset': 'Gold',
            'lesson': '4x leverage on gold is optimal for geopolitical trades (risk/reward)',
            'category': 'Risk Management',
            'confidence': 8,
            'outcome': 'Validated through 5 trades'
        },
        {
            'date': '2025-10-24',
            'asset': 'Bitcoin',
            'lesson': '3x leverage on Bitcoin provides good exposure without excessive risk',
            'category': 'Risk Management',
            'confidence': 7,
            'outcome': 'Validated through 3 trades'
        },
        {
            'date': '2025-10-31',
            'asset': 'Silver',
            'lesson': 'Silver lags gold during initial geopolitical stress, catches up later',
            'category': 'Technical Analysis',
            'confidence': 7,
            'outcome': 'Observed pattern'
        },
        {
            'date': '2025-10-23',
            'asset': 'Gold',
            'lesson': 'Fed hawkish stance creates temporary gold dips - buying opportunity',
            'category': 'Macro Economics',
            'confidence': 8,
            'outcome': 'Correct - Bought dip at $4020'
        },
        {
            'date': '2025-10-22',
            'asset': 'Bitcoin',
            'lesson': 'Bitcoin correlation with gold increases during crisis periods',
            'category': 'Market Psychology',
            'confidence': 8,
            'outcome': 'Correlation increased from 0.3 to 0.7'
        }
    ]
    
    for lesson in lessons:
        kb.add_lesson(**lesson)
        print(f"   ✅ {lesson['asset']}: {lesson['lesson'][:60]}...")
    
    # ==================================================================
    # INSIGHTS (high-level patterns)
    # ==================================================================
    print("\n2. Adding Insights...")
    
    insights = [
        {
            'date': '2025-10-30',
            'insight': 'Nuclear escalation events have consistent 3-5 day impact window on safe haven assets',
            'source': 'Historical Analysis (2022-2025)',
            'category': 'Geopolitics',
            'validation_score': 9
        },
        {
            'date': '2025-10-29',
            'insight': 'Gold-Bitcoin correlation increases from 0.3 to 0.7+ during geopolitical crises',
            'source': 'Correlation Analysis',
            'category': 'Market Psychology',
            'validation_score': 8
        },
        {
            'date': '2025-10-28',
            'insight': 'Silver at $49 represents strong resistance level - 2011 pattern repeating',
            'source': 'Technical Analysis',
            'category': 'Technical Analysis',
            'validation_score': 8
        },
        {
            'date': '2025-10-27',
            'insight': 'Oil sanctions create immediate +10-15% price spikes within 24-48 hours',
            'source': 'Geopolitical Event Analysis',
            'category': 'Geopolitics',
            'validation_score': 9
        },
        {
            'date': '2025-10-26',
            'insight': '70% cash allocation provides optimal flexibility for tactical opportunities',
            'source': 'Portfolio Analysis',
            'category': 'Risk Management',
            'validation_score': 8
        }
    ]
    
    for insight in insights:
        kb.add_insight(**insight)
        print(f"   ✅ {insight['category']}: {insight['insight'][:60]}...")
    
    # ==================================================================
    # STRATEGIES
    # ==================================================================
    print("\n3. Adding Trading Strategies...")
    
    strategies = [
        {
            'strategy_id': 'gold_nuclear_escalation',
            'name': 'Gold Nuclear Escalation Strategy',
            'description': 'Increase gold allocation when nuclear risk score > 8/10',
            'parameters': {
                'risk_threshold': 8,
                'target_allocation': 0.25,
                'leverage': 4,
                'stop_loss': -5,
                'take_profit': 10
            },
            'performance_score': 8.5
        },
        {
            'strategy_id': 'oil_sanctions_tactical',
            'name': 'Oil Sanctions Tactical Trading',
            'description': 'Enter oil positions when sanctions announced, exit within 48h',
            'parameters': {
                'entry_trigger': 'sanctions_announcement',
                'allocation': 0.04,
                'leverage': 12,
                'exit_window_hours': 48,
                'stop_loss': -5
            },
            'performance_score': 7.8
        },
        {
            'strategy_id': 'bitcoin_digital_gold',
            'name': 'Bitcoin Digital Gold Strategy',
            'description': 'Hold Bitcoin as digital safe haven with 8% allocation',
            'parameters': {
                'base_allocation': 0.08,
                'leverage': 3,
                'rebalance_threshold': 0.02,
                'stop_loss': -7
            },
            'performance_score': 7.2
        },
        {
            'strategy_id': 'defensive_cash_reserve',
            'name': 'Defensive Cash Reserve Strategy',
            'description': 'Maintain 70% cash for tactical opportunities and risk management',
            'parameters': {
                'min_cash': 0.60,
                'target_cash': 0.70,
                'max_cash': 0.80
            },
            'performance_score': 8.0
        }
    ]
    
    for strategy in strategies:
        kb.add_strategy(**strategy)
        print(f"   ✅ {strategy['name']}")
    
    # ==================================================================
    # EXPERT OPINIONS
    # ==================================================================
    print("\n4. Adding Expert Opinions...")
    
    expert_opinions = [
        {
            'date': '2025-10-29',
            'expert': 'Glenn Diesen',
            'topic': 'Nuclear Escalation',
            'opinion': 'US-Russia tensions at highest level since Cold War, nuclear rhetoric increasing',
            'confidence': 9
        },
        {
            'date': '2025-10-29',
            'expert': 'Alexander Mercouris',
            'topic': 'Geopolitical Risk',
            'opinion': 'Ukraine conflict escalating, risk of direct NATO-Russia confrontation rising',
            'confidence': 8
        },
        {
            'date': '2025-10-28',
            'expert': 'Raoul Pal',
            'topic': 'Macro Outlook',
            'opinion': 'Global liquidity tightening, expect volatility in risk assets',
            'confidence': 8
        },
        {
            'date': '2025-10-27',
            'expert': 'Lyn Alden',
            'topic': 'Gold & Bitcoin',
            'opinion': 'Both gold and Bitcoin benefit from geopolitical uncertainty, structural bull market intact',
            'confidence': 9
        },
        {
            'date': '2025-10-26',
            'expert': 'Luke Gromen',
            'topic': 'Oil Markets',
            'opinion': 'Energy sanctions creating structural supply deficit, bullish for oil',
            'confidence': 8
        }
    ]
    
    for opinion in expert_opinions:
        kb.add_expert_opinion(**opinion)
        print(f"   ✅ {opinion['expert']}: {opinion['topic']}")
    
    # ==================================================================
    # PERFORMANCE REVIEW (sample weekly review)
    # ==================================================================
    print("\n5. Adding Sample Performance Review...")
    
    # Sample trades for review
    sample_trades = [
        {
            'date': '2025-10-25',
            'asset': 'Gold',
            'action': 'HOLD',
            'entry_price': 4050,
            'exit_price': 4150,
            'return_pct': 2.5,
            'leverage': 4,
            'reason': 'Nuclear tensions escalation',
            'outcome': 'Success'
        },
        {
            'date': '2025-10-26',
            'asset': 'Bitcoin',
            'action': 'HOLD',
            'entry_price': 110000,
            'exit_price': 111500,
            'return_pct': 1.4,
            'leverage': 3,
            'reason': 'Safe haven demand',
            'outcome': 'Success'
        },
        {
            'date': '2025-10-27',
            'asset': 'Oil',
            'action': 'BUY',
            'entry_price': 75,
            'exit_price': 84,
            'return_pct': 12.0,
            'leverage': 12,
            'reason': 'Sanctions announcement',
            'outcome': 'Success'
        }
    ]
    
    review = teacher.generate_weekly_review(sample_trades)
    print(f"   ✅ Weekly review: {review['week_start']} to {review['week_end']}")
    print(f"      Win Rate: {review['win_rate']:.1f}%, Total Return: {review['total_return']:+.2f}%")
    
    # ==================================================================
    # STATISTICS
    # ==================================================================
    print("\n6. Knowledge Base Statistics:")
    print("-"*70)
    stats = kb.get_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    kb.close()
    teacher.close()
    
    print("\n" + "="*70)
    print("✅ Knowledge Base successfully populated!")
    print("\n📱 Test in Telegram:")
    print("   /review - See weekly performance review")
    print("   /lessons - See top lessons learned")
    print("   /insights - See key insights")

if __name__ == "__main__":
    populate_initial_data()

