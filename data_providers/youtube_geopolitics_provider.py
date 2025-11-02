"""
YouTube Geopolitics Provider
Analyzes expert geopolitical commentary from YouTube channels
Focus: Glenn Diesen, Alexander Mercouris, Luke Gromen
"""

from youtube_transcript_api import YouTubeTranscriptApi
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import re
import time

class YouTubeGeopoliticsProvider:
    def __init__(self, api_key=None):
        self.api_key = api_key or "AIzaSyDummy"  # Will use without API for transcripts
        self.youtube = None
        if api_key and api_key != "AIzaSyDummy":
            self.youtube = build('youtube', 'v3', developerKey=api_key)
        
        # Channel IDs (will be populated)
        self.channels = {
            # GEOPOLITICS
            'glenn_diesen': {
                'name': 'Glenn Diesen',
                'channel_id': '@GlennDiesen',
                'focus': 'Strategy & Russia/NATO Analysis',
                'frequency': 'Weekly',
                'category': 'geopolitics',
                'trading_value': 5
            },
            'alexander_mercouris': {
                'name': 'Alexander Mercouris',
                'channel_id': '@AlexanderMercouris',
                'focus': 'Daily Geopolitical Updates',
                'frequency': 'Daily',
                'category': 'geopolitics',
                'trading_value': 5
            },
            'luke_gromen': {
                'name': 'Luke Gromen',
                'channel_id': '@LukeGromen',
                'focus': 'Gold & Geopolitical Trading',
                'frequency': 'Weekly',
                'category': 'trading',
                'trading_value': 5
            },
            
            # MACRO/FINANCE (NEW)
            'raoul_pal': {
                'name': 'Raoul Pal',
                'channel_id': '@RaoulPal',
                'focus': 'Macro Timing & Gold/Bitcoin',
                'frequency': '2-3x per week',
                'category': 'macro',
                'trading_value': 5
            },
            'jeff_snider': {
                'name': 'Jeff Snider',
                'channel_id': '@EmilKalinowski',  # Eurodollar University
                'focus': 'Dollar System & Liquidity',
                'frequency': 'Weekly',
                'category': 'macro',
                'trading_value': 5
            },
            'lyn_alden': {
                'name': 'Lyn Alden',
                'channel_id': '@LynAlden',
                'focus': 'Portfolio Strategy & Macro',
                'frequency': 'Monthly',
                'category': 'strategy',
                'trading_value': 5
            },
            'steven_van_metre': {
                'name': 'Steven Van Metre',
                'channel_id': '@StevenVanMetre',
                'focus': 'Deflation & Bonds',
                'frequency': 'Daily',
                'category': 'macro',
                'trading_value': 4
            },
            'george_gammon': {
                'name': 'George Gammon',
                'channel_id': '@GeorgeGammon',
                'focus': 'Macro Education',
                'frequency': '2-3x per week',
                'category': 'macro',
                'trading_value': 4
            },
            'adam_taggart': {
                'name': 'Adam Taggart',
                'channel_id': '@thoughtfulmoney',
                'focus': 'Expert Interviews',
                'frequency': 'Daily',
                'category': 'interviews',
                'trading_value': 4
            }
        }
        
        # Trading-relevant keywords
        self.keywords = {
            'nuclear': {'weight': 10, 'impact': 'gold_up_bitcoin_neutral'},
            'escalation': {'weight': 8, 'impact': 'gold_up_equities_down'},
            'war': {'weight': 9, 'impact': 'gold_up_equities_down'},
            'sanctions': {'weight': 7, 'impact': 'gold_up_bitcoin_up'},
            'nato': {'weight': 6, 'impact': 'context_dependent'},
            'russia': {'weight': 6, 'impact': 'context_dependent'},
            'china': {'weight': 6, 'impact': 'context_dependent'},
            'dollar': {'weight': 8, 'impact': 'gold_inverse'},
            'gold': {'weight': 9, 'impact': 'direct'},
            'fed': {'weight': 7, 'impact': 'context_dependent'},
            'inflation': {'weight': 6, 'impact': 'gold_up'},
            'recession': {'weight': 7, 'impact': 'equities_down'},
            'crisis': {'weight': 8, 'impact': 'gold_up_equities_down'}
        }
    
    def search_latest_video(self, channel_name, max_age_days=7):
        """Search for latest video from a channel (fallback without API)"""
        # This is a simplified version - in production would use YouTube Data API
        # For now, returns mock data structure
        return {
            'video_id': 'mock_video_id',
            'title': f'Latest from {channel_name}',
            'published_at': datetime.now().isoformat(),
            'description': 'Geopolitical analysis'
        }
    
    def get_video_transcript(self, video_id):
        """Get transcript for a YouTube video"""
        try:
            transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
            
            # Combine all text
            full_text = ' '.join([entry['text'] for entry in transcript_list])
            
            return {
                'success': True,
                'text': full_text,
                'duration': len(transcript_list),
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'text': None
            }
    
    def extract_keywords(self, text):
        """Extract trading-relevant keywords from text"""
        if not text:
            return {}
        
        text_lower = text.lower()
        found_keywords = {}
        
        for keyword, data in self.keywords.items():
            # Count occurrences
            count = len(re.findall(r'\b' + keyword + r'\b', text_lower))
            if count > 0:
                found_keywords[keyword] = {
                    'count': count,
                    'weight': data['weight'],
                    'impact': data['impact'],
                    'score': count * data['weight']
                }
        
        return found_keywords
    
    def analyze_sentiment(self, text, keywords):
        """Analyze geopolitical sentiment for trading"""
        if not text or not keywords:
            return {
                'overall_risk': 5,
                'gold_sentiment': 'NEUTRAL',
                'bitcoin_sentiment': 'NEUTRAL',
                'equities_sentiment': 'NEUTRAL'
            }
        
        # Calculate risk score (0-10)
        risk_score = 0
        gold_score = 0
        bitcoin_score = 0
        equities_score = 0
        
        for keyword, data in keywords.items():
            risk_score += data['score'] * 0.1
            
            # Impact on assets
            impact = data['impact']
            if 'gold_up' in impact:
                gold_score += data['score']
            if 'bitcoin_up' in impact:
                bitcoin_score += data['score']
            if 'equities_down' in impact:
                equities_score -= data['score']
        
        # Normalize scores
        risk_score = min(10, risk_score)
        
        # Determine sentiments
        def get_sentiment(score):
            if score > 15:
                return 'VERY BULLISH'
            elif score > 8:
                return 'BULLISH'
            elif score > -8:
                return 'NEUTRAL'
            elif score > -15:
                return 'BEARISH'
            else:
                return 'VERY BEARISH'
        
        return {
            'overall_risk': round(risk_score, 1),
            'gold_sentiment': get_sentiment(gold_score),
            'bitcoin_sentiment': get_sentiment(bitcoin_score),
            'equities_sentiment': get_sentiment(equities_score),
            'risk_level': 'CRITICAL' if risk_score > 8 else 'HIGH' if risk_score > 6 else 'MEDIUM' if risk_score > 4 else 'LOW'
        }
    
    def extract_key_insights(self, text, max_insights=3):
        """Extract key insights from transcript"""
        if not text:
            return []
        
        # Simple sentence extraction (in production would use NLP)
        sentences = text.split('.')
        
        # Find sentences with high keyword density
        insights = []
        for sentence in sentences:
            sentence = sentence.strip()
            if len(sentence) < 50 or len(sentence) > 200:
                continue
            
            # Count keywords in sentence
            keyword_count = sum(1 for kw in self.keywords.keys() if kw in sentence.lower())
            
            if keyword_count >= 2:
                insights.append({
                    'text': sentence,
                    'relevance': keyword_count
                })
        
        # Sort by relevance and return top insights
        insights.sort(key=lambda x: x['relevance'], reverse=True)
        return [i['text'] for i in insights[:max_insights]]
    
    def analyze_channel(self, channel_key, max_age_days=7):
        """Analyze latest video from a channel"""
        channel_info = self.channels.get(channel_key)
        if not channel_info:
            return None
        
        print(f"📺 Analyzing {channel_info['name']}...")
        
        # Search for latest video
        video = self.search_latest_video(channel_info['name'], max_age_days)
        
        # Get transcript
        transcript = self.get_video_transcript(video['video_id'])
        
        if not transcript['success']:
            return {
                'channel': channel_info['name'],
                'status': 'error',
                'error': transcript['error'],
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        
        # Extract keywords
        keywords = self.extract_keywords(transcript['text'])
        
        # Analyze sentiment
        sentiment = self.analyze_sentiment(transcript['text'], keywords)
        
        # Extract insights
        insights = self.extract_key_insights(transcript['text'])
        
        return {
            'channel': channel_info['name'],
            'focus': channel_info['focus'],
            'trading_value': channel_info['trading_value'],
            'video_title': video['title'],
            'published_at': video['published_at'],
            'keywords': keywords,
            'sentiment': sentiment,
            'insights': insights,
            'status': 'success',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def get_comprehensive_analysis(self):
        """Get comprehensive geopolitical analysis from all channels"""
        print("🎓 Fetching YouTube Geopolitics + Macro Analysis...")
        print("📺 9 Channels: Diesen, Mercouris, Gromen, Pal, Snider, Alden, Van Metre, Gammon, Taggart")
        print()
        
        results = {}
        
        # Analyze each channel
        for channel_key in ['glenn_diesen', 'alexander_mercouris', 'luke_gromen', 
                            'raoul_pal', 'jeff_snider', 'lyn_alden',
                            'steven_van_metre', 'george_gammon', 'adam_taggart']:
            try:
                analysis = self.analyze_channel(channel_key, max_age_days=7)
                results[channel_key] = analysis
                time.sleep(1)  # Rate limiting
            except Exception as e:
                results[channel_key] = {
                    'channel': self.channels[channel_key]['name'],
                    'status': 'error',
                    'error': str(e)
                }
        
        # Aggregate sentiment
        overall_risk = 0
        risk_count = 0
        
        for channel_key, data in results.items():
            if data.get('status') == 'success' and data.get('sentiment'):
                overall_risk += data['sentiment']['overall_risk']
                risk_count += 1
        
        avg_risk = overall_risk / risk_count if risk_count > 0 else 5
        
        return {
            'channels': results,
            'overall_risk': round(avg_risk, 1),
            'risk_level': 'CRITICAL' if avg_risk > 8 else 'HIGH' if avg_risk > 6 else 'MEDIUM' if avg_risk > 4 else 'LOW',
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }

if __name__ == "__main__":
    # Test the provider
    provider = YouTubeGeopoliticsProvider()
    
    print("Testing YouTube Geopolitics + Finance Provider...")
    print("="*60)
    
    # Test with mock data (since we don't have real video IDs yet)
    print("\n📺 CONFIGURED CHANNELS (9 Total):")
    
    # Group by category
    categories = {}
    for key, channel in provider.channels.items():
        cat = channel.get('category', 'other')
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(channel)
    
    for cat, channels in categories.items():
        print(f"\n🎯 {cat.upper()}:")
        for channel in channels:
            print(f"   • {channel['name']}")
            print(f"     Focus: {channel['focus']}")
            print(f"     Frequency: {channel['frequency']}")
            print(f"     Value: {'⭐' * channel['trading_value']}")
    
    print("\n" + "="*60)
    print("✅ YouTube Provider Ready with 9 Channels!")
    print("\n📊 COVERAGE:")
    print("   • Geopolitics: 2 channels")
    print("   • Macro/Finance: 4 channels")
    print("   • Strategy: 1 channel")
    print("   • Trading: 1 channel")
    print("   • Interviews: 1 channel")
    print("\n💡 Next Steps:")
    print("   1. Fetch latest videos from all channels")
    print("   2. Analyze transcripts for trading insights")
    print("   3. Aggregate sentiment across all experts")
    print("   4. Generate trading recommendations")

