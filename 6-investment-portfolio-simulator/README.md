# Project 6 — Investment Portfolio Simulator

## Overview
Simulates managing a £10,000 portfolio of UK blue-chip stocks (FTSE 100) over 12 months. Tracks performance, calculates returns vs FTSE 100 benchmark, and maintains a monthly decision journal — mirroring real buy-side analyst work.

## Features
- 6 UK blue-chip holdings (Lloyds, Shell, AstraZeneca, Tesco, Barclays, Vodafone)
- Monthly price simulation with realistic drift and volatility
- FTSE 100 benchmark comparison and alpha calculation
- P&L tracking per holding and total portfolio
- Monthly investment decision journal with reasoning
- 4-panel dashboard: cumulative returns, allocation, stock returns, portfolio value

## How to run
```bash
pip install pandas matplotlib numpy
python main.py
```

## To use real market data (optional)
```bash
pip install yfinance
```
Then replace the `simulate_prices()` function with `yfinance.download()` calls.

## Skills demonstrated
- Investment portfolio construction and management
- Performance benchmarking and alpha calculation
- Financial markets knowledge (FTSE 100, UK equities)
- Decision-making with documented rationale
- Risk management and rebalancing
