"""
Enhanced Trading System Telegram Bot
With Alpha Vantage + GDELT Integration
"""

import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import yfinance as yf
from datetime import datetime
import sys
sys.path.append('/home/ubuntu/trading_agents')

from data_providers.alpha_vantage_provider import AlphaVantageProvider, get_symbol
from data_providers.geopolitics_professional import ProfessionalGeopoliticsAnalyzer
from data_providers.hybrid_provider import HybridMarketProvider

# Bot configuration
BOT_TOKEN = "8305397344:AAER-Kpnczu6kPPC_5jfmHs7rKoZVAuAAHE"

class EnhancedTradingBot:
    def __init__(self, token):
        self.token = token
        self.app = Application.builder().token(token).build()
        self.alpha_vantage = AlphaVantageProvider()
        self.geopolitics = ProfessionalGeopoliticsAnalyzer()
        self.hybrid = HybridMarketProvider()  # NEW: Hybrid provider
        self.portfolio = {
            'gold': {'allocation': 0.18, 'leverage': 4, 'capital': 1800},
            'bitcoin': {'allocation': 0.08, 'leverage': 3, 'capital': 800},
            'cash': {'allocation': 0.74, 'leverage': 1, 'capital': 7400}
        }
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Welcome message"""
        await update.message.reply_text(
            "🤖 *Enhanced Trading Bot aktiviert!*\n\n"
            "✨ *NEU: Alpha Vantage + GDELT Integration!*\n\n"
            "📊 *Portfolio:*\n"
            "/status - Quick Status\n"
            "/portfolio - Detailliert\n\n"
            "📈 *Erweiterte Analyse:*\n"
            "/gold - Gold (mit RSI, MACD)\n"
            "/silver - Silver Analyse\n"
            "/bitcoin - Bitcoin (mit Indicators)\n\n"
            "🌍 *Geopolitik (NEU!):*\n"
            "/geopolitik - Risiko-Assessment\n"
            "/news - Aktuelle Lage\n\n"
            "/help - Alle Befehle",
            parse_mode='Markdown'
        )
    
    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Quick portfolio status with geopolitical context"""
        await update.message.reply_text("📊 Lade Daten...")
        
        try:
            # Get prices from hybrid provider
            gold_data = self.hybrid.get_gold_analysis()
            btc_data = self.hybrid.get_bitcoin_analysis()
            
            gold = gold_data['price'] if gold_data else 0
            btc = btc_data['price'] if btc_data else 0
            
            # Get geopolitical risk (quick)
            msg = "📊 *PORTFOLIO STATUS*\n\n"
            msg += f"💰 *Gold:* ${gold:,.2f}\n"
            msg += f"   Allokation: 18% (4x Leverage)\n\n"
            msg += f"₿ *Bitcoin:* ${btc:,.2f}\n"
            msg += f"   Allokation: 8% (3x Leverage)\n\n"
            msg += f"💵 *Cash:* 74%\n\n"
            msg += f"🕐 {datetime.now().strftime('%d.%m.%Y %H:%M')}\n\n"
            msg += f"💡 Nutze /geopolitik für Risiko-Assessment"
            
            await update.message.reply_text(msg, parse_mode='Markdown')
        except Exception as e:
            await update.message.reply_text(f"❌ Fehler: {str(e)}")
    
    async def gold_analysis(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Enhanced Gold analysis with Hybrid Provider"""
        await update.message.reply_text("💰 Analysiere Gold (TradingView + yfinance)...")
        
        try:
            # Get gold data from hybrid provider
            gold = self.hybrid.get_gold_analysis()
            
            if not gold:
                await update.message.reply_text("❌ Konnte Gold-Daten nicht abrufen")
                return
            
            msg = "💰 *GOLD ANALYSE*\n\n"
            msg += f"📈 Preis: ${gold['price']:,.2f}\n"
            msg += f"📊 24h: {gold['change_percent']:+.2f}%\n"
            msg += f"🔺 High: ${gold['high']:,.2f}\n"
            msg += f"🔻 Low: ${gold['low']:,.2f}\n\n"
            
            if gold.get('rsi'):
                msg += f"📊 *Technical Indicators:*\n"
                msg += f"   • RSI(14): {gold['rsi']:.1f}\n"
                
                if gold.get('macd'):
                    msg += f"   • MACD: {gold['macd']:.2f}\n"
                
                msg += f"   • TradingView: {gold['recommendation']}\n\n"
            
            msg += f"✅ *Empfehlung:* HOLD 18%\n"
            msg += f"🎯 Target: $4,200\n"
            msg += f"🛑 Stop: $3,850\n\n"
            msg += f"💾 Quelle: {gold['source']}"
            
            await update.message.reply_text(msg, parse_mode='Markdown')
        except Exception as e:
            await update.message.reply_text(f"❌ Fehler: {str(e)}")
    
    async def bitcoin_analysis(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Enhanced Bitcoin analysis with TradingView"""
        await update.message.reply_text("₿ Analysiere Bitcoin (TradingView)...")
        
        try:
            # Get bitcoin data from hybrid provider (TradingView)
            btc = self.hybrid.get_bitcoin_analysis()
            
            if not btc:
                await update.message.reply_text("❌ Konnte Bitcoin-Daten nicht abrufen")
                return
            
            msg = "₿ *BITCOIN ANALYSE*\n\n"
            msg += f"📈 Preis: ${btc['price']:,.2f}\n"
            msg += f"📊 24h: {btc['change_percent']:+.2f}%\n\n"
            
            if btc.get('rsi'):
                msg += f"📊 *Technical Indicators:*\n"
                msg += f"   • RSI(14): {btc['rsi']:.1f}\n"
                
                if btc.get('macd'):
                    msg += f"   • MACD: {btc['macd']:.2f}\n"
                
                if btc.get('ema_50'):
                    msg += f"   • EMA(50): ${btc['ema_50']:,.0f}\n"
                
                msg += f"   • TradingView: {btc['recommendation']}\n\n"
            
            msg += f"✅ *Empfehlung:* HOLD 8%\n"
            msg += f"🎯 Target: $118,000\n"
            msg += f"🛑 Stop: $103,000\n\n"
            msg += f"💾 Quelle: {btc['source']}"
            
            await update.message.reply_text(msg, parse_mode='Markdown')
        except Exception as e:
            await update.message.reply_text(f"❌ Fehler: {str(e)}")
    
    async def silver_analysis(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Silver analysis with warning (Hybrid Provider)"""
        await update.message.reply_text("🥈 Analysiere Silver...")
        
        try:
            # Get silver data from hybrid provider
            silver = self.hybrid.get_silver_analysis()
            
            if not silver:
                await update.message.reply_text("❌ Konnte Silver-Daten nicht abrufen")
                return
            
            msg = "🥈 *SILVER ANALYSE*\n\n"
            msg += f"📈 Preis: ${silver['price']:,.2f}\n"
            msg += f"📊 24h: {silver['change_percent']:+.2f}%\n\n"
            
            if silver.get('rsi'):
                msg += f"📊 RSI(14): {silver['rsi']:.1f}\n"
                msg += f"📊 TradingView: {silver['recommendation']}\n\n"
            
            msg += f"⚠️ *WARNUNG:* Topping Pattern!\n"
            msg += f"🔴 $49 = Historisches Resistance\n"
            msg += f"📉 EV: -1.32% (negativ!)\n\n"
            msg += f"❌ *Empfehlung:* NICHT KAUFEN\n"
            msg += f"⏳ Warten auf $42-45\n\n"
            msg += f"💾 Quelle: {silver['source']}"
            
            await update.message.reply_text(msg, parse_mode='Markdown')
        except Exception as e:
            await update.message.reply_text(f"❌ Fehler: {str(e)}")
    
    async def geopolitical_analysis(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Professional geopolitical analysis (YouTube + News)"""
        await update.message.reply_text(
            "🌍 Starte professionelle Geopolitik-Analyse...\n\n"
            "🎓 YouTube: Diesen, Mercouris, Gromen\n"
            "📰 News: 10 internationale Quellen\n"
            "⏱️ Dauert ~45 Sekunden..."
        )
        
        try:
            # Professional analysis
            current_portfolio = {'gold': 18, 'bitcoin': 8, 'cash': 74}
            analysis = self.geopolitics.get_comprehensive_analysis(current_portfolio)
            
            # Format for Telegram
            msg = self.geopolitics.format_for_telegram(analysis)
            
            await update.message.reply_text(msg, parse_mode='Markdown')
            
        except Exception as e:
            await update.message.reply_text(
                f"❌ Fehler: {str(e)}\n\n"
                f"Fallback auf manuelle Analyse..."
            )
            await self.news(update, context)
    
    async def news(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Manual geopolitical news (fallback)"""
        msg = "📰 *GEOPOLITISCHE LAGE*\n\n"
        msg += "⚠️ *NUKLEAR-SPANNUNGEN:* 9/10\n"
        msg += "   • Trump & Putin: Atomwaffentests\n"
        msg += "   • Höchste Eskalation seit Kaltem Krieg\n\n"
        msg += "🔴 *GAZA-KONFLIKT:* 7/10\n"
        msg += "   • 68,527+ Tote\n"
        msg += "   • Fragile Waffenruhe\n\n"
        msg += "🔴 *UKRAINE-KRIEG:* 6/10\n"
        msg += "   • Pokrovsk kurz vor Fall\n\n"
        msg += "💰 *FED POLITIK:*\n"
        msg += "   • 25bp Cut (hawkish)\n"
        msg += "   • Powell: 'Dezember unsicher'\n\n"
        msg += "✅ Safe Haven Demand unterstützt Gold/Bitcoin\n\n"
        msg += "💡 Nutze /geopolitik für GDELT-Analyse"
        
        await update.message.reply_text(msg, parse_mode='Markdown')
    
    async def portfolio(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Detailed portfolio"""
        try:
            gold = yf.Ticker("GC=F").history(period="1d")['Close'].iloc[-1]
            btc = yf.Ticker("BTC-USD").history(period="1d")['Close'].iloc[-1]
            
            capital = 10000
            gold_eur = 1800
            btc_eur = 800
            cash_eur = 7400
            
            gold_exposure = gold_eur * 4
            btc_exposure = btc_eur * 3
            total_exposure = gold_exposure + btc_exposure + cash_eur
            
            msg = "💼 *DETAILLIERTES PORTFOLIO*\n\n"
            msg += f"💰 Gesamtkapital: €{capital:,}\n\n"
            
            msg += f"🥇 *GOLD*\n"
            msg += f"   Preis: ${gold:,.2f}\n"
            msg += f"   Allokation: €{gold_eur:,} (18%)\n"
            msg += f"   Leverage: 4x\n"
            msg += f"   Exposure: €{gold_exposure:,}\n\n"
            
            msg += f"₿ *BITCOIN*\n"
            msg += f"   Preis: ${btc:,.2f}\n"
            msg += f"   Allokation: €{btc_eur:,} (8%)\n"
            msg += f"   Leverage: 3x\n"
            msg += f"   Exposure: €{btc_exposure:,}\n\n"
            
            msg += f"💵 *CASH:* €{cash_eur:,} (74%)\n\n"
            
            msg += f"📊 Total Exposure: €{total_exposure:,}\n"
            msg += f"📈 Portfolio Leverage: {total_exposure/capital:.2f}x\n\n"
            msg += f"🛡️ Status: Defensive Positionierung"
            
            await update.message.reply_text(msg, parse_mode='Markdown')
        except Exception as e:
            await update.message.reply_text(f"❌ Fehler: {str(e)}")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Help message"""
        msg = "🤖 *ENHANCED TRADING BOT*\n\n"
        msg += "✨ *NEU:*\n"
        msg += "• Alpha Vantage Integration\n"
        msg += "• GDELT Geopolitik-Tracking\n"
        msg += "• Technical Indicators (RSI, MACD)\n\n"
        msg += "📊 *PORTFOLIO:*\n"
        msg += "/status - Quick Status\n"
        msg += "/portfolio - Detailliert\n\n"
        msg += "📈 *ANALYSE:*\n"
        msg += "/gold - Gold (mit Indicators)\n"
        msg += "/silver - Silver Warnung\n"
        msg += "/bitcoin - Bitcoin Analyse\n\n"
        msg += "🌍 *GEOPOLITIK:*\n"
        msg += "/geopolitik - GDELT Risk Assessment\n"
        msg += "/news - Manuelle Übersicht\n\n"
        msg += "💡 *EMPFEHLUNGEN:*\n"
        msg += "• Gold: HOLD 18%\n"
        msg += "• Silver: NICHT KAUFEN!\n"
        msg += "• Bitcoin: HOLD 8%\n"
        msg += "• Cash: 74%"
        
        await update.message.reply_text(msg, parse_mode='Markdown')
    
    def setup_handlers(self):
        """Setup command handlers"""
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("status", self.status))
        self.app.add_handler(CommandHandler("gold", self.gold_analysis))
        self.app.add_handler(CommandHandler("silver", self.silver_analysis))
        self.app.add_handler(CommandHandler("bitcoin", self.bitcoin_analysis))
        self.app.add_handler(CommandHandler("geopolitik", self.geopolitical_analysis))
        self.app.add_handler(CommandHandler("news", self.news))
        self.app.add_handler(CommandHandler("portfolio", self.portfolio))
        self.app.add_handler(CommandHandler("help", self.help_command))
    
    def run(self):
        """Start the bot"""
        self.setup_handlers()
        print("🤖 Enhanced Telegram Bot gestartet!")
        print("✨ Alpha Vantage + GDELT aktiviert!")
        print("📱 Bot ist bereit...")
        self.app.run_polling()

if __name__ == "__main__":
    bot = EnhancedTradingBot(BOT_TOKEN)
    bot.run()

