# Project 7 — Data Dashboard (UK Retail Sales Analysis)

## Overview
Analyses 3 years of UK retail sales data across 6 categories. Produces both a static Matplotlib dashboard and a fully interactive HTML dashboard — demonstrating business intelligence and data storytelling skills directly relevant to analyst roles.

## Two dashboards included
1. **dashboard.html** — Open in any browser. Interactive charts (Chart.js): trend line, category mix pie, YoY comparison, stacked bar breakdown. No server required.
2. **main.py** — Runs console analysis report + saves static PNG dashboard.

## KPIs tracked
- Latest month total sales
- Year-on-year growth
- Category mix (Food, Clothing, Electronics, Home, Health, Sports)
- Seasonal patterns and peak month analysis
- Quarterly breakdown

## How to run
```bash
# Static dashboard + data export
pip install pandas matplotlib numpy
python main.py

# Interactive dashboard — just open in browser:
open dashboard.html   # macOS
start dashboard.html  # Windows
```

## Skills demonstrated
- Business intelligence and KPI dashboards
- Data storytelling and narrative writing
- Interactive web-based visualisation (Chart.js)
- Seasonality and trend analysis
- ONS-style data interpretation
