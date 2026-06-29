"""
Project 5: Financial Ratio Analysis — Listed Company
======================================================
Analyses 3 years of annual report data for a simulated FTSE 250 company.
Calculates key financial ratios across profitability, liquidity, efficiency,
and gearing. Produces analyst-style commentary and visualisations.

Skills: Financial statement analysis, ratio calculation, accounting
Tools:  Python, Pandas, Matplotlib
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from datetime import datetime

COMPANY = "RetailGroup PLC (FTSE 250 — Simulated)"

# ── 1. FINANCIAL DATA (from annual reports) ───────────────────────────────────
# All figures in £000s

financials = {
    "Year": [2022, 2023, 2024],

    # Income Statement
    "Revenue":          [485000, 521000, 563000],
    "COGS":             [291000, 312600, 337800],
    "Gross_Profit":     [194000, 208400, 225200],
    "Operating_Profit": [48500,  52100,  59100],
    "EBITDA":           [62300,  67800,  75400],
    "Interest_Expense": [4200,   5100,   6300],
    "PBT":              [44300,  47000,  52800],
    "Tax":              [9746,   10340,  11616],
    "Net_Profit":       [34554,  36660,  41184],

    # Balance Sheet
    "Total_Assets":     [312000, 338000, 371000],
    "Current_Assets":   [98000,  105000, 118000],
    "Inventory":        [42000,  45500,  49200],
    "Receivables":      [31000,  33000,  37500],
    "Cash":             [25000,  26500,  31300],
    "Current_Liabilities": [74000, 81000, 89000],
    "Total_Debt":       [95000,  108000, 122000],
    "Total_Equity":     [156000, 168000, 181000],
    "Shares_Outstanding": [120000, 120000, 122000],  # thousands

    # Cash Flow
    "Operating_CF":     [55000,  61000,  70000],
    "CapEx":            [18000,  22000,  25000],
    "Dividends_Paid":   [12000,  13000,  14500],
}

df = pd.DataFrame(financials)
df = df.set_index("Year")

# ── 2. RATIO CALCULATIONS ─────────────────────────────────────────────────────

# Profitability
df["Gross_Margin_Pct"]   = (df["Gross_Profit"]     / df["Revenue"] * 100).round(2)
df["Operating_Margin_Pct"] = (df["Operating_Profit"] / df["Revenue"] * 100).round(2)
df["Net_Margin_Pct"]     = (df["Net_Profit"]        / df["Revenue"] * 100).round(2)
df["EBITDA_Margin_Pct"]  = (df["EBITDA"]            / df["Revenue"] * 100).round(2)
df["ROE_Pct"]            = (df["Net_Profit"]         / df["Total_Equity"] * 100).round(2)
df["ROA_Pct"]            = (df["Net_Profit"]         / df["Total_Assets"] * 100).round(2)

# Liquidity
df["Current_Ratio"]      = (df["Current_Assets"]   / df["Current_Liabilities"]).round(2)
df["Quick_Ratio"]        = ((df["Current_Assets"] - df["Inventory"]) / df["Current_Liabilities"]).round(2)
df["Cash_Ratio"]         = (df["Cash"]              / df["Current_Liabilities"]).round(2)

# Efficiency
df["Asset_Turnover"]     = (df["Revenue"]           / df["Total_Assets"]).round(2)
df["Inventory_Days"]     = (df["Inventory"]          / df["COGS"] * 365).round(1)
df["Receivable_Days"]    = (df["Receivables"]        / df["Revenue"] * 365).round(1)

# Gearing / Leverage
df["Debt_to_Equity"]     = (df["Total_Debt"]        / df["Total_Equity"]).round(2)
df["Debt_to_Assets"]     = (df["Total_Debt"]        / df["Total_Assets"]).round(2)
df["Interest_Cover"]     = (df["Operating_Profit"]  / df["Interest_Expense"]).round(1)

# Per Share
df["EPS_p"]              = (df["Net_Profit"]         / df["Shares_Outstanding"] * 100).round(1)
df["DPS_p"]              = (df["Dividends_Paid"]     / df["Shares_Outstanding"] * 100).round(1)
df["Free_CF_per_share"]  = ((df["Operating_CF"] - df["CapEx"]) / df["Shares_Outstanding"] * 100).round(1)

# ── 3. PRINT REPORT ───────────────────────────────────────────────────────────

print("=" * 70)
print(f"       FINANCIAL RATIO ANALYSIS")
print(f"       Company: {COMPANY}")
print(f"       Generated: {datetime.now().strftime('%d %B %Y')}")
print("=" * 70)

sections = [
    ("PROFITABILITY RATIOS", [
        ("Gross Margin",         "Gross_Margin_Pct",    "%",  ">40% is strong for retail"),
        ("Operating Margin",     "Operating_Margin_Pct","%",  ">10% is healthy"),
        ("Net Margin",           "Net_Margin_Pct",      "%",  ">6% is good"),
        ("EBITDA Margin",        "EBITDA_Margin_Pct",   "%",  ">12% is strong"),
        ("Return on Equity",     "ROE_Pct",             "%",  ">15% is excellent"),
        ("Return on Assets",     "ROA_Pct",             "%",  ">8% is solid"),
    ]),
    ("LIQUIDITY RATIOS", [
        ("Current Ratio",        "Current_Ratio",       "x",  ">1.5x is comfortable"),
        ("Quick Ratio",          "Quick_Ratio",         "x",  ">1.0x is safe"),
        ("Cash Ratio",           "Cash_Ratio",          "x",  ">0.3x is adequate"),
    ]),
    ("EFFICIENCY RATIOS", [
        ("Asset Turnover",       "Asset_Turnover",      "x",  ">1.5x for retail"),
        ("Inventory Days",       "Inventory_Days",      " days", "Lower = faster turnover"),
        ("Receivable Days",      "Receivable_Days",     " days", "Lower = faster collection"),
    ]),
    ("GEARING / LEVERAGE", [
        ("Debt to Equity",       "Debt_to_Equity",      "x",  "<1.0x is prudent"),
        ("Debt to Assets",       "Debt_to_Assets",      "x",  "<0.5x is conservative"),
        ("Interest Cover",       "Interest_Cover",      "x",  ">5x is safe"),
    ]),
    ("PER SHARE DATA", [
        ("EPS",                  "EPS_p",               "p",  "Earnings per share"),
        ("DPS",                  "DPS_p",               "p",  "Dividend per share"),
        ("Free CF per share",    "Free_CF_per_share",   "p",  "Cash generation per share"),
    ]),
]

for section_title, metrics in sections:
    print(f"\n📌 {section_title}")
    print(f"  {'Metric':<22} {'2022':>10} {'2023':>10} {'2024':>10}  Benchmark")
    print(f"  {'-'*22} {'-'*9} {'-'*9} {'-'*9}  {'-'*25}")
    for label, col, unit, benchmark in metrics:
        vals = df[col].values
        trend = "↑" if vals[-1] > vals[0] else "↓"
        print(f"  {label:<22} {vals[0]:>9.1f}{unit} {vals[1]:>9.1f}{unit} "
              f"{vals[2]:>9.1f}{unit} {trend}  {benchmark}")

print("\n\n📌 ANALYST COMMENTARY")
print("-" * 70)
gm = df["Gross_Margin_Pct"].iloc[-1]
nm = df["Net_Margin_Pct"].iloc[-1]
cr = df["Current_Ratio"].iloc[-1]
dte = df["Debt_to_Equity"].iloc[-1]
ic  = df["Interest_Cover"].iloc[-1]
roe = df["ROE_Pct"].iloc[-1]
rev_growth = (df["Revenue"].iloc[-1] / df["Revenue"].iloc[0] - 1) * 100

print(f"""
  PROFITABILITY
  Revenue has grown {rev_growth:.1f}% over 3 years, while gross margin held at ~{gm:.0f}%,
  suggesting effective cost-of-goods management. Net margin improved from
  {df['Net_Margin_Pct'].iloc[0]:.1f}% to {nm:.1f}%, reflecting operating leverage.

  LIQUIDITY
  The current ratio of {cr:.2f}x and quick ratio of {df['Quick_Ratio'].iloc[-1]:.2f}x are 
  adequate. Cash generation remains strong with operating cashflow of
  £{df['Operating_CF'].iloc[-1]/1000:.1f}m in FY2024.

  GEARING
  Debt-to-equity has risen from {df['Debt_to_Equity'].iloc[0]:.2f}x to {dte:.2f}x, reflecting
  increased CapEx investment. Interest cover of {ic:.1f}x remains comfortably
  above the 3x covenant threshold.

  RETURNS
  ROE of {roe:.1f}% indicates strong shareholder value creation. EPS has grown
  from {df['EPS_p'].iloc[0]:.0f}p to {df['EPS_p'].iloc[-1]:.0f}p, supporting a rising dividend policy.

  RECOMMENDATION: BUY — improving margins, strong cashflow, and disciplined
  capital allocation suggest continued value creation.
""")
print("=" * 70)

# ── 4. VISUALISATIONS ─────────────────────────────────────────────────────────

years = [2022, 2023, 2024]
fig, axes = plt.subplots(2, 3, figsize=(16, 9))
fig.suptitle(f"Financial Ratio Analysis — {COMPANY}", fontsize=13, fontweight="bold")

def plot_ratio(ax, col, title, unit="", benchmark=None, colour="#2E86AB"):
    vals = df[col].values
    ax.plot(years, vals, marker="o", color=colour, linewidth=2.5)
    ax.fill_between(years, vals, alpha=0.15, color=colour)
    for y, v in zip(years, vals):
        ax.annotate(f"{v:.1f}{unit}", (y, v), textcoords="offset points",
                    xytext=(0, 8), ha="center", fontsize=8)
    if benchmark:
        ax.axhline(benchmark, color="red", linestyle="--", linewidth=1, label=f"Benchmark: {benchmark}{unit}")
        ax.legend(fontsize=7)
    ax.set_title(title, fontsize=9, fontweight="bold")
    ax.set_xticks(years)
    ax.set_ylabel(unit if unit else "")

plot_ratio(axes[0,0], "Gross_Margin_Pct", "Gross Margin (%)",     "%",  40,  "#2E86AB")
plot_ratio(axes[0,1], "Net_Margin_Pct",   "Net Margin (%)",       "%",  6,   "#A23B72")
plot_ratio(axes[0,2], "ROE_Pct",          "Return on Equity (%)", "%",  15,  "#F18F01")
plot_ratio(axes[1,0], "Current_Ratio",    "Current Ratio",        "x",  1.5, "#81B29A")
plot_ratio(axes[1,1], "Debt_to_Equity",   "Debt to Equity",       "x",  1.0, "#E07A5F")
plot_ratio(axes[1,2], "EPS_p",            "Earnings per Share",   "p",  None,"#3D405B")

plt.tight_layout()
plt.savefig("financial_ratio_analysis.png", dpi=150, bbox_inches="tight")
plt.show()
print("\n✅ Chart saved as financial_ratio_analysis.png")
