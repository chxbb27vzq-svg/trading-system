"""
Teacher Agent - Performance Analysis & Lesson Extraction
Analyzes trading performance and extracts lessons learned
"""

from knowledge_base import KnowledgeBase
from datetime import datetime, timedelta
import json

class TeacherAgent:
    def __init__(self, kb_path='knowledge_base.db'):
        self.kb = KnowledgeBase(kb_path)
        self.categories = [
            'Geopolitics',
            'Technical Analysis',
            'Risk Management',
            'Macro Economics',
            'Behavioral Finance',
            'Market Psychology'
        ]
    
    def analyze_trade(self, trade_data):
        """
        Analyze a single trade and extract lessons
        
        trade_data format:
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
        }
        """
        lessons = []
        
        # Extract lessons based on outcome
        if trade_data['outcome'] == 'Success':
            # What worked?
            if 'nuclear' in trade_data['reason'].lower() and trade_data['asset'] == 'Gold':
                lesson = {
                    'date': trade_data['date'],
                    'asset': trade_data['asset'],
                    'lesson': f"Gold responds positively to nuclear tensions - gained {trade_data['return_pct']}%",
                    'category': 'Geopolitics',
                    'confidence': 9,
                    'outcome': f"Correct - {trade_data['asset']} +{trade_data['return_pct']}%"
                }
                lessons.append(lesson)
            
            # Risk management lesson
            if trade_data['return_pct'] > 2.0:
                lesson = {
                    'date': trade_data['date'],
                    'asset': trade_data['asset'],
                    'lesson': f"Leverage {trade_data['leverage']}x worked well for {trade_data['asset']} in this scenario",
                    'category': 'Risk Management',
                    'confidence': 8,
                    'outcome': f"Success - {trade_data['return_pct']}% return"
                }
                lessons.append(lesson)
        
        elif trade_data['outcome'] == 'Failure':
            # What didn't work?
            lesson = {
                'date': trade_data['date'],
                'asset': trade_data['asset'],
                'lesson': f"Strategy failed: {trade_data['reason']} did not produce expected result",
                'category': 'Technical Analysis',
                'confidence': 7,
                'outcome': f"Failed - {trade_data['return_pct']}% loss"
            }
            lessons.append(lesson)
        
        # Store lessons in knowledge base
        for lesson in lessons:
            self.kb.add_lesson(**lesson)
        
        return lessons
    
    def generate_weekly_review(self, trades):
        """
        Generate weekly performance review from trades
        
        trades: list of trade_data dictionaries
        """
        if not trades:
            return None
        
        # Calculate statistics
        total_trades = len(trades)
        winning_trades = len([t for t in trades if t['return_pct'] > 0])
        losing_trades = len([t for t in trades if t['return_pct'] < 0])
        total_return = sum([t['return_pct'] for t in trades])
        
        # Find best and worst trades
        best_trade = max(trades, key=lambda x: x['return_pct'])
        worst_trade = min(trades, key=lambda x: x['return_pct'])
        
        # Extract key lessons
        key_lessons = []
        
        # Lesson 1: Win rate
        win_rate = (winning_trades / total_trades * 100) if total_trades > 0 else 0
        if win_rate >= 60:
            key_lessons.append(f"Strong win rate: {win_rate:.1f}% - Strategy is working")
        elif win_rate < 50:
            key_lessons.append(f"Low win rate: {win_rate:.1f}% - Need strategy adjustment")
        
        # Lesson 2: Best performer
        key_lessons.append(f"Best trade: {best_trade['asset']} +{best_trade['return_pct']}% - {best_trade['reason']}")
        
        # Lesson 3: Worst performer
        if worst_trade['return_pct'] < 0:
            key_lessons.append(f"Worst trade: {worst_trade['asset']} {worst_trade['return_pct']}% - Avoid similar setups")
        
        # Generate recommendations
        recommendations = []
        
        if total_return > 5:
            recommendations.append("Excellent week! Consider increasing position sizes slightly")
        elif total_return < -2:
            recommendations.append("Reduce position sizes and review risk management")
        
        if winning_trades > 0 and losing_trades > 0:
            avg_win = sum([t['return_pct'] for t in trades if t['return_pct'] > 0]) / winning_trades
            avg_loss = sum([t['return_pct'] for t in trades if t['return_pct'] < 0]) / losing_trades
            win_loss_ratio = abs(avg_win / avg_loss) if avg_loss != 0 else 0
            
            if win_loss_ratio > 2:
                recommendations.append(f"Excellent risk/reward ratio: {win_loss_ratio:.2f}:1")
            elif win_loss_ratio < 1.5:
                recommendations.append(f"Improve risk/reward ratio (current: {win_loss_ratio:.2f}:1)")
        
        # Store review in knowledge base
        week_start = min([t['date'] for t in trades])
        week_end = max([t['date'] for t in trades])
        
        self.kb.add_performance_review(
            week_start=week_start,
            week_end=week_end,
            total_trades=total_trades,
            winning_trades=winning_trades,
            losing_trades=losing_trades,
            total_return=total_return,
            best_trade=json.dumps(best_trade),
            worst_trade=json.dumps(worst_trade),
            key_lessons=json.dumps(key_lessons),
            recommendations=json.dumps(recommendations)
        )
        
        return {
            'week_start': week_start,
            'week_end': week_end,
            'total_trades': total_trades,
            'winning_trades': winning_trades,
            'losing_trades': losing_trades,
            'win_rate': win_rate,
            'total_return': total_return,
            'best_trade': best_trade,
            'worst_trade': worst_trade,
            'key_lessons': key_lessons,
            'recommendations': recommendations
        }
    
    def extract_insights(self, lessons):
        """Extract high-level insights from multiple lessons"""
        insights = []
        
        # Group lessons by category
        by_category = {}
        for lesson in lessons:
            cat = lesson['category']
            if cat not in by_category:
                by_category[cat] = []
            by_category[cat].append(lesson)
        
        # Generate insights per category
        for category, cat_lessons in by_category.items():
            if len(cat_lessons) >= 2:
                # Pattern detected
                avg_confidence = sum([l['confidence'] for l in cat_lessons]) / len(cat_lessons)
                
                insight = {
                    'date': datetime.now().strftime('%Y-%m-%d'),
                    'insight': f"Pattern detected in {category}: {len(cat_lessons)} related lessons with avg confidence {avg_confidence:.1f}/10",
                    'source': 'Teacher Agent Analysis',
                    'category': category,
                    'validation_score': int(avg_confidence)
                }
                
                self.kb.add_insight(**insight)
                insights.append(insight)
        
        return insights
    
    def recommend_strategy_adjustments(self):
        """Recommend strategy adjustments based on recent performance"""
        recommendations = []
        
        # Get recent lessons
        recent_lessons = self.kb.get_recent_lessons(limit=20)
        
        # Analyze by asset
        by_asset = {}
        for lesson in recent_lessons:
            asset = lesson['asset']
            if asset not in by_asset:
                by_asset[asset] = {'success': 0, 'total': 0}
            by_asset[asset]['total'] += 1
            if 'Correct' in str(lesson['outcome']) or 'Success' in str(lesson['outcome']):
                by_asset[asset]['success'] += 1
        
        # Generate recommendations
        for asset, stats in by_asset.items():
            success_rate = (stats['success'] / stats['total'] * 100) if stats['total'] > 0 else 0
            
            if success_rate >= 70:
                recommendations.append({
                    'asset': asset,
                    'action': 'INCREASE',
                    'reason': f"High success rate: {success_rate:.1f}% ({stats['success']}/{stats['total']} trades)",
                    'confidence': 8
                })
            elif success_rate < 40:
                recommendations.append({
                    'asset': asset,
                    'action': 'DECREASE',
                    'reason': f"Low success rate: {success_rate:.1f}% ({stats['success']}/{stats['total']} trades)",
                    'confidence': 7
                })
        
        return recommendations
    
    def format_review_for_telegram(self, review):
        """Format weekly review for Telegram"""
        if not review:
            return "📊 Keine Performance-Daten verfügbar"
        
        msg = "📊 *WÖCHENTLICHE PERFORMANCE-REVIEW*\n\n"
        msg += f"📅 Zeitraum: {review['week_start']} bis {review['week_end']}\n\n"
        
        msg += f"📈 *STATISTIK:*\n"
        msg += f"   • Total Trades: {review['total_trades']}\n"
        msg += f"   • Gewinner: {review['winning_trades']} ✅\n"
        msg += f"   • Verlierer: {review['losing_trades']} ❌\n"
        msg += f"   • Win Rate: {review['win_rate']:.1f}%\n"
        msg += f"   • Total Return: {review['total_return']:+.2f}%\n\n"
        
        msg += f"🏆 *BESTER TRADE:*\n"
        msg += f"   • {review['best_trade']['asset']}: {review['best_trade']['return_pct']:+.2f}%\n"
        msg += f"   • Grund: {review['best_trade']['reason']}\n\n"
        
        if review['worst_trade']['return_pct'] < 0:
            msg += f"⚠️ *SCHLECHTESTER TRADE:*\n"
            msg += f"   • {review['worst_trade']['asset']}: {review['worst_trade']['return_pct']:+.2f}%\n"
            msg += f"   • Grund: {review['worst_trade']['reason']}\n\n"
        
        msg += f"💡 *KEY LESSONS:*\n"
        for i, lesson in enumerate(review['key_lessons'][:3], 1):
            msg += f"   {i}. {lesson}\n"
        msg += "\n"
        
        msg += f"🎯 *EMPFEHLUNGEN:*\n"
        for i, rec in enumerate(review['recommendations'][:3], 1):
            msg += f"   {i}. {rec}\n"
        
        return msg
    
    def format_lessons_for_telegram(self, lessons, limit=5):
        """Format lessons for Telegram"""
        if not lessons:
            return "📚 Keine Lessons verfügbar"
        
        msg = "📚 *TOP LESSONS LEARNED*\n\n"
        
        for i, lesson in enumerate(lessons[:limit], 1):
            confidence_emoji = '🟢' if lesson['confidence'] >= 8 else '🟡' if lesson['confidence'] >= 6 else '⚪'
            
            msg += f"{confidence_emoji} *LESSON #{i}:*\n"
            msg += f"   📅 {lesson['date']}\n"
            msg += f"   💰 {lesson['asset']}\n"
            msg += f"   📊 {lesson['category']}\n"
            msg += f"   ✅ {lesson['lesson']}\n"
            msg += f"   🎯 Confidence: {lesson['confidence']}/10\n"
            if lesson['outcome']:
                msg += f"   📈 Outcome: {lesson['outcome']}\n"
            msg += "\n"
        
        return msg
    
    def format_insights_for_telegram(self, insights, limit=5):
        """Format insights for Telegram"""
        if not insights:
            return "💡 Keine Insights verfügbar"
        
        msg = "💡 *KEY INSIGHTS*\n\n"
        
        for i, insight in enumerate(insights[:limit], 1):
            score_emoji = '🟢' if insight['validation_score'] >= 8 else '🟡' if insight['validation_score'] >= 6 else '⚪'
            
            msg += f"{score_emoji} *INSIGHT #{i}:*\n"
            msg += f"   📅 {insight['date']}\n"
            msg += f"   📊 {insight['category']}\n"
            msg += f"   💡 {insight['insight']}\n"
            msg += f"   🔍 Source: {insight['source']}\n"
            msg += f"   ⭐ Score: {insight['validation_score']}/10\n"
            msg += "\n"
        
        return msg
    
    def close(self):
        """Close knowledge base connection"""
        self.kb.close()

if __name__ == "__main__":
    # Test Teacher Agent
    print("Testing Teacher Agent...")
    print("="*70)
    
    teacher = TeacherAgent()
    
    # Sample trades for testing
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
            'asset': 'Silver',
            'action': 'AVOID',
            'entry_price': 49,
            'exit_price': 48,
            'return_pct': -2.0,
            'leverage': 0,
            'reason': 'Topping pattern at resistance',
            'outcome': 'Success'  # Success because we avoided it
        }
    ]
    
    print("\n1. Analyzing individual trades...")
    for trade in sample_trades:
        lessons = teacher.analyze_trade(trade)
        print(f"   Trade: {trade['asset']} → {len(lessons)} lessons extracted")
    
    print("\n2. Generating weekly review...")
    review = teacher.generate_weekly_review(sample_trades)
    print(f"   Week: {review['week_start']} to {review['week_end']}")
    print(f"   Total Return: {review['total_return']:+.2f}%")
    print(f"   Win Rate: {review['win_rate']:.1f}%")
    
    print("\n3. Extracting insights...")
    recent_lessons = teacher.kb.get_recent_lessons(limit=10)
    insights = teacher.extract_insights(recent_lessons)
    print(f"   Generated {len(insights)} insights")
    
    print("\n4. Generating strategy recommendations...")
    recommendations = teacher.recommend_strategy_adjustments()
    print(f"   Generated {len(recommendations)} recommendations")
    for rec in recommendations:
        print(f"   • {rec['asset']}: {rec['action']} - {rec['reason']}")
    
    print("\n5. Telegram Format Preview:")
    print("-"*70)
    print(teacher.format_review_for_telegram(review))
    
    teacher.close()
    print("="*70)
    print("✅ Teacher Agent test complete!")

