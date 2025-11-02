# 🚀 TRADING SYSTEM - SETUP GUIDE

**Enhanced mit Alpha Vantage + GDELT Integration**

---

## ✅ WAS IST INSTALLIERT

### 1. **GITHUB REPOSITORY**
- URL: https://github.com/chxbb27vzq-svg/trading-system
- 24 Files, 8,000+ Zeilen Code
- Vollständiges Backup aller Analysen und Module

### 2. **TELEGRAM BOT** 🤖
- Token: `8305397344:AAER-Kpnczu6kPPC_5jfmHs7rKoZVAuAAHE`
- Status: ✅ AKTIV (läuft 24/7)
- Enhanced Version mit Alpha Vantage + GDELT

### 3. **ALPHA VANTAGE API** 📊
- API Key: `6POZJ38W61I4MR9H`
- Limit: 25 calls/Tag (kostenlos)
- Features: RSI, MACD, EMA, Bollinger Bands

### 4. **GDELT PROJECT** 🌍
- Kostenlos & Unbegrenzt
- Geopolitische Risiko-Scores
- Real-time Event Tracking

---

## 📱 TELEGRAM BOT BEFEHLE

### **PORTFOLIO:**
- `/start` - Bot aktivieren
- `/status` - Quick Portfolio Status
- `/portfolio` - Detailliertes Portfolio

### **ANALYSE (Enhanced):**
- `/gold` - Gold mit RSI, MACD, EMA
- `/silver` - Silver Warnung (Topping Pattern!)
- `/bitcoin` - Bitcoin Analyse

### **GEOPOLITIK (NEU!):**
- `/geopolitik` - GDELT Risk Assessment (30 Sek)
  - Nuklear-Risiko Score (0-10)
  - Konflikt-Tracking (Gaza, Ukraine)
  - Markt-Impact (Gold, Bitcoin, Equities)
- `/news` - Manuelle Übersicht (schnell)

### **HILFE:**
- `/help` - Alle Befehle anzeigen

---

## 🎯 BEISPIEL-SESSION

```
Sie: /start
Bot: 🤖 Enhanced Trading Bot aktiviert!
     ✨ NEU: Alpha Vantage + GDELT Integration!

Sie: /gold
Bot: 💰 GOLD ANALYSE (Enhanced)
     📈 Preis: $4,029.03
     📊 Technical Indicators:
        • RSI(14): 65.0 (NEUTRAL)
        • MACD: BULLISH
        • EMA(50): $3,850.00
     ✅ Empfehlung: HOLD 18%
     🎯 Target: $4,200
     🛑 Stop: $3,850

Sie: /geopolitik
Bot: 🌍 Analysiere geopolitische Risiken mit GDELT...
     (Dauert ~30 Sekunden)
     
     🌍 GEOPOLITISCHE LAGE (GDELT)
     📊 Gesamt-Risiko: 8.5/10
     🎯 Level: CRITICAL
     🛡️ Safe Haven: VERY HIGH
     
     ⚠️ NUKLEAR-SPANNUNGEN: 9/10
        Level: CRITICAL
        Trend: escalating
        Artikel: 47
     
     📰 Letzte Events:
        • Trump announces nuclear weapons tests...
        • Putin responds to US nuclear threat...
     
     💰 MARKT-IMPACT:
        Gold: UP +5-10%
        Bitcoin: UP +3-7%
        Equities: DOWN -10-20%
     
     ✅ Portfolio-Empfehlung:
        Defensive Positionierung RICHTIG!
        18% Gold, 8% Bitcoin, 74% Cash
```

---

## 🔧 TECHNISCHE DETAILS

### **Alpha Vantage Provider**
Datei: `/home/ubuntu/trading_agents/data_providers/alpha_vantage_provider.py`

**Funktionen:**
- `get_quote(symbol)` - Real-time Preise
- `get_rsi(symbol)` - RSI Indicator
- `get_macd(symbol)` - MACD Indicator
- `get_ema(symbol)` - EMA (50-day)
- `get_bbands(symbol)` - Bollinger Bands
- `get_comprehensive_analysis(symbol)` - Alles zusammen

**Symbol Mapping:**
- Gold: GLD (SPDR Gold Trust ETF)
- Silver: SLV (iShares Silver Trust)
- Bitcoin: GBTC (Grayscale Bitcoin Trust)
- S&P 500: SPY (S&P 500 ETF)

**Rate Limiting:**
- 5 calls/Minute (automatisch)
- 25 calls/Tag (Free Tier)

---

### **GDELT Provider**
Datei: `/home/ubuntu/trading_agents/data_providers/gdelt_provider.py`

**Funktionen:**
- `get_nuclear_risk_score()` - Nuklear-Risiko (0-10)
- `get_conflict_risk_score(region)` - Konflikt-Risiko
- `get_economic_risk_score()` - Wirtschafts-Risiko
- `get_comprehensive_risk_assessment()` - Gesamt-Assessment

**Risiko-Kategorien:**
- **Nuklear:** Atomwaffentests, ICBM, nukleare Bedrohungen
- **Konflikte:** Militärische Konflikte, Kriege, Angriffe
- **Wirtschaft:** Rezession, Inflation, Sanktionen

**Output:**
- Score: 0-10 (0=LOW, 10=CRITICAL)
- Level: LOW, MEDIUM, HIGH, CRITICAL
- Trend: stable, escalating, de-escalating
- Latest Events: Top 5 Nachrichten
- Market Impact: Gold, Bitcoin, Equities

---

### **Enhanced Telegram Bot**
Datei: `/home/ubuntu/trading_agents/telegram_bot_enhanced.py`

**Status:**
- ✅ Läuft 24/7 im Hintergrund
- Process ID: Check mit `ps aux | grep telegram_bot_enhanced`
- Log: `/home/ubuntu/trading_agents/telegram_bot_enhanced.log`

**Neustart (falls nötig):**
```bash
cd /home/ubuntu/trading_agents
# Stop old bot
ps aux | grep telegram_bot_enhanced | awk '{print $2}' | xargs kill

# Start new bot
nohup python3.11 telegram_bot_enhanced.py > telegram_bot_enhanced.log 2>&1 &

# Check status
ps aux | grep telegram_bot_enhanced
```

---

## 📊 PORTFOLIO-EMPFEHLUNGEN

### **AKTUELL (31. Oktober 2025):**

| Asset | Allokation | Leverage | Exposure | Empfehlung |
|-------|------------|----------|----------|------------|
| **Gold** | 18% (€1,800) | 4x | €7,200 | ✅ HOLD |
| **Silver** | 0% | - | €0 | ❌ NICHT KAUFEN |
| **Bitcoin** | 8% (€800) | 3x | €2,400 | ✅ HOLD |
| **S&P 500** | 0% | - | €0 | ❌ MEIDEN |
| **Cash** | 74% (€7,400) | - | €7,400 | ✅ MAXIMIEREN |

**Total Exposure:** 1.7x Portfolio

---

### **BEGRÜNDUNG:**

**Gold (18%):**
- RSI: 65 (bullish, nicht überkauft)
- MACD: Bullish Crossover
- Geopolitik: Nuklear-Risiko 9/10 (KRITISCH!)
- Safe Haven Demand: SEHR HOCH
- EV: +2.15% (mit Geopolitik-Bonus)

**Silver (0%):**
- Preis: $49 (Historisches Resistance!)
- Topping Pattern (FXEmpire Analyse)
- EV: -1.32% (NEGATIV!)
- 2011 Parallele: $49 → $26 Crash
- **Warten auf $42-45!**

**Bitcoin (8%):**
- Digital Gold Narrative intakt
- Geopolitik unterstützt (+3-7% erwartet)
- Unter $110k Resistance
- EV: +0.50%

**Cash (74%):**
- Defensive Positionierung (Nuklear-Risiko!)
- Flexibilität für Opportunities
- Warten auf bessere Entry-Points

---

## 🚨 RISIKEN & ALERTS

### **KRITISCHE RISIKEN:**

1. **NUKLEAR-ESKALATION (9/10)** ⚠️⚠️⚠️
   - Trump & Putin: Atomwaffentests
   - Höchste Eskalation seit Kaltem Krieg
   - Impact: Gold +5-10%, Equities -10-20%

2. **SILVER TOPPING PATTERN (8/10)** ⚠️⚠️
   - $49 = 2011 All-Time High
   - Crash-Risiko: 60%
   - **NICHT KAUFEN!**

3. **VIX ZU NIEDRIG (7/10)** ⚠️
   - VIX 13.54 trotz Nuklear-Krise
   - Complacency = Gefahr
   - Potentieller Spike >25

---

## 📈 TRIGGER FÜR TRADES

| Trigger | Aktion | Begründung |
|---------|--------|------------|
| Gold >$4,050 | Erhöhen auf 20-22% | Breakout bestätigt |
| Gold <$3,970 | Reduzieren auf 15% | Support gebrochen |
| Silver <$42 | KAUFEN 5-10% | Guter Entry |
| Bitcoin >$110k | Erhöhen auf 10% | Resistance gebrochen |
| Nuklear-Risiko >9.5 | Gold auf 25-30% | Maximale Eskalation |
| VIX >20 | Gold erhöhen | Fear steigt |

---

## 🔄 WARTUNG & UPDATES

### **Tägliche Checks:**
- `/status` im Telegram Bot
- Portfolio-Performance
- Geopolitische Entwicklungen

### **Wöchentliche Checks:**
- `/geopolitik` für Risk Assessment
- Alpha Vantage API Limit (25/Tag)
- GitHub Backup Status

### **Bei Breaking News:**
- `/geopolitik` sofort ausführen
- Risiko-Scores prüfen
- Portfolio anpassen falls nötig

---

## 🆘 TROUBLESHOOTING

### **Bot antwortet nicht:**
```bash
# Check if running
ps aux | grep telegram_bot_enhanced

# Check logs
tail -50 /home/ubuntu/trading_agents/telegram_bot_enhanced.log

# Restart
cd /home/ubuntu/trading_agents
kill <PID>
nohup python3.11 telegram_bot_enhanced.py > telegram_bot_enhanced.log 2>&1 &
```

### **Alpha Vantage Fehler:**
- "API Limit": 25 calls/Tag erreicht → Warte bis morgen
- "Error Message": Symbol falsch → Verwende GLD statt GC=F

### **GDELT Timeout:**
- Dauert 30-60 Sekunden (normal!)
- Falls Timeout: Verwende `/news` (schneller)
- Rate Limiting: Warte 1 Minute

---

## 📚 DOKUMENTATION

### **Alle Dateien auf GitHub:**
https://github.com/chxbb27vzq-svg/trading-system

### **Wichtige Dokumente:**
- `MASTER_FRAMEWORK_V3.md` - Trading Framework
- `PROFESSIONELLE_MARKTANALYSE_31_OKT_2025.md` - Aktuelle Analyse
- `ASSET_UNIVERSE_RECOMMENDATIONS.md` - Asset-Auswahl
- `SETUP_GUIDE.md` - Dieses Dokument

### **Module:**
- `data_providers/alpha_vantage_provider.py` - Alpha Vantage
- `data_providers/gdelt_provider.py` - GDELT
- `telegram_bot_enhanced.py` - Enhanced Bot
- `master_trading_system.py` - Master System

---

## ✅ ZUSAMMENFASSUNG

**WAS SIE HABEN:**
- ✅ GitHub Repository (Backup)
- ✅ Telegram Bot (24/7 Alerts)
- ✅ Alpha Vantage (Technical Indicators)
- ✅ GDELT (Geopolitik-Tracking)
- ✅ Professionelle Analysen
- ✅ Master Framework V3.0

**WAS SIE TUN KÖNNEN:**
- ✅ Portfolio-Status jederzeit abrufen
- ✅ Geopolitische Risiken tracken
- ✅ Technical Indicators nutzen
- ✅ Automatische Alerts (später)
- ✅ Daten-basierte Entscheidungen

**KOSTEN:**
- €0 (alles kostenlos!)

**NÄCHSTE SCHRITTE:**
1. Telegram Bot testen (`/start`)
2. `/geopolitik` ausführen
3. Portfolio beobachten
4. Bei Breaking News: Sofort checken!

---

**Erstellt:** 2. November 2025  
**Version:** 1.0 (Enhanced)  
**Status:** ✅ PRODUKTIV

