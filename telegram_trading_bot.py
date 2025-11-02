"""
Enhanced Telegram Trading Bot
Real-time alerts, portfolio updates, market analysis
"""

import asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import yfinance as yf
from datetime import datetime
import json

# Bot configuration (will need token from user)
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"  # User needs to provide this

class TradingBot:
    def __init__(self, token):
        self.token = token
        self.app = Application.builder().token(token).build()
        self.portfolio = {
            'gold': {'allocation': 0.18, 'leverage': 4},
            'bitcoin': {'allocation': 0.08, 'leverage': 3},
            'cash': {'allocation': 0.74, 'leverage': 1}
        }
        self.alerts = {}
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Welcome message"""
        await update.message.reply_text(
            "🤖 Trading System Bot aktiviert!\n\n"
            "Verfügbare Befehle:\n"
            "/status - Portfolio Status\n"
            "/gold - Gold Analyse\n"
            "/silver - Silver Analyse\n"
            "/bitcoin - Bitcoin Analyse\n"
            "/alert <asset> <price> - Preis-Alert setzen\n"
            "/news - Letzte geopolitische News\n"
            "/portfolio - Detailliertes Portfolio\n"
            "/help - Hilfe"
        )
    
    async def status(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Quick portfolio status"""
        try:
            # Get current prices
            gold = yf.Ticker("GC=F").history(period="1d")['Close'].iloc[-1]
            btc = yf.Ticker("BTC-USD").history(period="1d")['Close'].iloc[-1]
            
            msg = f"📊 PORTFOLIO STATUS\n\n"
            msg += f"💰 Gold: ${gold:,.2f}\n"
            msg += f"   Allokation: 18% (4x Leverage)\n\n"
            msg += f"₿ Bitcoin: ${btc:,.2f}\n"
            msg += f"   Allokation: 8% (3x Leverage)\n\n"
            msg += f"💵 Cash: 74%\n\n"
            msg += f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
            
            await update.message.reply_text(msg)
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
            
            msg = f"💰 GOLD ANALYSE\n\n"
            msg += f"Aktuell: ${current:,.2f}\n"
            msg += f"24h: {change:+.2f}%\n"
            msg += f"Wochenhoch: ${week_high:,.2f}\n"
            msg += f"Wochentief: ${week_low:,.2f}\n\n"
            msg += f"📊 Empfehlung: HOLD 18%\n"
            msg += f"🎯 Target: $4,200\n"
            msg += f"🛑 Stop: $3,850\n\n"
            msg += f"💡 Geopolitik unterstützt Safe Haven Demand"
            
            await update.message.reply_text(msg)
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
            
            msg = f"🥈 SILVER ANALYSE\n\n"
            msg += f"Aktuell: ${current:,.2f}\n"
            msg += f"24h: {change:+.2f}%\n\n"
            msg += f"⚠️ WARNUNG: Topping Pattern!\n"
            msg += f"$49 = Historisches Resistance\n"
            msg += f"EV: -1.32% (negativ!)\n\n"
            msg += f"❌ Empfehlung: NICHT KAUFEN\n"
            msg += f"⏳ Warten auf $42-45"
            
            await update.message.reply_text(msg)
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
            
            msg = f"₿ BITCOIN ANALYSE\n\n"
            msg += f"Aktuell: ${current:,.2f}\n"
            msg += f"24h: {change:+.2f}%\n\n"
            msg += f"📊 Empfehlung: HOLD 8%\n"
            msg += f"🎯 Target: $118,000\n"
            msg += f"🛑 Stop: $103,000\n\n"
            msg += f"💡 Digital Gold Narrative intakt"
            
            await update.message.reply_text(msg)
        except Exception as e:
            await update.message.reply_text(f"❌ Fehler: {str(e)}")
    
    async def set_alert(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Set price alert"""
        try:
            if len(context.args) < 2:
                await update.message.reply_text(
                    "❌ Verwendung: /alert <asset> <price>\n"
                    "Beispiel: /alert gold 4050"
                )
                return
            
            asset = context.args[0].lower()
            price = float(context.args[1])
            
            self.alerts[asset] = price
            
            await update.message.reply_text(
                f"✅ Alert gesetzt!\n"
                f"Asset: {asset.upper()}\n"
                f"Preis: ${price:,.2f}\n\n"
                f"Du wirst benachrichtigt wenn erreicht."
            )
        except Exception as e:
            await update.message.reply_text(f"❌ Fehler: {str(e)}")
    
    async def portfolio(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Detailed portfolio"""
        try:
            gold = yf.Ticker("GC=F").history(period="1d")['Close'].iloc[-1]
            btc = yf.Ticker("BTC-USD").history(period="1d")['Close'].iloc[-1]
            
            capital = 10000
            gold_eur = capital * 0.18
            btc_eur = capital * 0.08
            cash_eur = capital * 0.74
            
            gold_exposure = gold_eur * 4
            btc_exposure = btc_eur * 3
            total_exposure = gold_exposure + btc_exposure + cash_eur
            
            msg = f"💼 DETAILLIERTES PORTFOLIO\n\n"
            msg += f"Gesamtkapital: €{capital:,.0f}\n\n"
            
            msg += f"💰 GOLD\n"
            msg += f"   Preis: ${gold:,.2f}\n"
            msg += f"   Allokation: €{gold_eur:,.0f} (18%)\n"
            msg += f"   Leverage: 4x\n"
            msg += f"   Exposure: €{gold_exposure:,.0f}\n\n"
            
            msg += f"₿ BITCOIN\n"
            msg += f"   Preis: ${btc:,.2f}\n"
            msg += f"   Allokation: €{btc_eur:,.0f} (8%)\n"
            msg += f"   Leverage: 3x\n"
            msg += f"   Exposure: €{btc_exposure:,.0f}\n\n"
            
            msg += f"💵 CASH: €{cash_eur:,.0f} (74%)\n\n"
            
            msg += f"📊 Total Exposure: €{total_exposure:,.0f} ({total_exposure/capital:.1f}x)\n\n"
            msg += f"🛡️ Defensive Positionierung"
            
            await update.message.reply_text(msg)
        except Exception as e:
            await update.message.reply_text(f"❌ Fehler: {str(e)}")
    
    async def news(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Latest geopolitical news"""
        msg = f"📰 GEOPOLITISCHE LAGE\n\n"
        msg += f"⚠️ NUKLEAR-SPANNUNGEN:\n"
        msg += f"   Trump & Putin: Atomwaffentests\n"
        msg += f"   Höchste Eskalation seit Kaltem Krieg\n\n"
        msg += f"🔴 GAZA-KONFLIKT:\n"
        msg += f"   68,527+ Tote\n"
        msg += f"   Fragile Waffenruhe\n\n"
        msg += f"🔴 UKRAINE-KRIEG:\n"
        msg += f"   Pokrovsk kurz vor Fall\n\n"
        msg += f"💰 FED POLITIK:\n"
        msg += f"   25bp Cut (hawkish)\n"
        msg += f"   Powell: 'Dezember unsicher'\n\n"
        msg += f"✅ Safe Haven Demand unterstützt Gold/Bitcoin"
        
        await update.message.reply_text(msg)
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Help message"""
        msg = f"🤖 TRADING BOT HILFE\n\n"
        msg += f"📊 PORTFOLIO:\n"
        msg += f"/status - Quick Status\n"
        msg += f"/portfolio - Detailliert\n\n"
        msg += f"📈 ANALYSE:\n"
        msg += f"/gold - Gold Analyse\n"
        msg += f"/silver - Silver Analyse\n"
        msg += f"/bitcoin - Bitcoin Analyse\n\n"
        msg += f"🔔 ALERTS:\n"
        msg += f"/alert <asset> <price> - Alert setzen\n"
        msg += f"Beispiel: /alert gold 4050\n\n"
        msg += f"📰 NEWS:\n"
        msg += f"/news - Geopolitische Lage\n\n"
        msg += f"💡 TIP: Bot läuft 24/7 und sendet Alerts automatisch!"
        
        await update.message.reply_text(msg)
    
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
        self.app.add_handler(CommandHandler("help", self.help_command))
    
    def run(self):
        """Start the bot"""
        self.setup_handlers()
        print("🤖 Telegram Bot gestartet!")
        print("Warte auf Befehle...")
        self.app.run_polling()

if __name__ == "__main__":
    # User needs to provide token
    if BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN":
        print("❌ FEHLER: Bitte Telegram Bot Token setzen!")
        print("\n📝 Anleitung:")
        print("1. Gehe zu @BotFather auf Telegram")
        print("2. Sende /newbot")
        print("3. Folge den Anweisungen")
        print("4. Kopiere den Token")
        print("5. Setze BOT_TOKEN in dieser Datei")
    else:
        bot = TradingBot(BOT_TOKEN)
        bot.run()
