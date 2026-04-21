"""
optimizer.py
Funzioni di ottimizzazione portafoglio: Max Sharpe, Min Volatility,
Efficient Frontier.
"""

import numpy as np
import pandas as pd
from scipy.optimize import minimize


def _portfolio_return(w, mu):
    return w @ mu


def _portfolio_vol(w, cov):
    return np.sqrt(w @ cov @ w)


def _neg_sharpe(w, mu, cov, rf):
    ret = _portfolio_return(w, mu)
    vol = _portfolio_vol(w, cov)
    return -(ret - rf) / vol


def max_sharpe(mu, cov, rf=0.04):
    """
    Trova il portafoglio con massimo Sharpe Ratio.

    Args:
        mu:  array rendimenti annualizzati
        cov: matrice covarianza annualizzata
        rf:  risk-free rate (default 4%)

    Returns:
        dict con weights, return, volatility, sharpe
    """
    n = len(mu)
    w0 = np.ones(n) / n
    bounds = [(0, 1)] * n
    constraints = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}

    res = minimize(_neg_sharpe, w0, args=(mu, cov, rf),
                   method='SLSQP', bounds=bounds, constraints=constraints)

    w = res.x
    ret = _portfolio_return(w, mu)
    vol = _portfolio_vol(w, cov)

    return {
        'weights': w,
        'return': ret,
        'volatility': vol,
        'sharpe': (ret - rf) / vol
    }


def min_volatility(mu, cov):
    """
    Trova il portafoglio a minima varianza.

    Returns:
        dict con weights, return, volatility, sharpe
    """
    n = len(mu)
    w0 = np.ones(n) / n
    bounds = [(0, 1)] * n
    constraints = {'type': 'eq', 'fun': lambda w: np.sum(w) - 1}

    res = minimize(_portfolio_vol, w0, args=(cov,),
                   method='SLSQP', bounds=bounds, constraints=constraints)

    w = res.x
    ret = _portfolio_return(w, mu)
    vol = _portfolio_vol(w, cov)

    return {
        'weights': w,
        'return': ret,
        'volatility': vol
    }


def efficient_frontier(mu, cov, rf=0.04, n_points=50):
    """
    Calcola la frontiera efficiente come serie di portafogli ottimali.

    Returns:
        DataFrame con colonne: target_return, volatility
    """
    minvol = min_volatility(mu, cov)
    maxsharpe = max_sharpe(mu, cov, rf)

    target_returns = np.linspace(
        minvol['return'],
        maxsharpe['return'] * 1.3,
        n_points
    )

    frontier = []
    n = len(mu)
    w0 = np.ones(n) / n
    bounds = [(0, 1)] * n

    for target in target_returns:
        constraints = [
            {'type': 'eq', 'fun': lambda w: np.sum(w) - 1},
            {'type': 'eq', 'fun': lambda w, t=target: w @ mu - t}
        ]
        res = minimize(_portfolio_vol, w0, args=(cov,),
                       method='SLSQP', bounds=bounds,
                       constraints=constraints)
        frontier.append({
            'target_return': target,
            'volatility': np.sqrt(res.x @ cov @ res.x) if res.success else np.nan
        })

    return pd.DataFrame(frontier)


def regional_allocation(weights, tickers, region_map):
    """
    Calcola l'allocazione percentuale per regione.

    Args:
        weights:    array di pesi
        tickers:    lista di ticker
        region_map: dict {ticker: region}

    Returns:
        dict {region: total_weight}
    """
    w_series = pd.Series(weights, index=tickers)
    allocation = {}
    for region in set(region_map.values()):
        region_tickers = [t for t, r in region_map.items() if r == region]
        allocation[region] = w_series[w_series.index.isin(region_tickers)].sum()
    return allocation