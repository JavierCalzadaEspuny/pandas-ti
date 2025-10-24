import pandas as pd
from ..registry import register_indicator

@register_indicator(ti_type='dataframe', extended_name='True Range')
def TR(High: pd.Series, Low: pd.Series, Close: pd.Series) -> pd.Series:
    """
    True Range (TR)

    Compute the True Range, a standard measure of price volatility. 
    For each row the TR is the maximum of the absolute values of the following three values:
      1. High - Low
      2. High - Previous Close
      3. Previous Close - Low

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
    TR: pd.Series
        Series of True Range values aligned with the input index. 

    Examples
    --------
    >>> df['TR'] = df.ti.TR()
    """
    High = High.astype(float)
    Low = Low.astype(float)
    Close = Close.astype(float)

    previous_close = Close.shift(1)

    tr1 = (High - Low).abs()
    tr2 = (High - previous_close).abs()
    tr3 = (previous_close - Low).abs()

    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    return tr
