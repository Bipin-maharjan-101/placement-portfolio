"""
Project 4: Personal Finance Tracker & Analysis
================================================
A complete monthly budget tracker with income/expense categorisation,
trend analysis, savings rate calculation, and a multi-panel dashboard.
Demonstrates core accounting, budgeting, and data presentation skills.

Skills: Budgeting, financial categorisation, data visualisation
Tools:  Python, Pandas, Matplotlib
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
from datetime import datetime

# ── 1. FINANCIAL DATA (12 months) ─────────────────────────────────────────────

months = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

income_data = {
    "Month":      months,
    "Salary":     [2400,2400,2400,2400,2550,2550,2550,2550,2550,2700,2700,2700],
    "Freelance":  [0,   150, 0,   200, 0,   350, 0,   0,   180, 0,   250, 500],
    "Other":      [50,  0,   100, 0,   30,  0,   0,   80,  0,   0,   50,  200],
}

expense_data = {
    "Month":         months,
    "Rent":          [850]*12,
    "Groceries":     [210,230,195,220,240,225,235,245,215,220,230,280],
    "Transport":     [85, 90, 88, 92, 78, 85, 95, 88, 82, 90, 87, 95],
    "Utilities":     [95, 105,88, 75, 65, 60, 58, 62, 70, 82, 95, 110],
    "Eating_Out":    [120,95, 140,110,160,180,195,170,145,125,130,200],
    "Entertainment": [45, 30, 65, 50, 80, 90, 110,75, 55, 45, 80, 150],
    "Clothing":      [0,  0,  120,0,  65, 0,  0,  200,0,  0,  80, 150],
    "Health":        [30, 30, 55, 30, 30, 30, 30, 30, 30, 30, 30, 30],
    "Subscriptions": [35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35, 35],
    "Savings_ISA":   [200,150,200,200,250,300,200,150,250,300,200,300],
    "Emergency_Fund":[50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50, 50],
}

income_df  = pd.DataFrame(income_data)
expense_df = pd.DataFrame(expense_data)

# ── 2. CALCULATIONS ────────────────────────────────────────────────────────────

income_df["Total_Income"]   = income_df[["Salary","Freelance","Other"]].sum(axis=1)
expense_cols = [c for c in expense_df.columns if c != "Month"]
expense_df["Total_Expenses"] = expense_df[expense_cols].sum(axis=1)
expense_df["Discretionary"]  = expense_df[["Eating_Out","Entertainment","Clothing"]].sum(axis=1)
expense_df["Essential"]      = expense_df[["Rent","Groceries","Transport","Utilities","Health","Subscriptions"]].sum(axis=1)
expense_df["Savings_Total"]  = expense_df[["Savings_ISA","Emergency_Fund"]].sum(axis=1)

combined = income_df.merge(expense_df[["Month","Total_Expenses","Discretionary","Essential","Savings_Total"]], on="Month")
combined["Net_Cashflow"]    = combined["Total_Income"] - combined["Total_Expenses"]
combined["Savings_Rate_Pct"]= (combined["Savings_Total"] / combined["Total_Income"] * 100).round(1)
combined["Running_Savings"] = combined["Savings_Total"].cumsum()
combined["Cumulative_Net"]  = combined["Net_Cashflow"].cumsum()

# ── 3. PRINT REPORT ───────────────────────────────────────────────────────────

print("=" * 70)
print("       PERSONAL FINANCE TRACKER — ANNUAL SUMMARY")
print(f"       Financial Year: 2024  |  Generated: {datetime.now().strftime('%d %B %Y')}")
print("=" * 70)

print("\n📌 MONTHLY SNAPSHOT")
print("-" * 70)
print(f"  {'Month':<8} {'Income':>10} {'Expenses':>10} {'Net':>10} {'Savings':>10} {'Rate':>7}")
print(f"  {'-'*7} {'-'*9} {'-'*9} {'-'*9} {'-'*9} {'-'*6}")
for _, row in combined.iterrows():
    net_icon = "✅" if row["Net_Cashflow"] >= 0 else "❌"
    print(f"  {row['Month']:<8} £{row['Total_Income']:>8,.0f} £{row['Total_Expenses']:>8,.0f} "
          f"{net_icon}£{row['Net_Cashflow']:>7,.0f} £{row['Savings_Total']:>8,.0f} "
          f"{row['Savings_Rate_Pct']:>5.1f}%")

print("\n📌 ANNUAL TOTALS")
print("-" * 45)
print(f"  Total Income:           £{combined['Total_Income'].sum():>8,.0f}")
print(f"  Total Expenses:         £{combined['Total_Expenses'].sum():>8,.0f}")
print(f"  Net Cashflow:           £{combined['Net_Cashflow'].sum():>8,.0f}")
print(f"  Total Saved (ISA+EF):   £{combined['Savings_Total'].sum():>8,.0f}")
print(f"  Avg Monthly Savings Rate:  {combined['Savings_Rate_Pct'].mean():.1f}%")
print(f"  Best month:              {combined.loc[combined['Savings_Rate_Pct'].idxmax(),'Month']} "
      f"({combined['Savings_Rate_Pct'].max():.1f}%)")

print("\n📌 EXPENSE BREAKDOWN (Annual)")
print("-" * 45)
for col in ["Rent","Groceries","Transport","Utilities","Eating_Out",
            "Entertainment","Clothing","Health","Subscriptions"]:
    total = expense_df[col].sum()
    pct   = total / expense_df["Total_Expenses"].sum() * 100
    bar   = "█" * int(pct // 2)
    print(f"  {col:<16} £{total:>6,.0f}  {pct:>5.1f}%  {bar}")

print("\n📌 INSIGHTS & RECOMMENDATIONS")
print("-" * 65)
high_disc_months = combined[combined["Discretionary"] > combined["Discretionary"].quantile(0.75)]["Month"].tolist()
print(f"  ► High discretionary spend months: {', '.join(high_disc_months)}")
print(f"    → Consider a monthly discretionary budget cap of £350")
print(f"  ► Freelance income totalled £{income_df['Freelance'].sum():,.0f} — increase pipeline to £300/month target")
print(f"  ► Savings rate below 15% in {(combined['Savings_Rate_Pct'] < 15).sum()} months — automate transfers on payday")
print(f"  ► Clothing spend spikes in Mar/Aug/Nov — plan seasonal budget of £150")
print("=" * 70)

# ── 4. DASHBOARD ──────────────────────────────────────────────────────────────

fig, axes = plt.subplots(2, 2, figsize=(14, 9))
fig.suptitle("Personal Finance Dashboard — 2024", fontsize=14, fontweight="bold")

x = np.arange(len(months))

# Chart 1: Income vs Expenses
ax1 = axes[0, 0]
ax1.plot(months, combined["Total_Income"],   marker="o", color="#2E86AB", linewidth=2, label="Income")
ax1.plot(months, combined["Total_Expenses"], marker="s", color="#E07A5F", linewidth=2, label="Expenses")
ax1.fill_between(months, combined["Total_Income"], combined["Total_Expenses"],
                 where=combined["Total_Income"] >= combined["Total_Expenses"],
                 alpha=0.15, color="green", label="Surplus")
ax1.fill_between(months, combined["Total_Income"], combined["Total_Expenses"],
                 where=combined["Total_Income"] < combined["Total_Expenses"],
                 alpha=0.15, color="red", label="Deficit")
ax1.set_title("Income vs Expenses (£)")
ax1.set_ylabel("£")
ax1.legend(fontsize=8)
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f"£{v:,.0f}"))

# Chart 2: Savings rate
ax2 = axes[0, 1]
bar_cols = ["#2ca02c" if r >= 10 else "#ff7f0e" for r in combined["Savings_Rate_Pct"]]
ax2.bar(months, combined["Savings_Rate_Pct"], color=bar_cols, alpha=0.9)
ax2.axhline(10, color="green", linestyle="--", linewidth=1.2, label="10% target")
ax2.axhline(20, color="blue",  linestyle="--", linewidth=1.2, label="20% goal")
ax2.set_title("Monthly Savings Rate (%)")
ax2.set_ylabel("%")
ax2.legend(fontsize=8)

# Chart 3: Expense categories (stacked)
ax3 = axes[1, 0]
bottom = np.zeros(12)
cat_cols = {"Essential":"#3D405B","Discretionary":"#E07A5F","Savings_Total":"#81B29A"}
for cat, col in cat_cols.items():
    vals = combined[cat].values
    ax3.bar(months, vals, bottom=bottom, label=cat.replace("_"," "), color=col, alpha=0.85)
    bottom += vals
ax3.set_title("Expense Breakdown (Stacked)")
ax3.set_ylabel("£")
ax3.legend(fontsize=8)
ax3.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f"£{v:,.0f}"))

# Chart 4: Cumulative savings
ax4 = axes[1, 1]
ax4.fill_between(months, combined["Running_Savings"], alpha=0.3, color="#81B29A")
ax4.plot(months, combined["Running_Savings"], marker="o", color="#81B29A", linewidth=2, label="Savings (ISA+EF)")
ax4.fill_between(months, combined["Cumulative_Net"], alpha=0.2, color="#2E86AB")
ax4.plot(months, combined["Cumulative_Net"], marker="s", color="#2E86AB", linewidth=2, label="Cumulative Net")
ax4.axhline(0, color="black", linewidth=0.6)
ax4.set_title("Cumulative Savings & Net Position (£)")
ax4.set_ylabel("£")
ax4.legend(fontsize=8)
ax4.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v,_: f"£{v:,.0f}"))

plt.tight_layout()
plt.savefig("personal_finance_tracker.png", dpi=150, bbox_inches="tight")
plt.show()
print("\n✅ Dashboard saved as personal_finance_tracker.png")
