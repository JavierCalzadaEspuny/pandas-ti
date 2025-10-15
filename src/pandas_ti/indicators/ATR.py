import pandas as pd
from .TR import TR

def ATR(High: pd.Series, Low: pd.Series, Close: pd.Series, length: int = 14) -> pd.Series:
    """
    Average True Range (ATR) calculation.

    Parameters
    ----------
        High : pd.Series
            Series of high prices.
        Low : pd.Series
            Series of low prices.
        Close : pd.Series
            Series of close prices.
        length : int, optional
            Length of the ATR window. Default is 14.

    Returns
    -------
        ATR: pd.Series
            Series containing the ATR values.
    """
    tr = TR(High, Low, Close)
    atr = tr.rolling(window=length).mean()

    return atr