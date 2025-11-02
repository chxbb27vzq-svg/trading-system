"""
Trading System Telegram Bot
Real-time alerts, portfolio updates, market analysis
"""

import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import yfinance as yf
from datetime import datetime
import sys
import os

# Add data_providers to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'data_providers'))
from propaganda_filter import PropagandaFilter

# Bot configuration
BOT_TOKEN = "8305397344:AAER-Kpnczu6kPPC_5jfmHs7rKoZVAuAAHE"

class TradingBot:
    def __init__(self, token):
        self.token = token
        self.app = Application.builder().token(token).build()
        self.portfolio = {
            'gold': {'allocation': 0.18, 'leverage': 4, 'capital': 1800},
            'bitcoin': {'allocation': 0.08, 'leverage': 3, 'capital': 800},
            'cash': {'allocation': 0.74, 'leverage': 1, 'capital': 7400}
        }
        self.alerts = {}
        self.propaganda_filter = PropagandaFilter()
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Welcome message"""
        await update.message.reply_text(
            "🤖 *Trading System Bot aktiviert!*\n\n"
            "📊 *Verfügbare Befehle:*\n"
            "/status - Portfolio Status\n"
            "/gold - Gold Analyse\n"
            "/silver - Silver Analyse\n"
            "/bitcoin - Bitcoin Analyse\n"
            "/alert <asset> <price> - Preis-Alert\n"
            "/news - Geopolitische Lage\n"
            "/facts - Verifizierte Fakten (Propaganda-frei)\n"
            "/portfolio - Detailliertes Portfolio\n"
            "/help - Hilfe\n\n"
            "💡 Tipp: Starte mit /status!",
            parse_mode='Markdown'
        )
    
    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Quick portfolio status"""
        try:
            # Get current prices
            gold = yf.Ticker("GC=F").history(period="1d")['Close'].iloc[-1]
            btc = yf.Ticker("BTC-USD").history(period="1d")['Close'].iloc[-1]
            
            msg = "📊 *PORTFOLIO STATUS*\n\n"
            msg += f"💰 *Gold:* ${gold:,.2f}\n"
            msg += f"   Allokation: 18% (4x Leverage)\n"
            msg += f"   Kapital: €1,800\n\n"
            msg += f"₿ *Bitcoin:* ${btc:,.2f}\n"
            msg += f"   Allokation: 8% (3x Leverage)\n"
            msg += f"   Kapital: €800\n\n"
            msg += f"💵 *Cash:* 74% (€7,400)\n\n"
            msg += f"🕐 {datetime.now().strftime('%d.%m.%Y %H:%M')}"
            
            await update.message.reply_text(msg, parse_mode='Markdown')
        except Exception as e:
            await update.message.reply_text(f"❌ Fehler: {str(e)}")
    
    async def gold_analysis(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Gold market analysis"""
        try:
            ticker = yf.Ticker("GC=F")
            hist = ticker.history(period="5d")
            current = hist['Close'].iloc[-1]
            prev = hist['Close'].iloc[-2]
            change = ((current - prev) / prev) * 100
            
            week_high = hist['High'].max()
            week_low = hist['Low'].min()
            
            msg = "💰 *GOLD ANALYSE*\n\n"
            msg += f"📈 Aktuell: ${current:,.2f}\n"
            msg += f"📊 24h: {change:+.2f}%\n"
            msg += f"⬆️ Wochenhoch: ${week_high:,.2f}\n"
            msg += f"⬇️ Wochentief: ${week_low:,.2f}\n\n"
            msg += f"✅ *Empfehlung:* HOLD 18%\n"
            msg += f"🎯 Target: $4,200\n"
            msg += f"🛑 Stop-Loss: $3,850\n\n"
            msg += f"💡 Geopolitik unterstützt Safe Haven Demand\n"
            msg += f"📊 EV: +0.58% (unter Threshold, aber OK)"
            
            await update.message.reply_text(msg, parse_mode='Markdown')
        except Exception as e:
            await update.message.reply_text(f"❌ Fehler: {str(e)}")
    
    async def silver_analysis(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Silver market analysis"""
        try:
            ticker = yf.Ticker("SI=F")
            hist = ticker.history(period="5d")
            current = hist['Close'].iloc[-1]
            prev = hist['Close'].iloc[-2]
            change = ((current - prev) / prev) * 100
            
            msg = "🥈 *SILVER ANALYSE*\n\n"
            msg += f"📈 Aktuell: ${current:,.2f}\n"
            msg += f"📊 24h: {change:+.2f}%\n\n"
            msg += f"⚠️ *WARNUNG:* Topping Pattern!\n"
            msg += f"🔴 $49 = Historisches Resistance\n"
            msg += f"📉 EV: -1.32% (negativ!)\n\n"
            msg += f"❌ *Empfehlung:* NICHT KAUFEN\n"
            msg += f"⏳ Warten auf $42-45\n\n"
            msg += f"💡 2011 Parallele: $49 → $26 Crash\n"
            msg += f"📊 Crash-Risiko: 60%"
            
            await update.message.reply_text(msg, parse_mode='Markdown')
        except Exception as e:
            await update.message.reply_text(f"❌ Fehler: {str(e)}")
    
    async def bitcoin_analysis(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Bitcoin market analysis"""
        try:
            ticker = yf.Ticker("BTC-USD")
            hist = ticker.history(period="5d")
            current = hist['Close'].iloc[-1]
            prev = hist['Close'].iloc[-2]
            change = ((current - prev) / prev) * 100
            
            week_high = hist['High'].max()
            week_low = hist['Low'].min()
            
            msg = "₿ *BITCOIN ANALYSE*\n\n"
            msg += f"📈 Aktuell: ${current:,.2f}\n"
            msg += f"📊 24h: {change:+.2f}%\n"
            msg += f"⬆️ Wochenhoch: ${week_high:,.2f}\n"
            msg += f"⬇️ Wochentief: ${week_low:,.2f}\n\n"
            msg += f"✅ *Empfehlung:* HOLD 8%\n"
            msg += f"🎯 Target: $118,000\n"
            msg += f"🛑 Stop-Loss: $103,000\n\n"
            msg += f"💡 Digital Gold Narrative intakt\n"
            msg += f"📊 EV: +0.50% (leicht positiv)"
            
            await update.message.reply_text(msg, parse_mode='Markdown')
        except Exception as e:
            await update.message.reply_text(f"❌ Fehler: {str(e)}")
    
    async def set_alert(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Set price alert"""
        try:
            if len(context.args) < 2:
                await update.message.reply_text(
                    "❌ *Verwendung:*\n"
                    "`/alert <asset> <price>`\n\n"
                    "*Beispiele:*\n"
                    "`/alert gold 4050`\n"
                    "`/alert bitcoin 115000`\n"
                    "`/alert silver 45`",
                    parse_mode='Markdown'
                )
                return
            
            asset = context.args[0].lower()
            price = float(context.args[1])
            
            self.alerts[asset] = price
            
            await update.message.reply_text(
                f"✅ *Alert gesetzt!*\n\n"
                f"Asset: {asset.upper()}\n"
                f"Preis: ${price:,.2f}\n\n"
                f"💡 Du wirst benachrichtigt wenn erreicht.\n"
                f"(Feature wird noch implementiert)",
                parse_mode='Markdown'
            )
        except Exception as e:
            await update.message.reply_text(f"❌ Fehler: {str(e)}")
    
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
    
    async def news(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Latest geopolitical news"""
        msg = "📰 *GEOPOLITISCHE LAGE*\n\n"
        msg += "⚠️ *NUKLEAR-SPANNUNGEN:*\n"
        msg += "   • Trump & Putin: Atomwaffentests\n"
        msg += "   • Höchste Eskalation seit Kaltem Krieg\n\n"
        msg += "🔴 *GAZA-KONFLIKT:*\n"
        msg += "   • 68,527+ Tote\n"
        msg += "   • Fragile Waffenruhe\n\n"
        msg += "🔴 *UKRAINE-KRIEG:*\n"
        msg += "   • Pokrovsk kurz vor Fall\n"
        msg += "   • Russland nutzt verbotene Raketen\n\n"
        msg += "💰 *FED POLITIK:*\n"
        msg += "   • 25bp Cut (hawkish)\n"
        msg += "   • Powell: 'Dezember unsicher'\n\n"
        msg += "✅ Safe Haven Demand unterstützt Gold/Bitcoin"
        
        await update.message.reply_text(msg, parse_mode='Markdown')
    
    async def facts(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Verified facts without propaganda"""
        try:
            # Get verified facts from propaganda filter
            analysis = self.propaganda_filter.get_trading_relevant_facts()
            
            if analysis['status'] == 'success':
                msg = self.propaganda_filter.format_for_telegram(analysis)
                await update.message.reply_text(msg, parse_mode='Markdown')
            else:
                await update.message.reply_text(
                    "❌ Fehler beim Laden der verifizierten Fakten.",
                    parse_mode='Markdown'
                )
        except Exception as e:
            await update.message.reply_text(f"❌ Fehler: {str(e)}")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Help message"""
        msg = "🤖 *TRADING BOT HILFE*\n\n"
        msg += "📊 *PORTFOLIO:*\n"
        msg += "/status - Quick Status\n"
        msg += "/portfolio - Detailliert\n\n"
        msg += "📈 *ANALYSE:*\n"
        msg += "/gold - Gold Analyse\n"
        msg += "/silver - Silver Analyse\n"
        msg += "/bitcoin - Bitcoin Analyse\n\n"
        msg += "🔔 *ALERTS:*\n"
        msg += "/alert <asset> <price>\n"
        msg += "Beispiel: `/alert gold 4050`\n\n"
        msg += "📰 *NEWS:*\n"
        msg += "/news - Geopolitische Lage\n"
        msg += "/facts - Verifizierte Fakten (Propaganda-frei)\n\n"
        msg += "💡 *EMPFEHLUNGEN (31. Okt):*\n"
        msg += "• Gold: HOLD 18%\n"
        msg += "• Silver: NICHT KAUFEN (Topping!)\n"
        msg += "• Bitcoin: HOLD 8%\n"
        msg += "• Cash: 74% (defensiv)\n\n"
        msg += "🚀 Bot läuft 24/7!"
        
        await update.message.reply_text(msg, parse_mode='Markdown')
    
    def setup_handlers(self):
        """Setup command handlers"""
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("status", self.status))
        self.app.add_handler(CommandHandler("gold", self.gold_analysis))
        self.app.add_handler(CommandHandler("silver", self.silver_analysis))
        self.app.add_handler(CommandHandler("bitcoin", self.bitcoin_analysis))
        self.app.add_handler(CommandHandler("alert", self.set_alert))
        self.app.add_handler(CommandHandler("portfolio", self.portfolio))
        self.app.add_handler(CommandHandler("news", self.news))
        self.app.add_handler(CommandHandler("facts", self.facts))
        self.app.add_handler(CommandHandler("help", self.help_command))
    
    def run(self):
        """Start the bot"""
        self.setup_handlers()
        print("🤖 Telegram Bot gestartet!")
        print("📱 Bot ist bereit für Befehle...")
        print("💡 Sende /start an deinen Bot um zu beginnen!")
        self.app.run_polling()

if __name__ == "__main__":
    bot = TradingBot(BOT_TOKEN)
    bot.run()

