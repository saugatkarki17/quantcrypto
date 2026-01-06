# Crypto Decoupling Detector (Alpha Hunter)

### A Regime-Based Quantitative Dashboard for Digital Assets

---

## Executive Summary
The **Crypto Decoupling Detector** is a real-time quantitative tool designed to identify **Unique Alpha** in the digital asset market. 

In high-volatility regimes, crypto assets often move in lockstep (Correlation $\approx$ 1), rendering traditional diversification useless. This dashboard calculates **Rolling Correlation Windows** to detect moments when specific assets "decouple" from the benchmark (Bitcoin), signaling potential independent price action (Alpha) or specific risk events.

---

## Investment Thesis
Most retail analytics focus on price prediction. This tool focuses on **Market Structure Analysis**.

1.  **The Problem (Systematic Risk):** During macro panic events, correlation across the crypto sector approaches 1.0. Buying "diverse" coins during these times does not reduce risk.
2.  **The Opportunity (Idiosyncratic Alpha):** The most profitable trades occur when an asset breaks its correlation with the broader market due to fundamental catalysts.
3.  **The Solution:** By moving from static correlation to **Dynamic Rolling Correlation**, this tool highlights exactly *when* an asset is trading on its own fundamentals rather than following the macro trend.

---

## Features

### 1. Dynamic Regime Detection
* **Lockstep Regime ($r > 0.8$):** High systematic risk. The asset is just mimicking Bitcoin.
* **Decoupled Regime ($r < 0.5$):** High idiosyncratic behavior. Potential Alpha opportunity.
* **Inverse Regime ($r < 0$):** The asset is acting as a hedge.

### 2. Rolling Correlation Engine
Calculates the Pearson Correlation Coefficient ($r$) over a user-defined sliding window (default 30 days). This removes noise and visualizes the *trend* of relationships, not just the snapshot.

### 3. Institutional Visualization
* **Correlation Matrix Heatmaps:** Instant view of sector-wide contagion.
* **Normalized Performance:** Relative strength comparison starting from a common base (Base 100).

---

## Methodology

The core engine relies on the **Pearson Correlation Coefficient** applied to a rolling window of log-returns:

$$
r_{xy} = \frac{\sum_{i=1}^{n}(x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum_{i=1}^{n}(x_i - \bar{x})^2} \sqrt{\sum_{i=1}^{n}(y_i - \bar{y})^2}}
$$

Where:
* $x$ = Benchmark Returns (BTC)
* $y$ = Asset Returns (e.g., SOL, ETH)
* $n$ = Rolling Window Size (e.g., 30 Days)

---

## Tech Stack
* **Core Logic:** Python (Pandas, NumPy)
* **Data Feed:** yfinance (Yahoo Finance API)
* **Visualization:** Plotly (Interactive financial charting)
* **Frontend:** Streamlit (Web-based dashboarding)

---

## 🚀 Quick Start

**1. Clone the repository**
```bash
git clone [https://github.com/YOUR_USERNAME/crypto-alpha-hunter.git](https://github.com/YOUR_USERNAME/crypto-alpha-hunter.git)
cd crypto-alpha-hunter