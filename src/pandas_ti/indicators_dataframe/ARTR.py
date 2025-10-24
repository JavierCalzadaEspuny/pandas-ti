import pandas as pd
from .RTR import RTR
from ..registry import register_indicator


@register_indicator(ti_type='dataframe', extended_name='Average Relative True Range')
def ARTR(High: pd.Series, Low: pd.Series, Close: pd.Series, n: int) -> pd.Series:
    """
    Average Relative True Range (ARTR)

    Calculates the arithmetic average of the Relative True Range over the last n periods.

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
    ARTR : pd.Series
        Series containing the ARTR values.

    Examples
    --------
    >>> df['ARTR_14'] = df.ti.ARTR(n=14)
    """
    rtr = RTR(High, Low, Close)
    artr = rtr.rolling(window=n).mean()

    return artr