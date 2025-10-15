import pandas as pd
from .RTR import RTR

def ARTR(High: pd.Series, Low: pd.Series, Close: pd.Series, length: int = 14) -> pd.Series:
    """
    Average Relative True Range (ARTR) calculation.

    Parameters
    ----------
        High : pd.Series
            Series of high prices.
        Low : pd.Series
            Series of low prices.
        Close : pd.Series
            Series of close prices.
        length : int, optional
            Length of the ARTR window. Default is 14.

    Returns
    -------
        ARTR: pd.Series
            Series containing the ARTR values.
    """
    rtr = RTR(High, Low, Close)
    artr = rtr.rolling(window=length).mean()

    return artr