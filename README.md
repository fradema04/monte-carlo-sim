# Monte Carlo Simulation & Portfolio Optimization

Comprehensive application of Monte Carlo methods in quantitative finance,
covering asset price simulation, derivative pricing, and global portfolio
optimization across three continents (2015–2026).

## Research Questions

1. How well does Geometric Brownian Motion approximate real asset price dynamics?
2. Does Monte Carlo option pricing converge to the Black-Scholes analytical solution?
3. What is the benefit of global diversification over a European-only universe?

## Key Findings

- Monte Carlo option pricing converges to Black-Scholes within **0.04** price units
  at 100,000 simulations, using real ASML.AS parameters (μ=27.53%, σ=33.26%)
- The **global efficient frontier** dominates the European frontier at every
  volatility level — Global Max Sharpe **1.69** vs European **0.92**
- Optimal global allocation concentrates in **America (49.7%)** and **Asia (34.3%)**,
  marginalizing Europe (16.0%) — consistent with superior risk-adjusted returns
  in tech-heavy US and high-growth Asian markets
- Global minimum volatility portfolio achieves **9.4% annualized vol** vs **12.6%**
  European-only — a 25% reduction through international diversification

## Structure
├── data/
│   ├── download_data.py                   # Data download script
│   └── raw/                               # Gitignored
├── notebooks/
│   ├── 01_gbm_and_option_pricing.ipynb   # GBM simulation + MC option pricing
│   ├── 02_portfolio_europe.ipynb          # EU efficient frontier (68 assets)
│   └── 03_portfolio_global.ipynb          # Global frontier EU+US+Asia (161 assets)
├── src/
│   └── optimizer.py                       # Portfolio optimization module
├── results/                               # Output charts
└── requirements.txt

## Methodology

**Asset Price Simulation — Geometric Brownian Motion:**

$$S_t = S_0 \exp\left[\left(\mu - \frac{\sigma^2}{2}\right)t + \sigma W_t\right]$$

**European Call Option Pricing:**

$$C = e^{-rT} \mathbb{E}^{\mathbb{Q}}\left[\max(S_T - K, 0)\right]$$

**Portfolio Optimization — Max Sharpe:**

$$\max_w \frac{\mu_p - r_f}{\sigma_p} \quad \text{s.t.} \quad \sum_i w_i = 1, \quad w_i \geq 0$$

## Data

| Source | Universe | Assets |
|--------|----------|--------|
| Yahoo Finance | Europe (STOXX large caps) | 68 |
| Yahoo Finance | America (S&P 100 subset) | 65 |
| Yahoo Finance | Asia (Nikkei + Hang Seng) | 28 |

**Sample period:** January 2015 – December 2025 | **Frequency:** Daily

## Results

### GBM — 1000 Simulated Price Paths (ASML.AS)
![GBM](results/gbm_simulation.png)

### MC Option Pricing Convergence to Black-Scholes
![Option Pricing](results/mc_option_pricing.png)

### Efficient Frontier — European Universe
![EU Frontier](results/eu_efficient_frontier_final.png)

### Efficient Frontier — Europe vs Global
![Global Frontier](results/global_efficient_frontier.png)

## Requirements

```bash
conda create -n montecarlo python=3.11
conda activate montecarlo
pip install pandas numpy scipy matplotlib seaborn yfinance jupyter
```

## Author

Francesco — Economics & Finance, Università Bocconi  
Research interests: quantitative asset pricing, high-frequency factor models,
market microstructure