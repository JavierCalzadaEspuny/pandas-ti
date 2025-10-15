import pandas as pd
import numpy as np
from scipy.stats import norm
from statsmodels.tsa.stattools import acovf
from .RTR import RTR
from typing import Literal


def _SRTR_iid(RTR: pd.Series, N: int = 1000, expand: bool = False, n: int = 14, full: bool = False):
    """
    Standardize rolling mean of log(Relative True Range) under the i.i.d. assumption.
    """
    df = pd.DataFrame({"RTR": RTR})

    # 1. Log-transform
    df['log_RTR'] = np.log(df['RTR'].clip(lower=1e-8))

    # 2. Rolling arithmetic mean of log(RTR)
    df['mu_n'] = df['log_RTR'].rolling(window=n).mean()

    # 3. Historical rolling mu/sigma
    if expand:
        df['mu_N'] = np.nan
        df['mu_N'].iloc[N-1:] = df['log_RTR'].iloc[N-1:].expanding().mean()
        df['sigma'] = np.nan
        df['sigma'].iloc[N-1:] = df['log_RTR'].iloc[N-1:].expanding().std(ddof=1)
    else:
        df['mu_N'] = df['log_RTR'].rolling(window=N).mean()
        df['sigma'] = df['log_RTR'].rolling(window=N).std(ddof=1)

    # 4. Z-score and percentile
    df['z_score'] = (df['mu_n'] - df['mu_N']) / (df['sigma'] / np.sqrt(n))

    # 5. Map to percentile (p value)
    df['p'] = norm.cdf(df['z_score'])

    if full:
        return df[["RTR", "mu_N", "sigma", "mu_n", "z_score", "p"]]
    else:
        return df["p"]



def _hac_variance(hist: np.ndarray, mu: float, L: int, n: int) -> float:
    """
    Compute the HAC / Newey-West variance estimator for the mean of a series.

    Parameters
    ----------
        hist : np.ndarray
            Historical data window
        mu : float
            Mean of historical data
        L : int
            Truncation lag for autocovariances
        n : int
            Sub-window size for rolling mean

    Returns
    -------
        variance : float
            HAC-adjusted variance of the rolling mean
    """
    # 1. Center data around mean
    diffs = hist - mu

    # 2. Compute autocovariances (use statsmodels for vectorized computation)
    gamma = acovf(diffs, nlag=L, adjusted=False, fft=False)

    # Bartlett weights: W0 = 1, Wk = 1 - k/(L+1)
    weights = np.concatenate([[1], 2 * (1 - np.arange(1, L+1)/(L+1))])

    # 4. Variance
    variance = np.dot(weights, gamma) / n

    return variance


def _SRTR_cluster(RTR: pd.Series, N: int = 1000, expand: bool = False, n: int = 14, L: int = None, full: bool = False):
    """
    Volatility metric using rolling arithmetic mean of log(RTR) with HAC / Newey-West adjustment.
    """
    if L is None:
        L = n - 1

    df = pd.DataFrame({"RTR": RTR})

    # 1. Log-transform
    df['log_RTR'] = np.log(df['RTR'].clip(lower=1e-8))

    # 2. Short-term rolling mean
    df['mu_n'] = df['log_RTR'].rolling(window=n).mean()

    # 3. Long-term mean (rolling or expanding after N)
    if expand:
        df['mu_N'] = np.nan
        df['mu_N'].iloc[N-1:] = df['log_RTR'].iloc[N-1:].expanding().mean()

        # Vectorized HAC variance for expanding windows
        temp = df['log_RTR'].iloc[N-1:].expanding(min_periods=n).apply(
            lambda w: np.sqrt(_hac_variance(w.values, np.mean(w.values), L, n))
        )
        df['sigma'] = np.nan
        df['sigma'].iloc[N-1:] = temp
    else:
        df['mu_N'] = df['log_RTR'].rolling(window=N).mean()

        # Vectorized HAC variance for rolling windows
        df['sigma'] = df['log_RTR'].rolling(window=N).apply(
            lambda w: np.sqrt(_hac_variance(w.values, np.mean(w.values), L, n))
        )

    # Match original NaN placement for consistency
    start_idx = (N - 1 if expand else N - 1) + (n - 1)
    df['sigma'].iloc[:start_idx] = np.nan

    # 4. Z-score where all components are available
    mask = df['mu_n'].notna() & df['mu_N'].notna() & df['sigma'].notna()
    df['z_score'] = np.nan
    df.loc[mask, 'z_score'] = (df.loc[mask, 'mu_n'] - df.loc[mask, 'mu_N']) / df.loc[mask, 'sigma']

    # 5. Percentile
    df['p'] = norm.cdf(df['z_score'])

    if full:
        return df[["RTR", "mu_N", "sigma", "mu_n", "z_score", "p"]]
    else:
        return df['p']


def SRTR(
    High: pd.Series,
    Low: pd.Series,
    Close: pd.Series,
    N: int = 1000,
    expand: bool = False,
    n: int = 14,
    method: Literal['iid', 'cluster'] = "cluster",
    L: int = None,
    full: bool = False
    ):
    """
    Standardize rolling mean of log(True Range) using either i.i.d. or HAC/Newey-West adjustment.

    This function computes a volatility metric by standardizing the short-term rolling mean of log(True Range)
    against its long-term mean and standard deviation, using either the i.i.d. assumption or a HAC/Newey-West
    estimator to account for autocorrelation.

    Steps:
        1. Log-transform the relative true range to approximate normality.
        2. Compute a short-term rolling mean (mu_n) of log(RTR) over n periods.
        3. Compute a long-term rolling mean (mu_N) and standard deviation (sigma) of log(RTR) over N periods.
        4. Standardize mu_n using the long-term mean and standard deviation:
            - If method="iid": sigma is rescaled by sqrt(n).
            - If method="autocorr": sigma is estimated using a HAC/Newey-West estimator with truncation lag L.
        5. Map the z-score to its percentile under the standard normal distribution.

    Parameters
    ----------
        High : pd.Series
            Series of high prices.
        Low : pd.Series
            Series of low prices.
        Close : pd.Series
            Series of close prices.
        N : int, optional
            Window size for historical mean and standard deviation (default=1000).
        expand : bool, optional
            If True, use expanding window for long-term mean and std (default=False).
        n : int, optional
            Window size for short-term rolling mean (default=10).
        method : Literal['iid', 'cluster'], optional
            "iid" for independent assumption, "cluster" for HAC/Newey-West adjustment (default="cluster").
        L : int, optional
            Truncation lag for HAC estimator (only used if method="cluster").
        full : bool, optional
            If True, return full DataFrame with intermediate values; if False, return only percentiles (default=False).

    Returns
    -------
        if full is True:
            pd.DataFrame with columns:
        if full is False:
            pd.Series of percentiles.
    """
    rtr = RTR(High, Low, Close)

    if len(rtr) <= N:
        raise ValueError("Length of series must be >= N.")
    if N <= n:
        raise ValueError("N must be greater than n.") 
    if method not in ["iid", "cluster"]:
        raise ValueError("Method must be either 'iid' or 'cluster'.")

    if n == 1 or method == "iid":
        return _SRTR_iid(rtr, N, expand, n, full)

    elif method == "cluster":
        return _SRTR_cluster(rtr, N, expand, n, L, full)
        


