import pandas as pd

def validate_inputs(*series: pd.Series):
    index = series[0].index
    for s in series:
        if not isinstance(s, pd.Series):
            raise TypeError("All inputs must be pandas Series.")
        if not s.index.equals(index):
            raise ValueError("All input Series must share the same index.")
