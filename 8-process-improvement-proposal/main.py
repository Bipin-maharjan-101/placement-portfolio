"""
Project 8: Process Improvement Proposal
=========================================
Analyses the student enrolment process for a university department.
Maps current state, identifies pain points using stakeholder feedback,
applies BA tools (MoSCoW, requirements document, process flowchart),
and produces a structured improvement proposal.

Skills: Business analysis, requirements gathering, process improvement
Tools:  Python, Pandas, Matplotlib (flowchart), BA frameworks
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
import numpy as np
from datetime import datetime

# ── 1. CURRENT STATE — PROCESS STEPS ─────────────────────────────────────────

current_state = [
    {"id": "S1", "step": "Student submits paper form",      "actor": "Student",    "time_hrs": 0.5, "pain_score": 8, "manual": True},
    {"id": "S2", "step": "Admin receives & logs form",      "actor": "Admin",      "time_hrs": 1.0, "pain_score": 7, "manual": True},
    {"id": "S3", "step": "Eligibility check (manual)",      "actor": "Admin",      "time_hrs": 2.5, "pain_score": 9, "manual": True},
    {"id": "S4", "step": "Approval from programme director","actor": "Director",   "time_hrs": 24,  "pain_score": 8, "manual": False},
    {"id": "S5", "step": "Module allocation (spreadsheet)", "actor": "Admin",      "time_hrs": 1.5, "pain_score": 7, "manual": True},
    {"id": "S6", "step": "IT system updated manually",      "actor": "IT Admin",   "time_hrs": 2.0, "pain_score": 9, "manual": True},
    {"id": "S7", "step": "Confirmation letter posted",      "actor": "Admin",      "time_hrs": 0.5, "pain_score": 6, "manual": True},
    {"id": "S8", "step": "Student receives confirmation",   "actor": "Student",    "time_hrs": 72,  "pain_score": 8, "manual": False},
]

future_state = [
    {"id": "F1", "step": "Student submits online form",     "actor": "Student",    "time_hrs": 0.2, "pain_score": 2, "manual": False},
    {"id": "F2", "step": "Automated eligibility check",     "actor": "System",     "time_hrs": 0.1, "pain_score": 1, "manual": False},
    {"id": "F3", "step": "Director approval (digital)",     "actor": "Director",   "time_hrs": 4,   "pain_score": 2, "manual": False},
    {"id": "F4", "step": "Auto module allocation",          "actor": "System",     "time_hrs": 0.1, "pain_score": 1, "manual": False},
    {"id": "F5", "step": "IT system auto-updated",          "actor": "System",     "time_hrs": 0.1, "pain_score": 1, "manual": False},
    {"id": "F6", "step": "Email confirmation sent",         "actor": "System",     "time_hrs": 0.1, "pain_score": 1, "manual": False},
]

cs_df = pd.DataFrame(current_state)
fs_df = pd.DataFrame(future_state)

# ── 2. STAKEHOLDER ANALYSIS ───────────────────────────────────────────────────

stakeholders = pd.DataFrame({
    "Stakeholder":  ["Students", "Admin Staff", "Programme Directors", "IT Department", "Senior Management"],
    "Interest":     [9, 8, 6, 5, 7],
    "Influence":    [5, 6, 8, 7, 9],
    "Pain_Score":   [8, 9, 6, 7, 4],
    "Priority":     ["High","High","High","Medium","Medium"],
})

# ── 3. MOSCOW PRIORITISATION ──────────────────────────────────────────────────

moscow = {
    "Must Have": [
        "Online enrolment form accessible 24/7",
        "Automated eligibility rules engine",
        "Email confirmation within 4 hours",
        "Integration with student information system (SIS)",
    ],
    "Should Have": [
        "Digital approval workflow with auto-reminders",
        "Student dashboard showing enrolment status",
        "Automated module conflict detection",
    ],
    "Could Have": [
        "Chatbot for FAQ support during enrolment",
        "Mobile app integration",
        "AI-powered module recommendations",
    ],
    "Won't Have (Now)": [
        "Full SIS platform replacement",
        "Biometric verification",
        "Live video approval with directors",
    ],
}

# ── 4. REQUIREMENTS DOCUMENT ──────────────────────────────────────────────────

requirements = [
    {"REQ_ID": "FR-01", "Type": "Functional",     "Priority": "Must",   "Requirement": "System shall allow students to submit enrolment requests via web portal"},
    {"REQ_ID": "FR-02", "Type": "Functional",     "Priority": "Must",   "Requirement": "System shall auto-check eligibility against degree programme rules"},
    {"REQ_ID": "FR-03", "Type": "Functional",     "Priority": "Must",   "Requirement": "System shall route approval requests to relevant director with 48hr SLA"},
    {"REQ_ID": "FR-04", "Type": "Functional",     "Priority": "Must",   "Requirement": "System shall auto-update student module allocation upon approval"},
    {"REQ_ID": "FR-05", "Type": "Functional",     "Priority": "Should", "Requirement": "System shall provide real-time status tracker for students"},
    {"REQ_ID": "FR-06", "Type": "Functional",     "Priority": "Could",  "Requirement": "System shall support AI-based module recommendations"},
    {"REQ_ID": "NFR-01","Type": "Non-Functional", "Priority": "Must",   "Requirement": "System shall be available 99.5% uptime during enrolment periods"},
    {"REQ_ID": "NFR-02","Type": "Non-Functional", "Priority": "Must",   "Requirement": "System shall comply with GDPR and university data governance policies"},
    {"REQ_ID": "NFR-03","Type": "Non-Functional", "Priority": "Should", "Requirement": "System shall process eligibility check in under 3 seconds"},
    {"REQ_ID": "NFR-04","Type": "Non-Functional", "Priority": "Should", "Requirement": "System shall be accessible on mobile devices (WCAG 2.1 AA)"},
]

req_df = pd.DataFrame(requirements)

# ── 5. PRINT REPORT ───────────────────────────────────────────────────────────

print("=" * 70)
print("       PROCESS IMPROVEMENT PROPOSAL")
print("       Project: University Student Enrolment System")
print("       Analyst: [Your Name] | Methodology: Agile BA / BCS")
print(f"       Date: {datetime.now().strftime('%d %B %Y')}")
print("=" * 70)

print("\n📌 EXECUTIVE SUMMARY")
print("-" * 70)
current_time  = cs_df["time_hrs"].sum()
future_time   = fs_df["time_hrs"].sum()
time_saving   = current_time - future_time
saving_pct    = time_saving / current_time * 100
print(f"""
  The current student enrolment process is entirely manual, taking an average
  of {current_time:.0f} hours end-to-end (including 72hr postal confirmation).
  Pain scores from stakeholder interviews average {cs_df['pain_score'].mean():.1f}/10.

  This proposal recommends digitising the process through a self-service
  web portal with automated eligibility checking and digital approvals.

  Projected outcomes:
  • End-to-end time: {current_time:.0f} hrs → {future_time:.1f} hrs (saving {saving_pct:.0f}%)
  • Admin effort:    ~4 hrs per student → <1 hr per student
  • Student NPS:     Expected increase from -12 to +40+
  • Annual saving:   ~£42,000 (admin hours for 3,000 students/year)
""")

print("\n📌 CURRENT STATE — PROCESS STEPS")
print("-" * 70)
print(f"  {'ID':<5} {'Step':<38} {'Actor':<12} {'Time':>8} {'Pain':>6} {'Manual':>7}")
print(f"  {'-'*4} {'-'*37} {'-'*11} {'-'*7} {'-'*5} {'-'*6}")
for _, row in cs_df.iterrows():
    manual = "✅" if row["manual"] else "🔄"
    time_label = f"{row['time_hrs']}h" if row["time_hrs"] < 24 else f"{row['time_hrs']:.0f}h"
    print(f"  {row['id']:<5} {row['step']:<38} {row['actor']:<12} {time_label:>8} "
          f"{row['pain_score']:>5}/10 {manual:>7}")
print(f"\n  Total end-to-end: {current_time:.0f} hours | Avg pain score: {cs_df['pain_score'].mean():.1f}/10")

print("\n📌 MOSCOW PRIORITISATION")
print("-" * 70)
icons = {"Must Have": "🔴", "Should Have": "🟡", "Could Have": "🟢", "Won't Have (Now)": "⚪"}
for category, items in moscow.items():
    print(f"\n  {icons[category]} {category.upper()}")
    for item in items:
        print(f"    • {item}")

print("\n\n📌 REQUIREMENTS (Sample)")
print("-" * 70)
print(f"  {'ID':<8} {'Type':<15} {'Priority':<8}  Requirement")
print(f"  {'-'*7} {'-'*14} {'-'*7}  {'-'*40}")
for _, row in req_df.iterrows():
    print(f"  {row['REQ_ID']:<8} {row['Type']:<15} {row['Priority']:<8}  {row['Requirement']}")

print("\n\n📌 FUTURE STATE — PROJECTED IMPROVEMENTS")
print("-" * 70)
print(f"  {'ID':<5} {'Step':<38} {'Actor':<12} {'Time':>8} {'Pain':>6}")
print(f"  {'-'*4} {'-'*37} {'-'*11} {'-'*7} {'-'*5}")
for _, row in fs_df.iterrows():
    print(f"  {row['id']:<5} {row['step']:<38} {row['actor']:<12} "
          f"{row['time_hrs']:.1f}h{' ':>4} {row['pain_score']:>4}/10")
print(f"\n  Total end-to-end: {future_time:.1f} hours | Avg pain score: {fs_df['pain_score'].mean():.1f}/10")
print(f"  Time reduction: {saving_pct:.0f}% | Pain reduction: "
      f"{(cs_df['pain_score'].mean() - fs_df['pain_score'].mean())/cs_df['pain_score'].mean()*100:.0f}%")

print("\n" + "=" * 70)

# ── 6. VISUALISATIONS ─────────────────────────────────────────────────────────

fig, axes = plt.subplots(1, 3, figsize=(16, 6))
fig.suptitle("Process Improvement Proposal — University Enrolment System", fontsize=13, fontweight="bold")

# Chart 1: Current vs Future process time
ax1 = axes[0]
steps_curr = cs_df["step"].str[:20].tolist()
steps_fut  = fs_df["step"].str[:20].tolist()
y_curr = range(len(cs_df))
y_fut  = range(len(fs_df))
ax1.barh([s + " [NOW]" for s in steps_curr], cs_df["time_hrs"], color="#E07A5F", alpha=0.85, label="Current")
ax1.set_title("Current Process Step Time (hrs)")
ax1.set_xlabel("Hours")
for i, v in enumerate(cs_df["time_hrs"]):
    ax1.text(v + 0.5, i, f"{v}h", va="center", fontsize=7)
ax1.invert_yaxis()

# Chart 2: Stakeholder power/interest grid
ax2 = axes[1]
colours_s = {"High":"#E07A5F","Medium":"#F18F01","Low":"#81B29A"}
for _, row in stakeholders.iterrows():
    col = colours_s.get(row["Priority"], "#999")
    ax2.scatter(row["Interest"], row["Influence"], s=200, c=col, zorder=3, edgecolors="white", linewidth=1.5)
    ax2.annotate(row["Stakeholder"], (row["Interest"], row["Influence"]),
                 textcoords="offset points", xytext=(5, 5), fontsize=7)
ax2.axhline(5, color="grey", linestyle="--", linewidth=0.8)
ax2.axvline(5, color="grey", linestyle="--", linewidth=0.8)
ax2.set_xlabel("Interest (1–10)")
ax2.set_ylabel("Influence (1–10)")
ax2.set_title("Stakeholder Power/Interest Grid")
ax2.set_xlim(0, 11); ax2.set_ylim(0, 11)
ax2.text(2, 2, "Low priority", fontsize=7, color="grey")
ax2.text(7, 8, "Manage closely", fontsize=7, color="grey")
ax2.text(2, 8, "Keep satisfied", fontsize=7, color="grey")
ax2.text(7, 2, "Keep informed", fontsize=7, color="grey")

# Chart 3: Before vs After comparison
ax3 = axes[2]
metrics = ["Total Time (hrs)", "Avg Pain Score", "Admin Touch Points", "Manual Steps"]
current_vals = [
    cs_df["time_hrs"].sum(),
    cs_df["pain_score"].mean(),
    cs_df[cs_df["actor"]=="Admin"].shape[0],
    cs_df["manual"].sum(),
]
future_vals = [
    fs_df["time_hrs"].sum(),
    fs_df["pain_score"].mean(),
    fs_df[fs_df["actor"]=="Admin"].shape[0] if "Admin" in fs_df["actor"].values else 0,
    fs_df["manual"].sum(),
]

# Normalise for radar-style bar
max_vals = [max(c,f)*1.1 for c,f in zip(current_vals, future_vals)]
curr_norm = [c/m*10 for c,m in zip(current_vals, max_vals)]
fut_norm  = [f/m*10 for f,m in zip(future_vals, max_vals)]

x = np.arange(len(metrics))
w = 0.35
ax3.bar(x - w/2, curr_norm, w, label="Current",  color="#E07A5F", alpha=0.85)
ax3.bar(x + w/2, fut_norm,  w, label="Proposed", color="#81B29A", alpha=0.85)
ax3.set_xticks(x)
ax3.set_xticklabels(metrics, fontsize=8, rotation=20, ha="right")
ax3.set_title("Current vs Proposed (Normalised Score)")
ax3.set_ylabel("Score (lower = better)")
ax3.legend(fontsize=8)

plt.tight_layout()
plt.savefig("process_improvement.png", dpi=150, bbox_inches="tight")
plt.show()
print("\n✅ Chart saved as process_improvement.png")
