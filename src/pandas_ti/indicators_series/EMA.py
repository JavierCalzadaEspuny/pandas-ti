import pandas as pd
from ..registry import register_indicator

@register_indicator(ti_type='series', extended_name='Exponential Moving Average')
def EMA(series: pd.Series, n: int) -> pd.Series:
    """
    Exponential Moving Average (EMA)

    Calculates the Exponential Moving Average of a pandas Series over the last `n` periods.
    The EMA gives more weight to recent prices, making it more responsive to new information.

    Parameters
    ----------
    n : int
        The window size for the moving average.

    Returns
    -------
    pd.Series
        Series containing the EMA values, aligned with the input index.

    Examples
    --------
    >>> EMA_14 = df['Close'].ti.EMA(n=14)
    """
    return series.ewm(span=n, adjust=False).mean()