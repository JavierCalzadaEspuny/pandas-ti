import pandas as pd
from .TR import TR
from ..registry import register_indicator

@register_indicator(ti_type='dataframe', extended_name='Average True Range')
def ATR(High: pd.Series, Low: pd.Series, Close: pd.Series, n: int) -> pd.Series:
    """
    Average True Range (ATR)

    Calculates the arithmetic average of the True Range over the last n periods.

    Required Columns
    ----------------
    High : pd.Series
        Series of high prices (Automatically injected).
    Low : pd.Series
        Series of low prices (Automatically injected).
    Close : pd.Series
        Series of close prices (Automatically injected).

    Parameters
    ----------
    n : int, optional
        Length of the window.

    Returns
    -------
    ATR : pd.Series
        Series containing the ATR values.

    Examples
    --------
    >>> # Via accessor (auto-inject)
    >>> df['ATR_14'] = df.ti.ATR(n=14)
    >>> 
    >>> # Direct import (explicit)
    >>> import pandas_ti as ti
    >>> df['ATR_14'] = ti.ATR(High=df['High'], Low=df['Low'], Close=df['Close'], n=14)
    """
    tr = TR(High, Low, Close)
    atr = tr.rolling(window=n).mean()

    return atr