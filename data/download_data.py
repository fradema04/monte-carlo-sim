"""
download_data.py
Scarica e salva localmente i prezzi azionari per tre universi:
- Europa: STOXX Europe 50 (proxy con titoli liquidi)
- America: S&P 100
- Asia: Nikkei 225 top 30 + Hang Seng top 20
"""

import yfinance as yf
import pandas as pd
import os

START = '2015-01-01'
END   = '2026-01-01'

os.makedirs('raw', exist_ok=True)

# ── EUROPA ──────────────────────────────────────────────────────────────────
europe_tickers = [
    # Olanda
    'ASML.AS', 'HEIA.AS', 'INGA.AS', 'PHIA.AS', 'NN.AS',
    # Germania
    'SAP.DE', 'SIE.DE', 'ALV.DE', 'DTE.DE', 'MUV2.DE',
    'BMW.DE', 'MBG.DE', 'BAS.DE', 'BAYN.DE', 'DBK.DE',
    'ADS.DE', 'VOW3.DE', 'RWE.DE', 'EON.DE', 'HEN3.DE',
    # Francia
    'MC.PA', 'OR.PA', 'SAN.PA', 'BNP.PA', 'AIR.PA',
    'DG.PA', 'RI.PA', 'KER.PA', 'CS.PA', 'ORA.PA',
    'VIE.PA', 'SGO.PA', 'DSY.PA', 'CAP.PA', 'EL.PA',
    # Svizzera
    'NESN.SW', 'NOVN.SW', 'ROG.SW', 'ABBN.SW', 'ZURN.SW',
    'UBSG.SW', 'CSGN.SW', 'SREN.SW', 'LONN.SW', 'GIVN.SW',
    # UK
    'SHEL.L', 'AZN.L', 'HSBA.L', 'BP.L', 'ULVR.L',
    'GSK.L', 'RIO.L', 'DGE.L', 'LSEG.L', 'BT-A.L',
    # Spagna
    'ITX.MC', 'SAN.MC', 'BBVA.MC', 'REP.MC', 'IBE.MC',
    # Italia
    'ENI.MI', 'ISP.MI', 'UCG.MI', 'ENEL.MI', 'G.MI',
    # Danimarca / Svezia / Finlandia
    'NOVO-B.CO', 'ERIC-B.ST', 'VOLV-B.ST', 'NDA-SE.ST', 'NOKIA.HE',
]

# ── AMERICA ─────────────────────────────────────────────────────────────────
america_tickers = [
    # Tech
    'AAPL', 'MSFT', 'NVDA', 'GOOGL', 'META',
    'AMZN', 'TSLA', 'AMD', 'INTC', 'QCOM',
    'ORCL', 'IBM', 'CRM', 'ADBE', 'NOW',
    # Finance
    'JPM', 'BAC', 'WFC', 'GS', 'MS',
    'BLK', 'AXP', 'V', 'MA', 'SPGI',
    # Healthcare
    'JNJ', 'UNH', 'PFE', 'MRK', 'ABBV',
    'LLY', 'TMO', 'ABT', 'MDT', 'BMY',
    # Energy
    'XOM', 'CVX', 'COP', 'SLB', 'EOG',
    # Consumer
    'PG', 'KO', 'PEP', 'WMT', 'HD',
    'MCD', 'NKE', 'SBUX', 'TGT', 'COST',
    # Industrial
    'GE', 'BA', 'CAT', 'HON', 'MMM',
    'LMT', 'RTX', 'DE', 'UPS', 'FDX',
    # Utilities / Telecom
    'NEE', 'DUK', 'SO', 'T', 'VZ',
]

# ── ASIA ────────────────────────────────────────────────────────────────────
asia_tickers = [
    # Giappone
    '7203.T',  # Toyota
    '6758.T',  # Sony
    '9984.T',  # SoftBank
    '8306.T',  # Mitsubishi UFJ
    '6861.T',  # Keyence
    '9432.T',  # NTT
    '7974.T',  # Nintendo
    '4063.T',  # Shin-Etsu Chemical
    '8035.T',  # Tokyo Electron
    '6954.T',  # Fanuc
    '4502.T',  # Takeda
    '9433.T',  # KDDI
    '8058.T',  # Mitsubishi Corp
    '6098.T',  # Recruit
    '7267.T',  # Honda
    # Hong Kong / Cina
    '0700.HK', # Tencent
    '9988.HK', # Alibaba
    '0941.HK', # China Mobile
    '1299.HK', # AIA
    '0005.HK', # HSBC HK
    '2318.HK', # Ping An
    '0388.HK', # Hong Kong Exchanges
    '1398.HK', # ICBC
    '0883.HK', # CNOOC
    '3690.HK', # Meituan
    # Korea / Taiwan / Australia
    '005930.KS', # Samsung
    '000660.KS', # SK Hynix
    'TSM',        # TSMC (ADR)
    'BHP.AX',     # BHP
    'CBA.AX',     # Commonwealth Bank
]


def download_universe(tickers, name):
    print(f"\nDownloading {name} ({len(tickers)} tickers)...")
    prices = yf.download(tickers, start=START, end=END, auto_adjust=True)['Close']
    
    # Rimuovi colonne con troppi NaN (>20% mancanti)
    threshold = 0.20
    prices = prices.loc[:, prices.isnull().mean() < threshold]
    
    # Forward fill per NaN residui (festività locali)
    prices = prices.ffill().dropna()
    
    returns = prices.pct_change().dropna()
    
    prices.to_csv(f'raw/prices_{name.lower()}.csv')
    returns.to_csv(f'raw/returns_{name.lower()}.csv')
    
    print(f"  Saved {prices.shape[1]} tickers x {len(prices)} days")
    print(f"  Prices:  raw/prices_{name.lower()}.csv")
    print(f"  Returns: raw/returns_{name.lower()}.csv")
    
    return prices, returns


if __name__ == '__main__':
    prices_eu, ret_eu = download_universe(europe_tickers, 'europe')
    prices_us, ret_us = download_universe(america_tickers, 'america')
    prices_as, ret_as = download_universe(asia_tickers, 'asia')
    
    print("\nAll data downloaded successfully.")
    print(f"Europe:  {ret_eu.shape[1]} assets")
    print(f"America: {ret_us.shape[1]} assets")
    print(f"Asia:    {ret_as.shape[1]} assets")