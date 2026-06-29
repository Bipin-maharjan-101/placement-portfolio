"""
Project 2: Business Operations Audit
======================================
Maps and audits the order fulfilment process for a small e-commerce business.
Identifies bottlenecks, calculates process efficiency metrics, and produces
a structured improvement report — mirroring real operations consulting work.

Skills: Process mapping, bottleneck analysis, operational efficiency
Tools:  Python, Pandas, Matplotlib
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch
import numpy as np
from datetime import datetime

# ── 1. PROCESS DATA ────────────────────────────────────────────────────────────
# Each process step: name, average time (mins), error rate (%), staff count

process_steps = [
    {"step": "Order Received",       "avg_time_mins": 2,  "error_rate_pct": 0.5, "staff": 1, "type": "start"},
    {"step": "Order Verification",   "avg_time_mins": 8,  "error_rate_pct": 3.2, "staff": 2, "type": "process"},
    {"step": "Inventory Check",      "avg_time_mins": 15, "error_rate_pct": 6.8, "staff": 1, "type": "bottleneck"},
    {"step": "Pick & Pack",          "avg_time_mins": 22, "error_rate_pct": 4.1, "staff": 4, "type": "process"},
    {"step": "Quality Control",      "avg_time_mins": 12, "error_rate_pct": 1.2, "staff": 2, "type": "process"},
    {"step": "Dispatch & Labelling", "avg_time_mins": 18, "error_rate_pct": 5.5, "staff": 2, "type": "bottleneck"},
    {"step": "Courier Collection",   "avg_time_mins": 35, "error_rate_pct": 2.0, "staff": 1, "type": "wait"},
    {"step": "Order Confirmed",      "avg_time_mins": 3,  "error_rate_pct": 0.3, "staff": 1, "type": "end"},
]

df = pd.DataFrame(process_steps)

# ── 2. VOLUME & FINANCIAL DATA ─────────────────────────────────────────────────

monthly_orders = 4200
avg_order_value = 47.50
error_cost_per_incident = 18.00   # avg cost to resolve an error

# ── 3. CALCULATIONS ────────────────────────────────────────────────────────────

df["total_errors_monthly"] = (df["error_rate_pct"] / 100 * monthly_orders).round(0)
df["error_cost_monthly"]   = df["total_errors_monthly"] * error_cost_per_incident
df["time_pct_of_total"]    = (df["avg_time_mins"] / df["avg_time_mins"].sum() * 100).round(1)

total_process_time = df["avg_time_mins"].sum()
total_errors_monthly = df["total_errors_monthly"].sum()
total_error_cost     = df["error_cost_monthly"].sum()
bottleneck_steps     = df[df["type"] == "bottleneck"]["step"].tolist()

# ── 4. PRINT REPORT ───────────────────────────────────────────────────────────

print("=" * 65)
print("       BUSINESS OPERATIONS AUDIT REPORT")
print("       Company: RetailFlow Ltd (E-Commerce)")
print(f"       Generated: {datetime.now().strftime('%d %B %Y')}")
print("=" * 65)

print("\n📌 PROCESS OVERVIEW")
print("-" * 65)
print(f"  Total process steps:       {len(df)}")
print(f"  Total end-to-end time:     {total_process_time} minutes ({total_process_time/60:.1f} hours)")
print(f"  Monthly order volume:      {monthly_orders:,}")
print(f"  Average order value:       £{avg_order_value:.2f}")

print("\n📌 STEP-BY-STEP ANALYSIS")
print("-" * 65)
print(f"  {'Step':<25} {'Time':>8} {'% Total':>8} {'Error%':>8} {'Monthly Errors':>15}")
print(f"  {'-'*24} {'-'*7} {'-'*7} {'-'*7} {'-'*14}")
for _, row in df.iterrows():
    flag = " ⚠️" if row["type"] == "bottleneck" else "  "
    print(f"  {row['step']:<25} {row['avg_time_mins']:>6}m {row['time_pct_of_total']:>7}% "
          f"{row['error_rate_pct']:>7}% {int(row['total_errors_monthly']):>13,}{flag}")

print("\n📌 BOTTLENECKS IDENTIFIED ⚠️")
print("-" * 65)
for step in bottleneck_steps:
    row = df[df["step"] == step].iloc[0]
    print(f"  ► {step}")
    print(f"    Time: {row['avg_time_mins']} mins | Error rate: {row['error_rate_pct']}% | "
          f"Monthly errors: {int(row['total_errors_monthly']):,}")

print("\n📌 FINANCIAL IMPACT OF ERRORS")
print("-" * 65)
print(f"  Total monthly errors:      {int(total_errors_monthly):,}")
print(f"  Cost per error resolution: £{error_cost_per_incident:.2f}")
print(f"  Total monthly error cost:  £{total_error_cost:,.0f}")
print(f"  Annualised error cost:     £{total_error_cost * 12:,.0f}")
print(f"  Error cost as % of revenue:  "
      f"{(total_error_cost / (monthly_orders * avg_order_value)) * 100:.1f}%")

print("\n📌 RECOMMENDATIONS")
print("-" * 65)
recs = [
    ("Inventory Check",      "Implement barcode scanning system. Target: reduce error rate from 6.8% to <2%."),
    ("Dispatch & Labelling", "Integrate label printing with order system to eliminate manual entry errors."),
    ("Courier Collection",   "Negotiate fixed daily collection windows to reduce 35-min average wait time."),
    ("Order Verification",   "Apply ML-based auto-verification for repeat customers (60% of orders)."),
]
for step, rec in recs:
    print(f"  ► {step}: {rec}")

total_saving_opportunity = df[df["type"].isin(["bottleneck"])]["error_cost_monthly"].sum()
print(f"\n  💡 Addressing bottlenecks alone could save ~£{total_saving_opportunity:,.0f}/month")
print("=" * 65)

# ── 5. VISUALISATIONS ─────────────────────────────────────────────────────────

fig, axes = plt.subplots(1, 3, figsize=(16, 6))
fig.suptitle("Business Operations Audit — RetailFlow Ltd", fontsize=14, fontweight="bold")

# Chart 1: Process time breakdown
colours_map = {"start": "#81B29A", "process": "#3D405B", "bottleneck": "#E07A5F",
               "wait": "#F2CC8F", "end": "#81B29A"}
bar_colours = [colours_map[t] for t in df["type"]]

ax1 = axes[0]
bars = ax1.barh(df["step"], df["avg_time_mins"], color=bar_colours, alpha=0.9, edgecolor="white")
ax1.set_title("Time per Process Step (mins)")
ax1.set_xlabel("Minutes")
for bar, val in zip(bars, df["avg_time_mins"]):
    ax1.text(val + 0.3, bar.get_y() + bar.get_height() / 2,
             f"{val}m", va="center", fontsize=8)
legend_patches = [
    mpatches.Patch(color="#E07A5F", label="Bottleneck"),
    mpatches.Patch(color="#3D405B", label="Process"),
    mpatches.Patch(color="#F2CC8F", label="Wait"),
    mpatches.Patch(color="#81B29A", label="Start/End"),
]
ax1.legend(handles=legend_patches, fontsize=7, loc="lower right")

# Chart 2: Error rates
ax2 = axes[1]
err_colours = ["#d62728" if r > 4 else "#ff7f0e" if r > 2 else "#2ca02c"
               for r in df["error_rate_pct"]]
ax2.bar(range(len(df)), df["error_rate_pct"], color=err_colours, alpha=0.85)
ax2.axhline(3, color="red", linestyle="--", linewidth=1, label="Risk threshold (3%)")
ax2.set_xticks(range(len(df)))
ax2.set_xticklabels(df["step"], rotation=45, ha="right", fontsize=7)
ax2.set_title("Error Rate per Step (%)")
ax2.set_ylabel("Error Rate (%)")
ax2.legend(fontsize=8)

# Chart 3: Monthly error cost by step
ax3 = axes[2]
ax3.pie(
    df["error_cost_monthly"],
    labels=df["step"],
    autopct=lambda p: f"£{p/100*total_error_cost:,.0f}" if p > 5 else "",
    startangle=140,
    textprops={"fontsize": 7},
    colors=plt.cm.Set3.colors[:len(df)]
)
ax3.set_title(f"Monthly Error Cost Distribution\n(Total: £{total_error_cost:,.0f})")

plt.tight_layout()
plt.savefig("operations_audit.png", dpi=150, bbox_inches="tight")
plt.show()
print("\n✅ Chart saved as operations_audit.png")
