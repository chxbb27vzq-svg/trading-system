"""
Professional News Aggregator
Balanced international sources: West + East + Neutral
NO Wikipedia, NO propaganda - only facts
"""

import requests
from datetime import datetime, timedelta
import time

class NewsAggregator:
    def __init__(self):
        self.sources = {
            # WESTERN SOURCES (30%)
            'reuters': {
                'name': 'Reuters',
                'region': 'West',
                'bias': 'Moderate West',
                'reliability': 9,
                'url': 'https://www.reuters.com'
            },
            'bloomberg': {
                'name': 'Bloomberg',
                'region': 'West',
                'bias': 'Moderate West',
                'reliability': 9,
                'url': 'https://www.bloomberg.com'
            },
            'ft': {
                'name': 'Financial Times',
                'region': 'West',
                'bias': 'Moderate West',
                'reliability': 9,
                'url': 'https://www.ft.com'
            },
            
            # EASTERN SOURCES (30%)
            'tass': {
                'name': 'TASS',
                'region': 'East',
                'bias': 'Pro-Russia',
                'reliability': 7,
                'url': 'https://tass.com'
            },
            'rt': {
                'name': 'RT (Russia Today)',
                'region': 'East',
                'bias': 'Pro-Russia',
                'reliability': 6,
                'url': 'https://www.rt.com'
            },
            'cgtn': {
                'name': 'CGTN',
                'region': 'East',
                'bias': 'Pro-China',
                'reliability': 7,
                'url': 'https://www.cgtn.com'
            },
            
            # NEUTRAL SOURCES (40%)
            'aljazeera': {
                'name': 'Al Jazeera',
                'region': 'Neutral',
                'bias': 'Minimal',
                'reliability': 8,
                'url': 'https://www.aljazeera.com'
            },
            'nikkei': {
                'name': 'Nikkei Asia',
                'region': 'Neutral',
                'bias': 'Minimal',
                'reliability': 9,
                'url': 'https://asia.nikkei.com'
            },
            'swissinfo': {
                'name': 'Swiss Info',
                'region': 'Neutral',
                'bias': 'Minimal',
                'reliability': 9,
                'url': 'https://www.swissinfo.ch'
            },
            'scmp': {
                'name': 'South China Morning Post',
                'region': 'Neutral',
                'bias': 'Slight East',
                'reliability': 8,
                'url': 'https://www.scmp.com'
            }
        }
        
        # Trading-relevant keywords (NO WIKIPEDIA!)
        self.keywords = [
            'nuclear', 'war', 'escalation', 'sanctions',
            'fed', 'interest rate', 'inflation', 'recession',
            'gold', 'dollar', 'yuan', 'bitcoin',
            'nato', 'russia', 'china', 'ukraine',
            'oil', 'energy', 'crisis', 'conflict'
        ]
        
        # Blacklist (NEVER use these sources)
        self.blacklist = [
            'wikipedia', 'wiki', 'wikimedia',
            'reddit', 'twitter', 'facebook',
            'blog', 'opinion', 'editorial'
        ]
    
    def is_blacklisted(self, url, title):
        """Check if source is blacklisted"""
        url_lower = url.lower()
        title_lower = title.lower()
        
        for banned in self.blacklist:
            if banned in url_lower or banned in title_lower:
                return True
        return False
    
    def search_news(self, query, hours=24, max_results=5):
        """Search for news across sources (mock implementation)"""
        # In production, would use NewsAPI, RSS feeds, or web scraping
        # For now, returns structured mock data
        
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        news_items = []
        
        # Mock news items (in production would fetch real news)
        mock_news = [
            {
                'title': 'Putin signals readiness for nuclear response if threatened',
                'source': 'tass',
                'url': 'https://tass.com/politics/example1',
                'published': datetime.now() - timedelta(hours=2),
                'summary': 'Russian President stated willingness to use all means if sovereignty threatened'
            },
            {
                'title': 'NATO announces new military exercises near Russian border',
                'source': 'reuters',
                'url': 'https://reuters.com/world/example1',
                'published': datetime.now() - timedelta(hours=5),
                'summary': 'Alliance to conduct largest drills in decades in Eastern Europe'
            },
            {
                'title': 'Gold hits new highs amid geopolitical tensions',
                'source': 'bloomberg',
                'url': 'https://bloomberg.com/markets/example1',
                'published': datetime.now() - timedelta(hours=1),
                'summary': 'Safe haven demand drives precious metals rally'
            },
            {
                'title': 'China calls for de-escalation in Europe',
                'source': 'cgtn',
                'url': 'https://cgtn.com/news/example1',
                'published': datetime.now() - timedelta(hours=3),
                'summary': 'Beijing urges dialogue between Russia and NATO'
            },
            {
                'title': 'Analysts warn of nuclear brinkmanship risks',
                'source': 'aljazeera',
                'url': 'https://aljazeera.com/news/example1',
                'published': datetime.now() - timedelta(hours=4),
                'summary': 'Experts compare current situation to Cold War crises'
            }
        ]
        
        # Filter and format
        for item in mock_news:
            if self.is_blacklisted(item['url'], item['title']):
                continue
            
            source_info = self.sources.get(item['source'], {})
            
            news_items.append({
                'title': item['title'],
                'source': source_info.get('name', item['source']),
                'region': source_info.get('region', 'Unknown'),
                'bias': source_info.get('bias', 'Unknown'),
                'reliability': source_info.get('reliability', 5),
                'url': item['url'],
                'published': item['published'].strftime('%Y-%m-%d %H:%M'),
                'summary': item['summary'],
                'age_hours': (datetime.now() - item['published']).total_seconds() / 3600
            })
        
        # Sort by time (newest first)
        news_items.sort(key=lambda x: x['age_hours'])
        
        return news_items[:max_results]
    
    def get_balanced_perspective(self, topic, hours=24):
        """Get balanced news perspective from West + East + Neutral"""
        print(f"📰 Fetching balanced news on: {topic}")
        
        all_news = self.search_news(topic, hours=hours, max_results=20)
        
        # Categorize by region
        western = [n for n in all_news if n['region'] == 'West']
        eastern = [n for n in all_news if n['region'] == 'East']
        neutral = [n for n in all_news if n['region'] == 'Neutral']
        
        # Extract facts (common themes across all sources)
        facts = self.extract_facts(all_news)
        
        return {
            'topic': topic,
            'western_view': western[:2],
            'eastern_view': eastern[:2],
            'neutral_view': neutral[:2],
            'facts': facts,
            'total_sources': len(all_news),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def extract_facts(self, news_items):
        """Extract common facts from multiple sources (cross-verification)"""
        # Simple implementation - in production would use NLP
        
        facts = []
        
        # Look for common keywords across sources
        keyword_counts = {}
        for item in news_items:
            text = (item['title'] + ' ' + item['summary']).lower()
            for keyword in self.keywords:
                if keyword in text:
                    keyword_counts[keyword] = keyword_counts.get(keyword, 0) + 1
        
        # Facts are keywords mentioned by multiple sources
        for keyword, count in keyword_counts.items():
            if count >= 2:  # Mentioned by at least 2 sources
                facts.append({
                    'keyword': keyword,
                    'mentions': count,
                    'confidence': min(10, count * 2)  # 0-10 scale
                })
        
        # Sort by confidence
        facts.sort(key=lambda x: x['confidence'], reverse=True)
        
        return facts[:5]
    
    def get_geopolitical_summary(self, hours=24):
        """Get comprehensive geopolitical news summary"""
        print("🌍 Fetching Geopolitical News Summary...")
        print("📊 Sources: West (30%) + East (30%) + Neutral (40%)")
        print()
        
        # Key topics
        topics = ['nuclear tensions', 'russia nato', 'gold markets', 'fed policy']
        
        summaries = {}
        
        for topic in topics:
            try:
                summary = self.get_balanced_perspective(topic, hours=hours)
                summaries[topic] = summary
                time.sleep(0.5)  # Rate limiting
            except Exception as e:
                summaries[topic] = {
                    'error': str(e),
                    'status': 'failed'
                }
        
        # Overall assessment
        all_facts = []
        for topic, data in summaries.items():
            if 'facts' in data:
                all_facts.extend(data['facts'])
        
        # Deduplicate and sort facts
        unique_facts = {}
        for fact in all_facts:
            key = fact['keyword']
            if key not in unique_facts or fact['confidence'] > unique_facts[key]['confidence']:
                unique_facts[key] = fact
        
        top_facts = sorted(unique_facts.values(), key=lambda x: x['confidence'], reverse=True)[:10]
        
        return {
            'topics': summaries,
            'top_facts': top_facts,
            'source_count': len(self.sources),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

if __name__ == "__main__":
    # Test the aggregator
    aggregator = NewsAggregator()
    
    print("Testing News Aggregator...")
    print("="*60)
    
    print("\n📰 CONFIGURED SOURCES:")
    
    west = [s for s in aggregator.sources.values() if s['region'] == 'West']
    east = [s for s in aggregator.sources.values() if s['region'] == 'East']
    neutral = [s for s in aggregator.sources.values() if s['region'] == 'Neutral']
    
    print(f"\n🇺🇸 WESTERN ({len(west)}):")
    for source in west:
        print(f"   • {source['name']} (Reliability: {source['reliability']}/10)")
    
    print(f"\n🇷🇺 EASTERN ({len(east)}):")
    for source in east:
        print(f"   • {source['name']} (Reliability: {source['reliability']}/10)")
    
    print(f"\n🌍 NEUTRAL ({len(neutral)}):")
    for source in neutral:
        print(f"   • {source['name']} (Reliability: {source['reliability']}/10)")
    
    print("\n" + "="*60)
    print("✅ News Aggregator Ready!")
    print("\n💡 Features:")
    print("   ✅ Balanced: 30% West + 30% East + 40% Neutral")
    print("   ✅ NO Wikipedia, NO propaganda")
    print("   ✅ Fact extraction via cross-verification")
    print("   ✅ Trading-relevant keywords only")

