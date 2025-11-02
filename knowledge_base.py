"""
Knowledge Base for Trading System
Stores lessons learned, insights, strategies, and expert opinions
"""

import sqlite3
from datetime import datetime
import json

class KnowledgeBase:
    def __init__(self, db_path='knowledge_base.db'):
        self.db_path = db_path
        self.conn = None
        self.initialize_database()
    
    def initialize_database(self):
        """Create database tables if they don't exist"""
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        
        # Lessons Learned table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS lessons_learned (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                trade_id TEXT,
                asset TEXT NOT NULL,
                lesson TEXT NOT NULL,
                category TEXT NOT NULL,
                confidence INTEGER NOT NULL,
                outcome TEXT,
                created_at TEXT NOT NULL
            )
        ''')
        
        # Insights table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS insights (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                insight TEXT NOT NULL,
                source TEXT NOT NULL,
                category TEXT NOT NULL,
                validation_score INTEGER NOT NULL,
                applied BOOLEAN DEFAULT 0,
                created_at TEXT NOT NULL
            )
        ''')
        
        # Strategies table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS strategies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                strategy_id TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                description TEXT NOT NULL,
                parameters TEXT,
                performance_score REAL,
                active BOOLEAN DEFAULT 1,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        ''')
        
        # Expert Opinions table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS expert_opinions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                expert TEXT NOT NULL,
                topic TEXT NOT NULL,
                opinion TEXT NOT NULL,
                confidence INTEGER NOT NULL,
                outcome TEXT,
                created_at TEXT NOT NULL
            )
        ''')
        
        # Performance Reviews table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS performance_reviews (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                week_start TEXT NOT NULL,
                week_end TEXT NOT NULL,
                total_trades INTEGER NOT NULL,
                winning_trades INTEGER NOT NULL,
                losing_trades INTEGER NOT NULL,
                total_return REAL NOT NULL,
                best_trade TEXT,
                worst_trade TEXT,
                key_lessons TEXT,
                recommendations TEXT,
                created_at TEXT NOT NULL
            )
        ''')
        
        self.conn.commit()
        print("✅ Knowledge Base initialized")
    
    def add_lesson(self, date, asset, lesson, category, confidence, trade_id=None, outcome=None):
        """Add a new lesson learned"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO lessons_learned 
            (date, trade_id, asset, lesson, category, confidence, outcome, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (date, trade_id, asset, lesson, category, confidence, outcome, 
              datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        self.conn.commit()
        return cursor.lastrowid
    
    def add_insight(self, date, insight, source, category, validation_score):
        """Add a new insight"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO insights 
            (date, insight, source, category, validation_score, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (date, insight, source, category, validation_score,
              datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        self.conn.commit()
        return cursor.lastrowid
    
    def add_strategy(self, strategy_id, name, description, parameters=None, performance_score=None):
        """Add or update a trading strategy"""
        cursor = self.conn.cursor()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        cursor.execute('''
            INSERT OR REPLACE INTO strategies 
            (strategy_id, name, description, parameters, performance_score, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (strategy_id, name, description, json.dumps(parameters) if parameters else None,
              performance_score, now, now))
        self.conn.commit()
        return cursor.lastrowid
    
    def add_expert_opinion(self, date, expert, topic, opinion, confidence, outcome=None):
        """Add expert opinion"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO expert_opinions 
            (date, expert, topic, opinion, confidence, outcome, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (date, expert, topic, opinion, confidence, outcome,
              datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        self.conn.commit()
        return cursor.lastrowid
    
    def add_performance_review(self, week_start, week_end, total_trades, winning_trades, 
                               losing_trades, total_return, best_trade=None, worst_trade=None,
                               key_lessons=None, recommendations=None):
        """Add weekly performance review"""
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO performance_reviews 
            (week_start, week_end, total_trades, winning_trades, losing_trades, 
             total_return, best_trade, worst_trade, key_lessons, recommendations, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (week_start, week_end, total_trades, winning_trades, losing_trades,
              total_return, best_trade, worst_trade, key_lessons, recommendations,
              datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        self.conn.commit()
        return cursor.lastrowid
    
    def get_recent_lessons(self, limit=10, category=None):
        """Get recent lessons learned"""
        cursor = self.conn.cursor()
        if category:
            cursor.execute('''
                SELECT * FROM lessons_learned 
                WHERE category = ?
                ORDER BY date DESC 
                LIMIT ?
            ''', (category, limit))
        else:
            cursor.execute('''
                SELECT * FROM lessons_learned 
                ORDER BY date DESC 
                LIMIT ?
            ''', (limit,))
        
        columns = [desc[0] for desc in cursor.description]
        results = cursor.fetchall()
        return [dict(zip(columns, row)) for row in results]
    
    def get_recent_insights(self, limit=10, category=None):
        """Get recent insights"""
        cursor = self.conn.cursor()
        if category:
            cursor.execute('''
                SELECT * FROM insights 
                WHERE category = ?
                ORDER BY date DESC 
                LIMIT ?
            ''', (category, limit))
        else:
            cursor.execute('''
                SELECT * FROM insights 
                ORDER BY date DESC 
                LIMIT ?
            ''', (limit,))
        
        columns = [desc[0] for desc in cursor.description]
        results = cursor.fetchall()
        return [dict(zip(columns, row)) for row in results]
    
    def get_active_strategies(self):
        """Get all active strategies"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM strategies 
            WHERE active = 1
            ORDER BY performance_score DESC
        ''')
        
        columns = [desc[0] for desc in cursor.description]
        results = cursor.fetchall()
        return [dict(zip(columns, row)) for row in results]
    
    def get_latest_performance_review(self):
        """Get the most recent performance review"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM performance_reviews 
            ORDER BY week_end DESC 
            LIMIT 1
        ''')
        
        columns = [desc[0] for desc in cursor.description]
        result = cursor.fetchone()
        return dict(zip(columns, result)) if result else None
    
    def get_expert_opinions(self, expert=None, limit=10):
        """Get expert opinions"""
        cursor = self.conn.cursor()
        if expert:
            cursor.execute('''
                SELECT * FROM expert_opinions 
                WHERE expert = ?
                ORDER BY date DESC 
                LIMIT ?
            ''', (expert, limit))
        else:
            cursor.execute('''
                SELECT * FROM expert_opinions 
                ORDER BY date DESC 
                LIMIT ?
            ''', (limit,))
        
        columns = [desc[0] for desc in cursor.description]
        results = cursor.fetchall()
        return [dict(zip(columns, row)) for row in results]
    
    def get_statistics(self):
        """Get knowledge base statistics"""
        cursor = self.conn.cursor()
        
        stats = {}
        
        # Count lessons
        cursor.execute('SELECT COUNT(*) FROM lessons_learned')
        stats['total_lessons'] = cursor.fetchone()[0]
        
        # Count insights
        cursor.execute('SELECT COUNT(*) FROM insights')
        stats['total_insights'] = cursor.fetchone()[0]
        
        # Count strategies
        cursor.execute('SELECT COUNT(*) FROM strategies WHERE active = 1')
        stats['active_strategies'] = cursor.fetchone()[0]
        
        # Count expert opinions
        cursor.execute('SELECT COUNT(*) FROM expert_opinions')
        stats['total_expert_opinions'] = cursor.fetchone()[0]
        
        # Count performance reviews
        cursor.execute('SELECT COUNT(*) FROM performance_reviews')
        stats['total_reviews'] = cursor.fetchone()[0]
        
        return stats
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()

if __name__ == "__main__":
    # Test knowledge base
    print("Testing Knowledge Base...")
    print("="*70)
    
    kb = KnowledgeBase()
    
    # Add sample lessons
    print("\n1. Adding sample lessons...")
    kb.add_lesson(
        date='2025-10-25',
        asset='Gold',
        lesson='Gold rallies strongly during nuclear tensions',
        category='Geopolitics',
        confidence=9,
        outcome='Correct - Gold +2.5%'
    )
    
    kb.add_lesson(
        date='2025-10-28',
        asset='Silver',
        lesson='Silver at $49 shows topping pattern similar to 2011',
        category='Technical Analysis',
        confidence=8,
        outcome='Pending'
    )
    
    # Add sample insights
    print("2. Adding sample insights...")
    kb.add_insight(
        date='2025-10-30',
        insight='Nuclear escalation events have 3-5 day impact window on gold prices',
        source='Historical Analysis',
        category='Geopolitics',
        validation_score=9
    )
    
    # Add sample strategy
    print("3. Adding sample strategy...")
    kb.add_strategy(
        strategy_id='gold_nuclear_escalation',
        name='Gold Nuclear Escalation Strategy',
        description='Increase gold allocation when nuclear risk score > 8/10',
        parameters={'risk_threshold': 8, 'target_allocation': 0.25, 'leverage': 4},
        performance_score=8.5
    )
    
    # Add sample expert opinion
    print("4. Adding sample expert opinion...")
    kb.add_expert_opinion(
        date='2025-10-29',
        expert='Glenn Diesen',
        topic='Nuclear Escalation',
        opinion='US-Russia tensions at highest level since Cold War',
        confidence=9
    )
    
    # Get statistics
    print("\n5. Knowledge Base Statistics:")
    print("-"*70)
    stats = kb.get_statistics()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Get recent lessons
    print("\n6. Recent Lessons:")
    print("-"*70)
    lessons = kb.get_recent_lessons(limit=5)
    for lesson in lessons:
        print(f"   [{lesson['date']}] {lesson['asset']}: {lesson['lesson']}")
        print(f"   Confidence: {lesson['confidence']}/10 | Outcome: {lesson['outcome']}")
        print()
    
    # Get recent insights
    print("7. Recent Insights:")
    print("-"*70)
    insights = kb.get_recent_insights(limit=5)
    for insight in insights:
        print(f"   [{insight['date']}] {insight['insight']}")
        print(f"   Source: {insight['source']} | Score: {insight['validation_score']}/10")
        print()
    
    kb.close()
    print("="*70)
    print("✅ Knowledge Base test complete!")

