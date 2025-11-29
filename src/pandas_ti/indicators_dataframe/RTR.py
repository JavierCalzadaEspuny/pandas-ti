import pandas as pd
from ..registry import register_indicator

@register_indicator(ti_type='dataframe', extended_name='Relative True Range')
def RTR(High: pd.Series, Low: pd.Series, Close: pd.Series) -> pd.Series:
    """
    Relative True Range (RTR)

    Calculates the Relative True Range indicator, a normalized measure of volatility.

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
    None

    Returns
    -------
    RTR : pd.Series
        Series containing the relative true range values.

    Examples
    --------
    >>> # Via accessor (auto-inject)
    >>> df['RTR'] = df.ti.RTR()
    >>> 
    >>> # Direct import (explicit)
    >>> import pandas_ti as ti
    >>> df['RTR'] = ti.RTR(High=df['High'], Low=df['Low'], Close=df['Close'])
    """
    High = High.astype(float)
    Low = Low.astype(float)
    Close = Close.astype(float)

    previous_close = Close.shift(1)
    previous_close.iloc[0] = Close.iloc[0]  # handle first value

    tr1 = (High - Low).abs()
    tr2 = (High - previous_close).abs()
    tr3 = (previous_close - Low).abs()

    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    rtr = tr / previous_close

    return rtr
