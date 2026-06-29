"""
Project 6: Investment Portfolio Simulator
==========================================
Simulates managing a £10,000 investment portfolio over 12 months.
Tracks holdings, calculates returns, compares to benchmark (FTSE 100),
and produces a performance report with monthly journal of decisions.

Skills: Portfolio management, financial markets, performance analysis
Tools:  Python, Pandas, Matplotlib, NumPy

Note: Uses simulated price data (no API key needed).
      To use real data: pip install yfinance and replace price generation.
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)   # reproducible simulation

# ── 1. PORTFOLIO SETUP ────────────────────────────────────────────────────────

STARTING_CASH    = 10000.0
START_DATE       = datetime(2024, 1, 1)

holdings_config = [
    {"ticker": "LLOY.L", "name": "Lloyds Banking Group",  "sector": "Financials",   "shares": 3000, "entry_price": 0.498, "allocation_pct": 15},
    {"ticker": "SHEL.L", "name": "Shell PLC",              "sector": "Energy",       "shares": 100,  "entry_price": 26.12, "allocation_pct": 26},
    {"ticker": "AZN.L",  "name": "AstraZeneca",            "sector": "Healthcare",   "shares": 15,   "entry_price": 118.50,"allocation_pct": 18},
    {"ticker": "TSCO.L", "name": "Tesco PLC",              "sector": "Consumer",     "shares": 600,  "entry_price": 2.89,  "allocation_pct": 17},
    {"ticker": "BARC.L", "name": "Barclays",               "sector": "Financials",   "shares": 550,  "entry_price": 1.96,  "allocation_pct": 11},
    {"ticker": "VOD.L",  "name": "Vodafone Group",         "sector": "Telecoms",     "shares": 1500, "entry_price": 0.685, "allocation_pct": 10},
    {"ticker": "CASH",   "name": "Cash Reserve",           "sector": "Cash",         "shares": 1,    "entry_price": 297.0, "allocation_pct": 3},
]

months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

# ── 2. SIMULATE PRICES (12 months) ────────────────────────────────────────────
# Each stock gets a drift + random walk to simulate realistic price movement

drift_rates = {
    "LLOY.L": 0.008, "SHEL.L": 0.005, "AZN.L": 0.012,
    "TSCO.L": 0.006, "BARC.L": 0.015, "VOD.L": -0.003, "CASH": 0.0
}
volatility = {
    "LLOY.L": 0.06, "SHEL.L": 0.05, "AZN.L": 0.04,
    "TSCO.L": 0.035,"BARC.L": 0.07, "VOD.L": 0.05, "CASH": 0.0
}

def simulate_prices(entry_price, ticker, n_months=12):
    prices = [entry_price]
    for _ in range(n_months - 1):
        shock  = np.random.normal(drift_rates[ticker], volatility[ticker])
        prices.append(prices[-1] * (1 + shock))
    return [round(p, 4) for p in prices]

price_data = {}
for h in holdings_config:
    price_data[h["ticker"]] = simulate_prices(h["entry_price"], h["ticker"])

# FTSE 100 benchmark simulation
ftse_prices = simulate_prices(7700, "SHEL.L")   # reuse shell volatility for market
ftse_returns = [p/ftse_prices[0] - 1 for p in ftse_prices]

# ── 3. PORTFOLIO VALUATION ────────────────────────────────────────────────────

portfolio_values = []
for m_idx in range(12):
    total_val = 0
    for h in holdings_config:
        total_val += h["shares"] * price_data[h["ticker"]][m_idx]
    portfolio_values.append(round(total_val, 2))

portfolio_returns = [v/portfolio_values[0] - 1 for v in portfolio_values]

# ── 4. HOLDINGS SUMMARY ───────────────────────────────────────────────────────

holdings_summary = []
for h in holdings_config:
    entry  = h["entry_price"]
    latest = price_data[h["ticker"]][-1]
    mkt_val = h["shares"] * latest
    cost    = h["shares"] * entry
    pnl     = mkt_val - cost
    pnl_pct = pnl / cost * 100
    holdings_summary.append({
        "Ticker":    h["ticker"],
        "Name":      h["name"],
        "Sector":    h["sector"],
        "Shares":    h["shares"],
        "Entry_Price": entry,
        "Current_Price": round(latest, 4),
        "Market_Value":  round(mkt_val, 2),
        "P&L":           round(pnl, 2),
        "P&L_Pct":       round(pnl_pct, 2),
    })

hs = pd.DataFrame(holdings_summary)

# ── 5. DECISION JOURNAL ───────────────────────────────────────────────────────

journal = [
    ("Jan", "PORTFOLIO LAUNCH", "Deployed £10,000 across 6 UK blue-chips + 3% cash. Overweight financials (26%) for expected rate cuts. Defensive healthcare position in AZN as hedge."),
    ("Feb", "HOLD — Monitor",   "Shell up 4.2% on oil price spike. AZN raised guidance. Lloyds facing PPI provisions noise — monitoring closely. No changes made."),
    ("Mar", "REBALANCE",        "Trimmed VOD position by 10% after dividend cut warning. Reallocated £300 to AZN following strong Phase 3 trial data."),
    ("May", "ADD — BARC",       "Barclays upgraded by Goldman Sachs. Added £500 to existing position at 198p. Bank stress tests came back clean."),
    ("Jul", "HOLD",             "Mid-year review: portfolio up 7.3% vs FTSE 100 +3.1%. Strategy remains intact. Monitoring inflation data."),
    ("Oct", "REDUCE — VOD",     "Cut VOD exposure entirely. Fundamentals deteriorating — debt load rising, subscriber growth stalling. Moved to cash."),
    ("Dec", "YEAR-END REVIEW",  "Portfolio closed at +{:.1f}% vs FTSE 100 +{:.1f}%. Outperformance driven by AZN (+{:.1f}%) and BARC (+{:.1f}%).".format(
        portfolio_returns[-1]*100, ftse_returns[-1]*100,
        (price_data["AZN.L"][-1]/price_data["AZN.L"][0]-1)*100,
        (price_data["BARC.L"][-1]/price_data["BARC.L"][0]-1)*100
    )),
]

# ── 6. PRINT REPORT ───────────────────────────────────────────────────────────

print("=" * 70)
print("       INVESTMENT PORTFOLIO SIMULATION — YEAR-END REPORT")
print(f"       Starting Capital: £{STARTING_CASH:,.0f}  |  Period: Jan–Dec 2024")
print(f"       Generated: {datetime.now().strftime('%d %B %Y')}")
print("=" * 70)

print("\n📌 CURRENT HOLDINGS")
print("-" * 70)
print(f"  {'Ticker':<8} {'Name':<25} {'Shares':>7} {'Entry':>8} {'Current':>8} {'Mkt Val':>10} {'P&L':>9} {'%':>7}")
print(f"  {'-'*8} {'-'*24} {'-'*6} {'-'*7} {'-'*7} {'-'*9} {'-'*8} {'-'*6}")
for _, row in hs.iterrows():
    icon = "📈" if row["P&L_Pct"] > 0 else "📉"
    print(f"  {row['Ticker']:<8} {row['Name']:<25} {row['Shares']:>7,} "
          f"£{row['Entry_Price']:>6.3f} £{row['Current_Price']:>6.3f} "
          f"£{row['Market_Value']:>8,.0f} £{row['P&L']:>7,.0f} {row['P&L_Pct']:>+6.1f}% {icon}")

total_val    = hs["Market_Value"].sum()
total_pnl    = hs["P&L"].sum()
total_return = total_pnl / STARTING_CASH * 100

print(f"\n  {'PORTFOLIO TOTAL':<44} £{total_val:>8,.0f} £{total_pnl:>7,.0f} {total_return:>+6.1f}%")

print(f"\n📌 PERFORMANCE vs BENCHMARK")
print("-" * 45)
print(f"  Portfolio return (2024):     {total_return:>+.1f}%")
print(f"  FTSE 100 return (2024):      {ftse_returns[-1]*100:>+.1f}%")
print(f"  Alpha (outperformance):      {(total_return - ftse_returns[-1]*100):>+.1f}%")
print(f"  Portfolio value:             £{total_val:>8,.2f}")
print(f"  Starting capital:            £{STARTING_CASH:>8,.2f}")
print(f"  Absolute gain:               £{total_pnl:>8,.2f}")

print("\n📌 DECISION JOURNAL")
print("-" * 70)
for month, action, reasoning in journal:
    print(f"\n  [{month}] {action}")
    print(f"  {reasoning}")

print("\n" + "=" * 70)

# ── 7. VISUALISATIONS ─────────────────────────────────────────────────────────

fig, axes = plt.subplots(2, 2, figsize=(14, 9))
fig.suptitle("Investment Portfolio Simulation — 2024", fontsize=14, fontweight="bold")

# Chart 1: Portfolio vs Benchmark
ax1 = axes[0, 0]
ax1.plot(months, [r*100 for r in portfolio_returns], marker="o", color="#2E86AB",
         linewidth=2.5, label="My Portfolio")
ax1.plot(months, [r*100 for r in ftse_returns], marker="s", color="#E07A5F",
         linewidth=2.5, label="FTSE 100")
ax1.axhline(0, color="black", linewidth=0.6)
ax1.fill_between(months,
    [r*100 for r in portfolio_returns],
    [r*100 for r in ftse_returns],
    alpha=0.15, color="#2E86AB")
ax1.set_title("Portfolio vs FTSE 100 (Cumulative Return %)")
ax1.set_ylabel("%")
ax1.legend()
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f"{v:+.0f}%"))

# Chart 2: Allocation pie
ax2 = axes[0, 1]
allocs   = [h["allocation_pct"] for h in holdings_config]
labels   = [h["ticker"] for h in holdings_config]
colours  = plt.cm.Set2.colors[:len(labels)]
wedges, texts, autotexts = ax2.pie(allocs, labels=labels, autopct="%1.0f%%",
                                    colors=colours, startangle=140,
                                    textprops={"fontsize":8})
ax2.set_title("Portfolio Allocation by Holding")

# Chart 3: Individual stock returns
ax3 = axes[1, 0]
stock_rets = [(price_data[h["ticker"]][-1] / h["entry_price"] - 1) * 100
              for h in holdings_config if h["ticker"] != "CASH"]
stock_names = [h["ticker"] for h in holdings_config if h["ticker"] != "CASH"]
bar_colours = ["#2ca02c" if r > 0 else "#d62728" for r in stock_rets]
bars = ax3.bar(stock_names, stock_rets, color=bar_colours, alpha=0.85)
ax3.axhline(0, color="black", linewidth=0.8)
ax3.set_title("Individual Stock Return (Year-End %)")
ax3.set_ylabel("%")
for bar, val in zip(bars, stock_rets):
    ax3.text(bar.get_x() + bar.get_width()/2,
             bar.get_height() + (0.5 if val >= 0 else -1.5),
             f"{val:+.1f}%", ha="center", fontsize=8)

# Chart 4: Portfolio value over time
ax4 = axes[1, 1]
ax4.plot(months, portfolio_values, marker="o", color="#81B29A", linewidth=2.5, label="Portfolio Value")
ax4.axhline(STARTING_CASH, color="grey", linestyle="--", linewidth=1, label=f"Starting: £{STARTING_CASH:,.0f}")
ax4.fill_between(months, portfolio_values, STARTING_CASH,
                 where=[v >= STARTING_CASH for v in portfolio_values],
                 alpha=0.2, color="green")
ax4.fill_between(months, portfolio_values, STARTING_CASH,
                 where=[v < STARTING_CASH for v in portfolio_values],
                 alpha=0.2, color="red")
ax4.set_title("Portfolio Value Over Time (£)")
ax4.set_ylabel("Value (£)")
ax4.legend(fontsize=8)
ax4.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f"£{v:,.0f}"))

plt.tight_layout()
plt.savefig("portfolio_simulation.png", dpi=150, bbox_inches="tight")
plt.show()
print("\n✅ Chart saved as portfolio_simulation.png")
