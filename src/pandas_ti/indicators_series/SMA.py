import pandas as pd
from ..registry import register_indicator

@register_indicator(ti_type='series', extended_name='Simple Moving Average')
def SMA(series: pd.Series, n: int) -> pd.Series:
    """
    Simple Moving Average (SMA)

    Calculates the arithmetic mean of the series values over the last n periods.

    Parameters
    ----------
    n : int, optional
        Length of the window.

    Returns
    -------
    SMA : pd.Series
        Series containing the SMA values.

    Examples
    --------
    >>> # Via accessor
    >>> df['SMA_14'] = df['Close'].ti.SMA(n=14)
    >>> 
    >>> # Direct import
    >>> import pandas_ti as ti
    >>> df['SMA_14'] = ti.SMA(series=df['Close'], n=14)
    """
    return series.rolling(window=n).mean()
    