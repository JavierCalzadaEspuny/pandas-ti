# pandas_ti
Pandas accessor for technical indicators.

## Installation
```bash
pip install -e .
```

## Usage
```python
import pandas as pd
import pandas_ti

df = pd.read_csv('data.csv')
print(df.ti.TR())  # Automatically calculates True Range

# Customize columns
df.ti.set_column_mapping({'close': 'Adj Close'})

# List indicators
print(df.ti.available_indicators())
```

## Extend
Add a file in the `indicators/` directory with:
```python
def YourIndicator(high: pd.Series, ...) -> pd.Series:
```