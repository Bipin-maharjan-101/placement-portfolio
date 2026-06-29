"""
Project 7: Interactive Data Dashboard
=======================================
Analyses UK retail sales data (ONS-style public dataset simulation)
and builds a multi-panel interactive HTML dashboard.
Covers trend analysis, seasonality, category breakdown, and KPI cards.

Skills: Data analysis, business intelligence, data storytelling
Tools:  Python, Pandas, Matplotlib, JSON (for embedded HTML dashboard)

Run main.py to get:
  1. Console data analysis report
  2. Static matplotlib dashboard (PNG)
  3. Standalone HTML interactive dashboard (open in browser)
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import json
from datetime import datetime

# ── 1. DATASET — UK RETAIL SALES (2022–2024) ──────────────────────────────────
# Simulates ONS-style monthly retail sales by category

np.random.seed(99)
months_24 = pd.date_range("2022-01-01", periods=36, freq="MS")
months_label = [m.strftime("%b %Y") for m in months_24]

base_sales = {
    "Food & Grocery":        [np.random.normal(4200 + i*8,  150) for i in range(36)],
    "Clothing & Footwear":   [np.random.normal(1800 + i*5,  200) for i in range(36)],
    "Electronics":           [np.random.normal(2100 + i*3,  250) for i in range(36)],
    "Home & Garden":         [np.random.normal(1500 + i*6,  180) for i in range(36)],
    "Health & Beauty":       [np.random.normal(980  + i*4,  90)  for i in range(36)],
    "Sports & Leisure":      [np.random.normal(760  + i*3,  110) for i in range(36)],
}

# Add seasonality (Christmas boost, Jan dip)
for key in base_sales:
    for i, val in enumerate(base_sales[key]):
        month = months_24[i].month
        if month == 12:
            base_sales[key][i] *= 1.35
        elif month == 1:
            base_sales[key][i] *= 0.82
        elif month in [6, 7]:
            base_sales[key][i] *= 1.08

df = pd.DataFrame(base_sales, index=months_24)
df = df.round(0).astype(int)
df["Total"] = df.sum(axis=1)
df["Month"] = months_label
df["Quarter"] = pd.PeriodIndex(months_24, freq="Q").astype(str)

# ── 2. KPI CALCULATIONS ───────────────────────────────────────────────────────

latest_month  = df.iloc[-1]["Total"]
prev_month    = df.iloc[-2]["Total"]
yoy_month     = df.iloc[-1]["Total"] - df.iloc[-13]["Total"]
yoy_pct       = yoy_month / df.iloc[-13]["Total"] * 100

ytd_2024      = df[df.index.year == 2024]["Total"].sum()
ytd_2023      = df[df.index.year == 2023]["Total"].sum()
ytd_growth    = (ytd_2024 - ytd_2023) / ytd_2023 * 100

best_category = df[list(base_sales.keys())].sum().idxmax()
best_cat_val  = df[list(base_sales.keys())].sum().max()

mom_change    = (latest_month - prev_month) / prev_month * 100

# ── 3. PRINT REPORT ───────────────────────────────────────────────────────────

print("=" * 70)
print("       UK RETAIL SALES DATA ANALYSIS REPORT")
print(f"       Period: Jan 2022 – Dec 2024")
print(f"       Generated: {datetime.now().strftime('%d %B %Y')}")
print("=" * 70)

print("\n📌 KEY PERFORMANCE INDICATORS")
print("-" * 45)
print(f"  Latest month sales:     £{latest_month:>8,.0f}k")
print(f"  Month-on-month change:  {mom_change:>+7.1f}%")
print(f"  YoY change:             {yoy_pct:>+7.1f}%")
print(f"  YTD 2024 vs 2023:       {ytd_growth:>+7.1f}%")
print(f"  Largest category:       {best_category} (£{best_cat_val/1000:.1f}m total)")

print("\n📌 CATEGORY PERFORMANCE (3-YEAR TOTALS)")
print("-" * 55)
cat_totals = df[list(base_sales.keys())].sum().sort_values(ascending=False)
total_all  = cat_totals.sum()
for cat, val in cat_totals.items():
    share = val / total_all * 100
    bar   = "█" * int(share // 2)
    print(f"  {cat:<22} £{val/1000:>7.1f}m  {share:>5.1f}%  {bar}")

print("\n📌 QUARTERLY BREAKDOWN (2024)")
print("-" * 55)
q2024 = df[df.index.year == 2024].copy()
q2024["Q"] = ["Q1","Q1","Q1","Q2","Q2","Q2","Q3","Q3","Q3","Q4","Q4","Q4"]
quarterly = q2024.groupby("Q")["Total"].sum()
for q, val in quarterly.items():
    print(f"  {q}:  £{val:>8,.0f}k")

print("\n📌 SEASONALITY INSIGHTS")
print("-" * 55)
monthly_avg = df.groupby(df.index.month)["Total"].mean()
peak_month  = monthly_avg.idxmax()
low_month   = monthly_avg.idxmin()
import calendar
print(f"  Peak month (avg):  {calendar.month_name[peak_month]} (£{monthly_avg[peak_month]:,.0f}k avg)")
print(f"  Lowest month (avg):{calendar.month_name[low_month]} (£{monthly_avg[low_month]:,.0f}k avg)")
print(f"  Seasonal spread:   {((monthly_avg.max()/monthly_avg.min()-1)*100):.1f}% variance")

print("\n📌 ANALYST NARRATIVE")
print("-" * 70)
print(f"""
  UK retail sales have shown consistent growth over the 3-year period,
  with total market growing at approximately {ytd_growth:.1f}% YoY in 2024.
  
  Food & Grocery remains the dominant category at {cat_totals['Food & Grocery']/total_all*100:.0f}% of total sales,
  reflecting defensive consumer spending behaviour. Electronics and Clothing
  show the highest volatility, sensitive to consumer confidence indices.
  
  Seasonal patterns are pronounced: December consistently outperforms by 30-35%
  vs annual average, while January shows a predictable 15-20% dip post-Christmas.
  
  Recommendation: Retailers should pre-position inventory in Q3, target
  digital campaigns from October, and use January for clearance and loyalty
  programme acquisition.
""")
print("=" * 70)

# ── 4. STATIC MATPLOTLIB DASHBOARD ───────────────────────────────────────────

fig, axes = plt.subplots(2, 2, figsize=(14, 9))
fig.suptitle("UK Retail Sales Dashboard — 2022 to 2024", fontsize=14, fontweight="bold")

x = range(len(df))

# Chart 1: Total sales trend
ax1 = axes[0, 0]
ax1.plot(list(x), df["Total"], color="#2E86AB", linewidth=2)
ax1.fill_between(list(x), df["Total"], alpha=0.15, color="#2E86AB")
ax1.set_title("Total Monthly Retail Sales (£k)")
ax1.set_xticks(list(x)[::6])
ax1.set_xticklabels(df["Month"].iloc[::6], rotation=30, ha="right", fontsize=7)
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f"£{v:,.0f}k"))

# Chart 2: Category stacked area
ax2 = axes[0, 1]
cats = list(base_sales.keys())
colours_stack = ["#2E86AB","#A23B72","#F18F01","#E07A5F","#81B29A","#3D405B"]
bottom = np.zeros(len(df))
for cat, col in zip(cats, colours_stack):
    ax2.bar(list(x), df[cat], bottom=bottom, label=cat, color=col, alpha=0.85, width=1)
    bottom += df[cat].values
ax2.set_title("Sales by Category (Stacked, £k)")
ax2.set_xticks(list(x)[::6])
ax2.set_xticklabels(df["Month"].iloc[::6], rotation=30, ha="right", fontsize=7)
ax2.legend(fontsize=6, loc="upper left")

# Chart 3: YoY comparison
ax3 = axes[1, 0]
if len(df[df.index.year == 2023]) == 12 and len(df[df.index.year == 2024]) == 12:
    vals_2022 = df[df.index.year == 2022]["Total"].values
    vals_2023 = df[df.index.year == 2023]["Total"].values
    vals_2024 = df[df.index.year == 2024]["Total"].values
    m_labels  = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    ax3.plot(m_labels, vals_2022, marker="o", label="2022", color="#A23B72", linewidth=1.8)
    ax3.plot(m_labels, vals_2023, marker="s", label="2023", color="#F18F01", linewidth=1.8)
    ax3.plot(m_labels, vals_2024, marker="^", label="2024", color="#2E86AB", linewidth=1.8)
ax3.set_title("Year-on-Year Comparison (£k)")
ax3.legend(fontsize=8)
ax3.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f"£{v:,.0f}k"))
ax3.set_xticklabels(m_labels, rotation=30, ha="right", fontsize=7)

# Chart 4: Category mix pie (2024 only)
ax4 = axes[1, 1]
sales_2024 = df[df.index.year == 2024][cats].sum()
wedges, texts, autotexts = ax4.pie(
    sales_2024, labels=cats, autopct="%1.0f%%",
    colors=colours_stack, startangle=140,
    textprops={"fontsize": 7}
)
ax4.set_title("2024 Sales Mix by Category")

plt.tight_layout()
plt.savefig("data_dashboard.png", dpi=150, bbox_inches="tight")
plt.show()
print("\n✅ Static dashboard saved as data_dashboard.png")

# ── 5. EXPORT DATA FOR HTML DASHBOARD ────────────────────────────────────────
export = {
    "months":  df["Month"].tolist(),
    "total":   df["Total"].tolist(),
    "categories": {cat: df[cat].tolist() for cat in cats},
}
with open("dashboard_data.json", "w") as f:
    json.dump(export, f)
print("✅ Data exported to dashboard_data.json (used by dashboard.html)")
print("   Open dashboard.html in your browser for the interactive version!")
