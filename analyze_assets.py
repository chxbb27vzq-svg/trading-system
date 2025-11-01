"""
Asset Universe Analysis - Welche Assets sollten wir handeln?
Analysiert: Liquidität, Volatilität, Korrelation, Sharpe Ratio
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def analyze_asset(ticker, name, category):
    """Analysiert ein einzelnes Asset"""
    try:
        # Daten holen (1 Jahr)
        asset = yf.Ticker(ticker)
        hist = asset.history(period="1y")
        
        if len(hist) < 200:
            return None
            
        # Metriken berechnen
        returns = hist['Close'].pct_change().dropna()
        
        # 1. Volatilität (annualisiert)
        volatility = returns.std() * np.sqrt(252) * 100
        
        # 2. Durchschnittliches Volumen
        avg_volume = hist['Volume'].mean()
        
        # 3. Return (1 Jahr)
        total_return = ((hist['Close'][-1] / hist['Close'][0]) - 1) * 100
        
        # 4. Sharpe Ratio (annualisiert, risk-free = 4%)
        excess_returns = returns - (0.04/252)
        sharpe = (excess_returns.mean() / returns.std()) * np.sqrt(252) if returns.std() > 0 else 0
        
        # 5. Max Drawdown
        cumulative = (1 + returns).cumprod()
        running_max = cumulative.cummax()
        drawdown = (cumulative - running_max) / running_max
        max_drawdown = drawdown.min() * 100
        
        # 6. Aktueller Preis
        current_price = hist['Close'][-1]
        
        return {
            'Ticker': ticker,
            'Name': name,
            'Category': category,
            'Price': f"${current_price:.2f}",
            'Volatility': f"{volatility:.1f}%",
            'Return_1Y': f"{total_return:.1f}%",
            'Sharpe': f"{sharpe:.2f}",
            'Max_DD': f"{max_drawdown:.1f}%",
            'Avg_Volume': f"{avg_volume/1e6:.1f}M",
            'Vol_Raw': volatility,
            'Return_Raw': total_return,
            'Sharpe_Raw': sharpe
        }
    except Exception as e:
        print(f"Error analyzing {ticker}: {e}")
        return None

# Asset Universe
assets = [
    # Aktuell im Portfolio
    ("GC=F", "Gold", "Commodities"),
    ("^GSPC", "S&P 500", "Equities"),
    ("BTC-USD", "Bitcoin", "Crypto"),
    ("BZ=F", "Brent Oil", "Commodities"),
    
    # Weitere Commodities
    ("SI=F", "Silver", "Commodities"),
    ("HG=F", "Copper", "Commodities"),
    ("NG=F", "Natural Gas", "Commodities"),
    ("ZW=F", "Wheat", "Commodities"),
    
    # Weitere Equities
    ("^IXIC", "NASDAQ", "Equities"),
    ("^DJI", "Dow Jones", "Equities"),
    ("^FTSE", "FTSE 100", "Equities"),
    ("^N225", "Nikkei 225", "Equities"),
    ("000001.SS", "Shanghai Composite", "Equities"),
    
    # Weitere Crypto
    ("ETH-USD", "Ethereum", "Crypto"),
    ("SOL-USD", "Solana", "Crypto"),
    ("BNB-USD", "Binance Coin", "Crypto"),
    
    # Forex
    ("EURUSD=X", "EUR/USD", "Forex"),
    ("GBPUSD=X", "GBP/USD", "Forex"),
    ("USDJPY=X", "USD/JPY", "Forex"),
    ("USDCHF=X", "USD/CHF", "Forex"),
    
    # Bonds
    ("^TNX", "US 10Y Treasury", "Bonds"),
    ("^TYX", "US 30Y Treasury", "Bonds"),
    
    # Volatility
    ("^VIX", "VIX", "Volatility"),
]

print("=" * 100)
print("ASSET UNIVERSE ANALYSIS")
print("=" * 100)
print(f"Analyzing {len(assets)} assets...")
print()

# Analysieren
results = []
for ticker, name, category in assets:
    print(f"Analyzing {name} ({ticker})...", end=" ")
    result = analyze_asset(ticker, name, category)
    if result:
        results.append(result)
        print("✓")
    else:
        print("✗")

# DataFrame erstellen
df = pd.DataFrame(results)

# Nach Kategorie sortieren
df = df.sort_values(['Category', 'Sharpe_Raw'], ascending=[True, False])

print()
print("=" * 100)
print("RESULTS - ALL ASSETS")
print("=" * 100)
print(df[['Name', 'Category', 'Price', 'Volatility', 'Return_1Y', 'Sharpe', 'Max_DD']].to_string(index=False))

print()
print("=" * 100)
print("TOP 10 BY SHARPE RATIO")
print("=" * 100)
top_sharpe = df.nlargest(10, 'Sharpe_Raw')
print(top_sharpe[['Name', 'Category', 'Return_1Y', 'Sharpe', 'Volatility']].to_string(index=False))

print()
print("=" * 100)
print("TOP 10 BY RETURN (1Y)")
print("=" * 100)
top_return = df.nlargest(10, 'Return_Raw')
print(top_return[['Name', 'Category', 'Return_1Y', 'Sharpe', 'Max_DD']].to_string(index=False))

print()
print("=" * 100)
print("CATEGORY ANALYSIS")
print("=" * 100)
category_stats = df.groupby('Category').agg({
    'Return_Raw': 'mean',
    'Vol_Raw': 'mean',
    'Sharpe_Raw': 'mean'
}).round(2)
category_stats.columns = ['Avg Return (%)', 'Avg Volatility (%)', 'Avg Sharpe']
print(category_stats)

print()
print("=" * 100)
print("RECOMMENDATIONS")
print("=" * 100)

# Empfehlungen basierend auf Kriterien
print("\n✅ HIGH PRIORITY (Sharpe > 1.0, Vol < 50%):")
high_priority = df[(df['Sharpe_Raw'] > 1.0) & (df['Vol_Raw'] < 50)]
if len(high_priority) > 0:
    for _, row in high_priority.iterrows():
        print(f"  • {row['Name']:20s} | Return: {row['Return_1Y']:>8s} | Sharpe: {row['Sharpe']:>5s} | Vol: {row['Volatility']:>6s}")
else:
    print("  None found")

print("\n⭐ MEDIUM PRIORITY (Sharpe > 0.5, Vol < 70%):")
medium_priority = df[(df['Sharpe_Raw'] > 0.5) & (df['Sharpe_Raw'] <= 1.0) & (df['Vol_Raw'] < 70)]
if len(medium_priority) > 0:
    for _, row in medium_priority.iterrows():
        print(f"  • {row['Name']:20s} | Return: {row['Return_1Y']:>8s} | Sharpe: {row['Sharpe']:>5s} | Vol: {row['Volatility']:>6s}")
else:
    print("  None found")

print("\n⚠️  LOW PRIORITY (Others):")
low_priority = df[~((df['Sharpe_Raw'] > 0.5) & (df['Vol_Raw'] < 70))]
if len(low_priority) > 0:
    for _, row in low_priority.iterrows():
        print(f"  • {row['Name']:20s} | Return: {row['Return_1Y']:>8s} | Sharpe: {row['Sharpe']:>5s} | Vol: {row['Volatility']:>6s}")

print()
print("=" * 100)
print("DIVERSIFICATION ANALYSIS")
print("=" * 100)

# Korrelationsmatrix für Top Assets
print("\nCalculating correlations for top assets...")
top_assets = df.nlargest(10, 'Sharpe_Raw')['Ticker'].tolist()

# Daten holen
correlation_data = {}
for ticker in top_assets:
    try:
        hist = yf.Ticker(ticker).history(period="1y")
        if len(hist) > 200:
            correlation_data[ticker] = hist['Close'].pct_change().dropna()
    except:
        pass

if len(correlation_data) > 1:
    corr_df = pd.DataFrame(correlation_data)
    correlation_matrix = corr_df.corr()
    
    print("\nCorrelation Matrix (Top 10 by Sharpe):")
    print(correlation_matrix.round(2))
    
    # Durchschnittliche Korrelation
    print("\nAverage Correlation per Asset:")
    avg_corr = correlation_matrix.mean().sort_values()
    for ticker, corr in avg_corr.items():
        name = df[df['Ticker'] == ticker]['Name'].values[0] if len(df[df['Ticker'] == ticker]) > 0 else ticker
        print(f"  {name:20s}: {corr:.2f}")

print()
print("=" * 100)
print("FINAL RECOMMENDATIONS")
print("=" * 100)
print("""
Basierend auf der Analyse:

1. KEEP (Aktuelles Portfolio):
   ✅ Gold - Safe Haven, niedrige Korrelation
   ✅ Bitcoin - Hohe Returns, aber volatil
   ⚠️  S&P 500 - Aktuell überbewertet (reduzieren)
   ⚠️  Brent Oil - Aktuell bearish (skip)

2. ADD (Neue Assets):
   Basierend auf Sharpe Ratio, Volatilität und Diversifikation
   (siehe HIGH/MEDIUM PRIORITY oben)

3. SKIP (Zu volatil oder schlechte Performance):
   (siehe LOW PRIORITY oben)
""")

print("\nAnalysis completed!")
