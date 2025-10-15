import pandas as pd

def RTR(High: pd.Series, Low: pd.Series, Close: pd.Series) -> pd.Series:
    """
    Relative True Range (RTR) is a volatility indicator that measures the relative range of price movement for (TR).

    Parameters
    ----------
        High: pd.Series: 
            Series of high prices.
        Low: pd.Series: 
            Series of low prices.
        Close: pd.Series: 
            Series of close prices.

    Returns
    -------
        RTR: pd.Series: 
            Series containing the relative true range values.
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
