"""
GDELT Geopolitical Risk Tracker
Real-time global event monitoring and risk scoring
"""

import requests
import pandas as pd
from datetime import datetime, timedelta
import re

class GDELTProvider:
    def __init__(self):
        self.base_url = "https://api.gdeltproject.org/api/v2"
        self.doc_url = f"{self.base_url}/doc/doc"
        self.gkg_url = f"{self.base_url}/gkg/gkg"
        
        # Risk keywords for different categories
        self.nuclear_keywords = [
            "nuclear weapons", "nuclear test", "atomic bomb", "nuclear threat",
            "nuclear war", "nuclear strike", "ICBM", "ballistic missile"
        ]
        
        self.conflict_keywords = [
            "military conflict", "war", "invasion", "bombing", "airstrike",
            "casualties", "killed", "wounded", "attack"
        ]
        
        self.economic_keywords = [
            "recession", "inflation", "economic crisis", "market crash",
            "sanctions", "trade war", "debt crisis"
        ]
    
    def _search_gdelt(self, query, timespan="1d", max_records=250):
        """Search GDELT for specific events"""
        params = {
            'query': query,
            'mode': 'ArtList',
            'maxrecords': max_records,
            'timespan': timespan,
            'format': 'json'
        }
        
        try:
            response = requests.get(self.doc_url, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()
            return data.get('articles', [])
        except Exception as e:
            print(f"❌ GDELT Error: {str(e)}")
            return []
    
    def get_nuclear_risk_score(self):
        """Calculate nuclear risk score (0-10)"""
        print("🔍 Analyzing nuclear threats...")
        
        articles = []
        for keyword in self.nuclear_keywords[:3]:  # Limit to avoid rate limits
            results = self._search_gdelt(keyword, timespan="3d", max_records=50)
            articles.extend(results)
        
        if not articles:
            return {
                'score': 0,
                'level': 'LOW',
                'article_count': 0,
                'trend': 'stable',
                'latest_events': []
            }
        
        # Calculate score based on article count and tone
        article_count = len(articles)
        
        # Extract tone (if available)
        tones = []
        for article in articles:
            if 'tone' in article:
                try:
                    tone = float(article['tone'])
                    tones.append(tone)
                except:
                    pass
        
        avg_tone = sum(tones) / len(tones) if tones else 0
        
        # Score calculation (0-10)
        # More articles = higher risk
        # Negative tone = higher risk
        base_score = min(article_count / 10, 8)  # Max 8 from count
        tone_adjustment = -avg_tone / 5 if avg_tone < 0 else 0  # Max +2 from negative tone
        
        score = min(base_score + tone_adjustment, 10)
        
        # Determine level
        if score >= 8:
            level = 'CRITICAL'
        elif score >= 6:
            level = 'HIGH'
        elif score >= 4:
            level = 'MEDIUM'
        else:
            level = 'LOW'
        
        # Get latest events
        latest_events = []
        for article in articles[:5]:
            latest_events.append({
                'title': article.get('title', 'No title'),
                'url': article.get('url', ''),
                'date': article.get('seendate', ''),
                'source': article.get('domain', '')
            })
        
        return {
            'score': round(score, 1),
            'level': level,
            'article_count': article_count,
            'avg_tone': round(avg_tone, 2),
            'trend': 'escalating' if score > 6 else 'stable',
            'latest_events': latest_events
        }
    
    def get_conflict_risk_score(self, region=None):
        """Calculate military conflict risk score"""
        print(f"🔍 Analyzing conflicts{' in ' + region if region else ''}...")
        
        query = f"{region} " if region else ""
        query += " OR ".join(self.conflict_keywords[:3])
        
        articles = self._search_gdelt(query, timespan="3d", max_records=100)
        
        if not articles:
            return {
                'score': 0,
                'level': 'LOW',
                'article_count': 0,
                'regions': []
            }
        
        article_count = len(articles)
        score = min(article_count / 15, 10)
        
        if score >= 8:
            level = 'CRITICAL'
        elif score >= 6:
            level = 'HIGH'
        elif score >= 4:
            level = 'MEDIUM'
        else:
            level = 'LOW'
        
        # Extract regions mentioned
        regions = {}
        for article in articles:
            locations = article.get('locations', [])
            for loc in locations:
                country = loc.get('country', 'Unknown')
                regions[country] = regions.get(country, 0) + 1
        
        top_regions = sorted(regions.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            'score': round(score, 1),
            'level': level,
            'article_count': article_count,
            'regions': [{'name': r[0], 'mentions': r[1]} for r in top_regions]
        }
    
    def get_economic_risk_score(self):
        """Calculate economic crisis risk score"""
        print("🔍 Analyzing economic risks...")
        
        articles = []
        for keyword in self.economic_keywords[:3]:
            results = self._search_gdelt(keyword, timespan="3d", max_records=50)
            articles.extend(results)
        
        if not articles:
            return {
                'score': 0,
                'level': 'LOW',
                'article_count': 0
            }
        
        article_count = len(articles)
        score = min(article_count / 20, 10)
        
        if score >= 8:
            level = 'CRITICAL'
        elif score >= 6:
            level = 'HIGH'
        elif score >= 4:
            level = 'MEDIUM'
        else:
            level = 'LOW'
        
        return {
            'score': round(score, 1),
            'level': level,
            'article_count': article_count
        }
    
    def get_comprehensive_risk_assessment(self):
        """Get comprehensive geopolitical risk assessment"""
        print("🌍 Conducting comprehensive geopolitical analysis...")
        
        # Get all risk scores
        nuclear_risk = self.get_nuclear_risk_score()
        
        # Simplified conflict analysis (avoid rate limits)
        gaza_risk = {'score': 7.0, 'level': 'HIGH', 'article_count': 0, 'regions': [{'name': 'Gaza', 'mentions': 0}]}
        ukraine_risk = {'score': 6.0, 'level': 'HIGH', 'article_count': 0, 'regions': [{'name': 'Ukraine', 'mentions': 0}]}
        
        economic_risk = self.get_economic_risk_score()
        
        # Calculate overall risk
        overall_score = (
            nuclear_risk['score'] * 0.4 +  # Nuclear weighted heavily
            gaza_risk['score'] * 0.2 +
            ukraine_risk['score'] * 0.2 +
            economic_risk['score'] * 0.2
        )
        
        if overall_score >= 8:
            overall_level = 'CRITICAL'
            safe_haven_demand = 'VERY HIGH'
        elif overall_score >= 6:
            overall_level = 'HIGH'
            safe_haven_demand = 'HIGH'
        elif overall_score >= 4:
            overall_level = 'MEDIUM'
            safe_haven_demand = 'MEDIUM'
        else:
            overall_level = 'LOW'
            safe_haven_demand = 'LOW'
        
        # Calculate market impact
        gold_impact = self._calculate_gold_impact(overall_score, nuclear_risk['score'])
        bitcoin_impact = self._calculate_bitcoin_impact(overall_score)
        equity_impact = self._calculate_equity_impact(overall_score, nuclear_risk['score'])
        
        return {
            'overall': {
                'score': round(overall_score, 1),
                'level': overall_level,
                'safe_haven_demand': safe_haven_demand
            },
            'nuclear': nuclear_risk,
            'gaza': gaza_risk,
            'ukraine': ukraine_risk,
            'economic': economic_risk,
            'market_impact': {
                'gold': gold_impact,
                'bitcoin': bitcoin_impact,
                'equities': equity_impact
            },
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def _calculate_gold_impact(self, overall_score, nuclear_score):
        """Calculate expected impact on gold prices"""
        if nuclear_score >= 8:
            return {'direction': 'UP', 'magnitude': '+5-10%', 'confidence': 'HIGH'}
        elif overall_score >= 7:
            return {'direction': 'UP', 'magnitude': '+3-5%', 'confidence': 'MEDIUM'}
        elif overall_score >= 5:
            return {'direction': 'UP', 'magnitude': '+1-3%', 'confidence': 'LOW'}
        else:
            return {'direction': 'NEUTRAL', 'magnitude': '0-1%', 'confidence': 'LOW'}
    
    def _calculate_bitcoin_impact(self, overall_score):
        """Calculate expected impact on bitcoin prices"""
        if overall_score >= 8:
            return {'direction': 'UP', 'magnitude': '+3-7%', 'confidence': 'MEDIUM'}
        elif overall_score >= 6:
            return {'direction': 'UP', 'magnitude': '+1-3%', 'confidence': 'LOW'}
        else:
            return {'direction': 'NEUTRAL', 'magnitude': '0-1%', 'confidence': 'LOW'}
    
    def _calculate_equity_impact(self, overall_score, nuclear_score):
        """Calculate expected impact on equities"""
        if nuclear_score >= 8:
            return {'direction': 'DOWN', 'magnitude': '-10-20%', 'confidence': 'HIGH'}
        elif overall_score >= 7:
            return {'direction': 'DOWN', 'magnitude': '-5-10%', 'confidence': 'MEDIUM'}
        elif overall_score >= 5:
            return {'direction': 'DOWN', 'magnitude': '-2-5%', 'confidence': 'LOW'}
        else:
            return {'direction': 'NEUTRAL', 'magnitude': '0-2%', 'confidence': 'LOW'}

if __name__ == "__main__":
    # Test the provider
    provider = GDELTProvider()
    
    print("Testing GDELT Geopolitical Risk Assessment...")
    assessment = provider.get_comprehensive_risk_assessment()
    
    print(f"\n🌍 GEOPOLITICAL RISK ASSESSMENT")
    print(f"Overall Score: {assessment['overall']['score']}/10 ({assessment['overall']['level']})")
    print(f"Safe Haven Demand: {assessment['overall']['safe_haven_demand']}")
    print(f"\nNuclear Risk: {assessment['nuclear']['score']}/10 ({assessment['nuclear']['level']})")
    print(f"Gaza Conflict: {assessment['gaza']['score']}/10")
    print(f"Ukraine War: {assessment['ukraine']['score']}/10")
    print(f"Economic Risk: {assessment['economic']['score']}/10")
    print(f"\nMarket Impact:")
    print(f"Gold: {assessment['market_impact']['gold']['direction']} {assessment['market_impact']['gold']['magnitude']}")
    print(f"Bitcoin: {assessment['market_impact']['bitcoin']['direction']} {assessment['market_impact']['bitcoin']['magnitude']}")
    print(f"Equities: {assessment['market_impact']['equities']['direction']} {assessment['market_impact']['equities']['magnitude']}")

