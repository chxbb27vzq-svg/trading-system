# AI-Powered Trading System

## Overview
Comprehensive AI-powered trading system for €10,000 portfolio targeting €1M in 18-21 years through disciplined trading with 25-30% annual returns.

## Core Features

### 1. Master Trading Framework V3.0
- Expected Value (EV) calculations
- Multi-factor scoring system
- Risk management (max 5% loss per trade)
- Leverage optimization (3-4x)

### 2. Telegram Bot (24/7)
Real-time portfolio monitoring and analysis via Telegram:

**Portfolio & Analysis:**
- `/status` - Quick portfolio status
- `/portfolio` - Detailed portfolio breakdown
- `/gold` - Gold market analysis
- `/silver` - Silver market analysis
- `/bitcoin` - Bitcoin market analysis
- `/sp500` - S&P 500 market analysis
- `/oil` - Oil tactical trading analysis

**News & Intelligence:**
- `/news` - Geopolitical situation summary
- **`/facts`** - **Verified facts without propaganda** 🆕

**Learning & Performance:**
- **`/review`** - **Weekly performance review** 🆕
- **`/lessons`** - **Top lessons learned** 🆕
- **`/insights`** - **Key insights from knowledge base** 🆕

**Utilities:**
- `/alert` - Set price alerts
- `/help` - Command help

### 3. Propaganda Filter & Fact Extractor
Cross-verifies news from 10+ international sources:
- **Western sources**: Reuters, Bloomberg, BBC, AP
- **Eastern sources**: TASS, RT, CGTN
- **Neutral sources**: Al Jazeera, Swiss Info, Nikkei

**Features:**
- Cross-verification: Only events reported by BOTH sides
- Propaganda filtering: Removes emotional language and bias
- Confidence scoring: 1-10 based on source agreement
- Trading impact: Quantified effects on assets

### 4. Geopolitical Risk Analysis V2.0
Integrates 9 YouTube expert channels + 10 news sources:

**YouTube Experts:**
- Geopolitics: Glenn Diesen, Alexander Mercouris
- Macro/Finance: Raoul Pal, Jeff Snider, Lyn Alden, Steven Van Metre, George Gammon
- Trading: Luke Gromen
- Interviews: Adam Taggart

### 5. Teacher Agent System (Self-Learning)
Continuous learning and performance improvement system:

**Features:**
- **Knowledge Base**: SQLite database storing lessons, insights, strategies, and expert opinions
- **Performance Analysis**: Automatic weekly reviews with win rate, returns, and recommendations
- **Lesson Extraction**: Extracts patterns from successful and failed trades
- **Insight Generation**: Identifies high-level patterns across multiple lessons
- **Strategy Optimization**: Recommends adjustments based on performance data

**Current Knowledge:**
- 20 Lessons Learned (Gold, Bitcoin, Oil, Silver, S&P 500)
- 11 Key Insights (Geopolitics, Technical Analysis, Risk Management)
- 5 Active Trading Strategies
- 8 Expert Opinions
- 2 Performance Reviews

**Evolution Path:**
- Phase 1 (Current): Rule-based analysis, €0/month ✅
- Phase 2 (Future): Enhanced automation, €0/month
- Phase 3 (Optional): LLM-powered multi-agent, €20-50/month

See `TEACHER_AGENT_GUIDE.md` for complete documentation.

### 6. Real-Time Market Data
- TradingView (primary)
- yfinance (backup)
- Alpha Vantage (technical indicators)

## Portfolio Strategy

**Current Allocation (€10,000):**
- Gold: 18% (€1,800, 4x leverage)
- Bitcoin: 8% (€800, 3x leverage)
- Oil: 4% (€400, 12x leverage) - Tactical
- Cash: 70% (€7,000)

**Target Returns:**
- 25-30% annual returns
- €1 million in 18-21 years
- Maximum drawdown: 20%

## Assets Tracked
- **Gold (GC=F)** - Safe haven, 18% allocation, 4x leverage
- **Silver (SI=F)** - Industrial metal, currently avoided (topping pattern)
- **Bitcoin (BTC-USD)** - Digital safe haven, 8% allocation, 3x leverage
- **S&P 500 (^GSPC)** - Equities, 0-5% tactical allocation during high geopolitical risk
- **Brent Oil (BZ=F)** - Energy, 4% tactical allocation, 12x leverage

## Technical Stack
- **Language**: Python 3.11
- **Bot Framework**: python-telegram-bot (async)
- **Data Sources**: yfinance, TradingView, Alpha Vantage
- **Database**: SQLite
- **Version Control**: Git + GitHub
- **Key Libraries**: pandas, numpy, requests, asyncio

## Setup

### Prerequisites
```bash
pip install -r requirements.txt
```

### Configuration
1. Set Telegram Bot Token in `telegram_bot.py`
2. Configure API keys (Alpha Vantage, etc.)
3. Set authorized Telegram User ID

### Running the Bot
```bash
# Start Telegram bot
python3 telegram_bot.py

# Run in background
nohup python3 telegram_bot.py > bot.log 2>&1 &
```

### Testing Propaganda Filter
```bash
python3 data_providers/propaganda_filter.py
```

## GitHub Repository
https://github.com/chxbb27vzq-svg/trading-system

## Documentation
- `MILLIONEN_AKKUMULATION_GUIDE.md` - Complete wealth accumulation guide
- `PLAN_10K_START.md` - €10k to €1M roadmap
- `ASSET_UNIVERSE_RECOMMENDATIONS.md` - Asset analysis and recommendations

## Security
- Telegram bot restricted to single authorized user ID
- No public API endpoints
- Secure token management

## Cost
**Total: €0/month**
- All data sources: Free tier
- No paid APIs required
- Professional quality analysis

## License
Private use only

## Author
Trading System V3.0 - November 2025

