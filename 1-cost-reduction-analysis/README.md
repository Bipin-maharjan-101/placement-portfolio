# Project 1 — Cost Reduction Analysis

## Overview
Analyses 3 years of departmental cost data for a mid-size retail company. Identifies departments consistently overspending their budget, calculates potential savings, and produces actionable recommendations — mirroring a real management consulting deliverable.

## What it does
- Loads 3 years of budget vs actual cost data across 8 departments
- Calculates variance (£ and %) for each year
- Flags departments with consistent overspend (>3% above budget)
- Computes year-on-year cost growth rates
- Estimates total potential savings if budgets are met
- Outputs a printed management report + 4-panel visualisation

## Skills demonstrated
- Financial variance analysis
- Budget management and cost control
- Data visualisation (Matplotlib)
- Report writing and recommendations

## How to run
```bash
pip install pandas matplotlib numpy
python main.py
```

## Sample output
```
TOTAL COMPANY COSTS BY YEAR
2022  Budget: £2,400,000  |  Actual: £2,437,000  |  Over by: £37,000 (1.5%)
2023  Budget: £2,510,000  |  Actual: £2,614,000  |  Over by: £104,000 (4.1%)
2024  Budget: £2,600,000  |  Actual: £2,729,000  |  Over by: £129,000 (5.0%)
```
