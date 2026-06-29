"""
Project 1: Cost Reduction Analysis
===================================
Analyses a company's cost structure across departments,
identifies inefficiencies, and recommends cost-saving measures.
Mirrors real management consulting deliverables.

Skills: Financial analysis, data visualisation, report writing
Tools:  Python, Pandas, Matplotlib
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from datetime import datetime

# ── 1. SAMPLE DATASET ─────────────────────────────────────────────────────────
# Simulates 3 years of departmental cost data for a mid-size retail company

data = {
    "Department": [
        "Operations", "Marketing", "HR", "IT", "Finance",
        "Logistics", "Customer Service", "Procurement"
    ],
    "Budget_2022": [520000, 310000, 180000, 240000, 150000, 430000, 200000, 370000],
    "Actual_2022": [534000, 298000, 175000, 260000, 148000, 445000, 195000, 382000],
    "Budget_2023": [545000, 325000, 185000, 255000, 155000, 450000, 210000, 385000],
    "Actual_2023": [571000, 340000, 192000, 278000, 153000, 471000, 208000, 401000],
    "Budget_2024": [560000, 340000, 190000, 270000, 160000, 465000, 220000, 395000],
    "Actual_2024": [589000, 362000, 189000, 295000, 158000, 498000, 215000, 423000],
}

df = pd.DataFrame(data)

# ── 2. ANALYSIS FUNCTIONS ──────────────────────────────────────────────────────

def calculate_variance(df):
    """Calculate budget vs actual variance for each year."""
    for year in [2022, 2023, 2024]:
        df[f"Variance_{year}"] = df[f"Actual_{year}"] - df[f"Budget_{year}"]
        df[f"Variance_Pct_{year}"] = (
            (df[f"Variance_{year}"] / df[f"Budget_{year}"]) * 100
        ).round(2)
    return df

def calculate_yoy_growth(df):
    """Calculate year-on-year actual cost growth."""
    df["YoY_Growth_23"] = (
        (df["Actual_2023"] - df["Actual_2022"]) / df["Actual_2022"] * 100
    ).round(2)
    df["YoY_Growth_24"] = (
        (df["Actual_2024"] - df["Actual_2023"]) / df["Actual_2023"] * 100
    ).round(2)
    df["Avg_YoY_Growth"] = ((df["YoY_Growth_23"] + df["YoY_Growth_24"]) / 2).round(2)
    return df

def identify_overspend(df, threshold_pct=3.0):
    """Flag departments consistently overspending their budget."""
    overspend = df[
        (df["Variance_Pct_2022"] > threshold_pct) |
        (df["Variance_Pct_2023"] > threshold_pct) |
        (df["Variance_Pct_2024"] > threshold_pct)
    ][["Department", "Variance_Pct_2022", "Variance_Pct_2023", "Variance_Pct_2024"]]
    return overspend

def estimate_savings(df):
    """Estimate potential savings if departments hit budget targets."""
    df["Potential_Saving_2024"] = df["Actual_2024"] - df["Budget_2024"]
    df["Potential_Saving_2024"] = df["Potential_Saving_2024"].clip(lower=0)
    return df

# ── 3. RUN ANALYSIS ────────────────────────────────────────────────────────────

df = calculate_variance(df)
df = calculate_yoy_growth(df)
df = identify_overspend(df)
df = estimate_savings(df)

# ── 4. PRINT REPORT ───────────────────────────────────────────────────────────

print("=" * 65)
print("       COST REDUCTION ANALYSIS REPORT")
print(f"       Generated: {datetime.now().strftime('%d %B %Y')}")
print("=" * 65)

print("\n📌 TOTAL COMPANY COSTS BY YEAR")
print("-" * 40)
for year in [2022, 2023, 2024]:
    budget = df[f"Budget_{year}"].sum()
    actual = df[f"Actual_{year}"].sum()
    variance = actual - budget
    pct = (variance / budget) * 100
    print(f"  {year}  Budget: £{budget:,.0f}  |  Actual: £{actual:,.0f}  |  Over by: £{variance:,.0f} ({pct:.1f}%)")

print("\n📌 DEPARTMENTS WITH CONSISTENT OVERSPEND (>3% above budget)")
print("-" * 65)
overspend_depts = df[
    (df["Variance_Pct_2022"] > 3) |
    (df["Variance_Pct_2023"] > 3) |
    (df["Variance_Pct_2024"] > 3)
]
for _, row in overspend_depts.iterrows():
    print(f"  {row['Department']:<20} 2022: {row['Variance_Pct_2022']:+.1f}%  "
          f"2023: {row['Variance_Pct_2023']:+.1f}%  2024: {row['Variance_Pct_2024']:+.1f}%")

print("\n📌 POTENTIAL SAVINGS IF 2024 BUDGETS ARE MET")
print("-" * 45)
total_saving = df["Potential_Saving_2024"].sum()
for _, row in df[df["Potential_Saving_2024"] > 0].iterrows():
    print(f"  {row['Department']:<20} £{row['Potential_Saving_2024']:>8,.0f}")
print(f"  {'TOTAL POTENTIAL SAVING':<20} £{total_saving:>8,.0f}")

print("\n📌 FASTEST GROWING COST CENTRES (Avg YoY Growth)")
print("-" * 45)
top_growth = df.nlargest(3, "Avg_YoY_Growth")[["Department", "Avg_YoY_Growth"]]
for _, row in top_growth.iterrows():
    print(f"  {row['Department']:<20} +{row['Avg_YoY_Growth']:.1f}% per year")

print("\n📌 RECOMMENDATIONS")
print("-" * 65)
recommendations = [
    ("Operations & Logistics", "Review supplier contracts; consolidate vendors to cut procurement costs."),
    ("IT",                     "Audit software licences; migrate to cloud-based tools to reduce CapEx."),
    ("Marketing",              "Shift 20% of spend to digital channels with measurable ROI tracking."),
    ("Procurement",            "Implement e-procurement system to reduce manual processing costs."),
]
for dept, rec in recommendations:
    print(f"  ► {dept}: {rec}")

print("\n" + "=" * 65)

# ── 5. VISUALISATIONS ─────────────────────────────────────────────────────────

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Cost Reduction Analysis — 3-Year Overview", fontsize=15, fontweight="bold", y=1.01)

colours = ["#2E86AB", "#A23B72", "#F18F01"]
years   = [2022, 2023, 2024]

# Chart 1: Budget vs Actual per year
ax1 = axes[0, 0]
x = np.arange(len(df["Department"]))
width = 0.35
for i, year in enumerate(years):
    offset = (i - 1) * width / 1.5
    ax1.bar(x + offset, df[f"Actual_{year}"] / 1000, width / 1.5, label=str(year), color=colours[i], alpha=0.85)
ax1.set_title("Actual Costs by Department (£000s)")
ax1.set_xticks(x)
ax1.set_xticklabels(df["Department"], rotation=30, ha="right", fontsize=8)
ax1.legend(fontsize=8)
ax1.set_ylabel("Cost (£000s)")
ax1.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"£{v:.0f}k"))

# Chart 2: Variance % in 2024
ax2 = axes[0, 1]
colours_var = ["#d62728" if v > 0 else "#2ca02c" for v in df["Variance_Pct_2024"]]
bars = ax2.barh(df["Department"], df["Variance_Pct_2024"], color=colours_var, alpha=0.85)
ax2.axvline(0, color="black", linewidth=0.8)
ax2.set_title("2024 Budget vs Actual Variance (%)")
ax2.set_xlabel("Variance (%)")
for bar, val in zip(bars, df["Variance_Pct_2024"]):
    ax2.text(val + 0.1, bar.get_y() + bar.get_height() / 2,
             f"{val:+.1f}%", va="center", fontsize=8)

# Chart 3: Potential savings
ax3 = axes[1, 0]
savings_df = df[df["Potential_Saving_2024"] > 0]
ax3.bar(savings_df["Department"], savings_df["Potential_Saving_2024"] / 1000,
        color="#E07A5F", alpha=0.9, edgecolor="white")
ax3.set_title("Potential 2024 Savings if Budget Met (£000s)")
ax3.set_ylabel("Savings (£000s)")
ax3.set_xticklabels(savings_df["Department"], rotation=30, ha="right", fontsize=8)
ax3.yaxis.set_major_formatter(plt.FuncFormatter(lambda v, _: f"£{v:.0f}k"))

# Chart 4: YoY Growth trend
ax4 = axes[1, 1]
ax4.plot(df["Department"], df["YoY_Growth_23"], marker="o", label="2022→2023",
         color="#3D405B", linewidth=2)
ax4.plot(df["Department"], df["YoY_Growth_24"], marker="s", label="2023→2024",
         color="#81B29A", linewidth=2)
ax4.axhline(0, color="grey", linewidth=0.6, linestyle="--")
ax4.set_title("Year-on-Year Cost Growth (%)")
ax4.set_ylabel("Growth (%)")
ax4.set_xticklabels(df["Department"], rotation=30, ha="right", fontsize=8)
ax4.legend(fontsize=8)

plt.tight_layout()
plt.savefig("cost_reduction_analysis.png", dpi=150, bbox_inches="tight")
plt.show()
print("\n✅ Chart saved as cost_reduction_analysis.png")
