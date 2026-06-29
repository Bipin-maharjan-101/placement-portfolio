"""
Project 3: Market Entry Strategy
==================================
Produces a full market entry strategy for a UK fashion retailer
expanding into Germany. Covers PESTLE, SWOT, competitor analysis,
market sizing, and entry mode recommendation.

Skills: Strategic analysis, market research, structured frameworks
Tools:  Python, Pandas, Matplotlib
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from datetime import datetime

COMPANY   = "StyleCo UK"
MARKET    = "Germany"
INDUSTRY  = "Online Fashion Retail"

# ── 1. PESTLE ANALYSIS ────────────────────────────────────────────────────────

pestle = {
    "Political": [
        ("EU single market access post-Brexit", "Negative", 3),
        ("Stable German government & regulation", "Positive", 1),
        ("GDPR compliance requirements", "Neutral", 2),
    ],
    "Economic": [
        ("Germany: largest EU economy (GDP €4.1tn)", "Positive", 1),
        ("Consumer spending growth +2.8% YoY", "Positive", 1),
        ("Rising interest rates affecting disposable income", "Negative", 2),
    ],
    "Social": [
        ("Strong sustainability consciousness in consumers", "Positive", 2),
        ("Growing online shopping adoption (82% penetration)", "Positive", 1),
        ("Cultural preference for quality over fast fashion", "Neutral", 2),
    ],
    "Technological": [
        ("Mature e-commerce infrastructure", "Positive", 1),
        ("High mobile commerce adoption", "Positive", 1),
        ("Advanced logistics network (DHL, DPD)", "Positive", 1),
    ],
    "Legal": [
        ("Strict consumer return rights (14+ days)", "Negative", 2),
        ("Packaging and waste regulations (VerpackG)", "Negative", 2),
        ("Strong employment law if hiring locally", "Neutral", 3),
    ],
    "Environmental": [
        ("High consumer demand for sustainable products", "Positive", 2),
        ("Carbon reporting requirements increasing", "Neutral", 2),
        ("Circular economy policy pressure", "Neutral", 3),
    ],
}

# ── 2. SWOT ANALYSIS ─────────────────────────────────────────────────────────

swot = {
    "Strengths": [
        "Established UK brand with 15-year track record",
        "Strong digital-first operations and fulfilment",
        "Competitive price point vs German incumbents",
        "Proprietary sustainability line ('GreenCo')",
    ],
    "Weaknesses": [
        "No brand recognition in Germany",
        "No local language customer service capability",
        "Higher logistics costs than local competitors",
        "Currency risk (GBP/EUR exchange rate exposure)",
    ],
    "Opportunities": [
        "Underserved mid-market sustainable fashion segment",
        "German consumers spend avg €1,400/year on fashion",
        "Online fashion market growing at 9.2% CAGR",
        "Partnership potential with Zalando marketplace",
    ],
    "Threats": [
        "Zalando, About You, and Zara dominate the market",
        "High return rates in German e-commerce (avg 50%)",
        "Strong local brands with loyal customer bases",
        "Brexit-related customs friction raises unit costs",
    ],
}

# ── 3. COMPETITOR ANALYSIS ────────────────────────────────────────────────────

competitors = pd.DataFrame({
    "Company":         ["Zalando", "About You", "H&M Germany", "Zara Germany", "StyleCo (Projected)"],
    "Market_Share_Pct": [28.4,      12.1,         9.6,           7.2,           1.5],
    "Price_Index":      [100,        95,           85,            110,           90],
    "Sustainability":   [3,          2,            3,             2,             5],
    "Online_Only":      [True,       True,         False,         False,         True],
})

# ── 4. MARKET SIZING ──────────────────────────────────────────────────────────

market_size_bn = 24.8       # German online fashion market 2024 (£bn)
cagr           = 0.092
target_share_y3 = 0.015     # 1.5% market share by year 3

year1_revenue = market_size_bn * 0.003
year2_revenue = market_size_bn * (1 + cagr) * 0.008
year3_revenue = market_size_bn * ((1 + cagr) ** 2) * target_share_y3

# ── 5. ENTRY MODE EVALUATION ──────────────────────────────────────────────────

entry_modes = pd.DataFrame({
    "Mode":           ["Direct Website", "Zalando Partnership", "Joint Venture", "Acquisition"],
    "Cost_Score":     [4, 8, 5, 2],          # 10 = lowest cost
    "Speed_Score":    [5, 9, 6, 7],          # 10 = fastest
    "Control_Score":  [9, 4, 6, 8],          # 10 = most control
    "Risk_Score":     [4, 8, 6, 3],          # 10 = lowest risk
})
entry_modes["Total_Score"] = entry_modes[["Cost_Score","Speed_Score","Control_Score","Risk_Score"]].mean(axis=1)

# ── 6. PRINT REPORT ───────────────────────────────────────────────────────────

print("=" * 70)
print(f"       MARKET ENTRY STRATEGY: {COMPANY} → {MARKET}")
print(f"       Industry: {INDUSTRY}")
print(f"       Generated: {datetime.now().strftime('%d %B %Y')}")
print("=" * 70)

print("\n📌 PESTLE ANALYSIS SUMMARY")
print("-" * 70)
for pillar, factors in pestle.items():
    print(f"\n  {pillar.upper()}")
    for factor, impact, priority in factors:
        icon = "✅" if impact == "Positive" else "⚠️" if impact == "Neutral" else "❌"
        stars = "★" * (4 - priority) + "☆" * (priority - 1)
        print(f"    {icon} [{stars}] {factor}")

print("\n\n📌 SWOT ANALYSIS")
print("-" * 70)
for category, points in swot.items():
    icon = {"Strengths":"✅","Weaknesses":"❌","Opportunities":"🎯","Threats":"⚠️"}[category]
    print(f"\n  {icon} {category.upper()}")
    for p in points:
        print(f"    • {p}")

print("\n\n📌 COMPETITOR LANDSCAPE")
print("-" * 70)
print(f"  {'Company':<20} {'Market Share':>13} {'Price Index':>12} {'Sustainability':>14}")
print(f"  {'-'*20} {'-'*12} {'-'*11} {'-'*13}")
for _, row in competitors.iterrows():
    print(f"  {row['Company']:<20} {row['Market_Share_Pct']:>11.1f}% {row['Price_Index']:>12} "
          f"  {'⭐'*int(row['Sustainability'])}")

print("\n\n📌 REVENUE PROJECTIONS (3-YEAR)")
print("-" * 70)
print(f"  Market size (2024):     £{market_size_bn:.1f}bn")
print(f"  Market CAGR:            {cagr*100:.1f}%")
print(f"  Year 1 (0.3% share):    £{year1_revenue:.2f}m")
print(f"  Year 2 (0.8% share):    £{year2_revenue:.2f}m")
print(f"  Year 3 (1.5% share):    £{year3_revenue:.2f}m")

print("\n\n📌 ENTRY MODE RECOMMENDATION")
print("-" * 70)
best = entry_modes.loc[entry_modes["Total_Score"].idxmax()]
print(f"  {'Mode':<22} {'Cost':>6} {'Speed':>7} {'Control':>8} {'Risk':>6} {'Score':>7}")
print(f"  {'-'*22} {'-'*5} {'-'*6} {'-'*7} {'-'*5} {'-'*6}")
for _, row in entry_modes.iterrows():
    marker = " ◄ RECOMMENDED" if row["Mode"] == best["Mode"] else ""
    print(f"  {row['Mode']:<22} {row['Cost_Score']:>6} {row['Speed_Score']:>7} "
          f"{row['Control_Score']:>8} {row['Risk_Score']:>6} {row['Total_Score']:>7.1f}{marker}")

print(f"\n  Recommendation: Launch via {best['Mode']} to maximise speed-to-market")
print("  while managing cost and risk exposure in year 1.")
print("=" * 70)

# ── 7. VISUALISATIONS ─────────────────────────────────────────────────────────

fig, axes = plt.subplots(1, 3, figsize=(16, 6))
fig.suptitle(f"Market Entry Strategy: {COMPANY} → {MARKET}", fontsize=14, fontweight="bold")

# Chart 1: Market share comparison
ax1 = axes[0]
colours_comp = ["#2E86AB","#A23B72","#F18F01","#E07A5F","#81B29A"]
wedges, texts, autotexts = ax1.pie(
    competitors["Market_Share_Pct"],
    labels=competitors["Company"],
    autopct="%1.1f%%",
    colors=colours_comp,
    startangle=90,
    textprops={"fontsize": 8}
)
ax1.set_title("German Online Fashion Market Share (%)")

# Chart 2: Revenue projections
ax2 = axes[1]
years    = ["Year 1", "Year 2", "Year 3"]
revenues = [year1_revenue, year2_revenue, year3_revenue]
bars = ax2.bar(years, revenues, color=["#3D405B","#81B29A","#F2CC8F"], alpha=0.9, edgecolor="white")
ax2.set_title("StyleCo Projected Revenue in Germany (£m)")
ax2.set_ylabel("Revenue (£m)")
for bar, val in zip(bars, revenues):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
             f"£{val:.2f}m", ha="center", fontsize=9)

# Chart 3: Entry mode radar-style bar chart
ax3 = axes[2]
x = np.arange(len(entry_modes["Mode"]))
width = 0.2
metrics = ["Cost_Score","Speed_Score","Control_Score","Risk_Score"]
colours_m = ["#2E86AB","#A23B72","#F18F01","#E07A5F"]
for i, (metric, col) in enumerate(zip(metrics, colours_m)):
    ax3.bar(x + i*width, entry_modes[metric], width, label=metric.replace("_Score",""),
            color=col, alpha=0.85)
ax3.set_xticks(x + width*1.5)
ax3.set_xticklabels(entry_modes["Mode"], rotation=20, ha="right", fontsize=8)
ax3.set_title("Entry Mode Evaluation (Score /10)")
ax3.legend(fontsize=7)
ax3.set_ylim(0, 12)
ax3.axhline(7, linestyle="--", color="grey", linewidth=0.8, label="Target threshold")

plt.tight_layout()
plt.savefig("market_entry_strategy.png", dpi=150, bbox_inches="tight")
plt.show()
print("\n✅ Chart saved as market_entry_strategy.png")
