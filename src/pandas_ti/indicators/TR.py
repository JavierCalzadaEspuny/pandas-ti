import pandas as pd

def TR(High: pd.Series, Low: pd.Series, Close: pd.Series) -> pd.Series:
    """
    True Range (TR) is a volatility indicator that measures the range of price movement for each session.

    It is calculated as the maximum of three values:
        1. The difference between the current high and the current low.
        2. The absolute difference between the current high and the previous close.
        3. The absolute difference between the current low and the previous close.

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
        TR: pd.Series: 
            Series of true range values.
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

    return tr
