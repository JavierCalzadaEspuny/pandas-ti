# pandas_ti

[![PyPI version](https://badge.fury.io/py/pandas-ti.svg)](https://badge.fury.io/py/pandas-ti)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Project Description

pandas_ti is a lightweight and extensible technical indicators library for pandas DataFrames. Its main objective is to provide a simple and automated interface for calculating technical indicators on financial data, eliminating the need to manually specify OHLCV (Open, High, Low, Close, Volume) column names.

The library is characterized by:
- Automatic detection of OHLCV columns with multiple naming conventions
- Automatic indicator registration system using decorators
- Consistent interface through the `df.ti` accessor
- Integrated documentation for all indicators
- Extensible architecture that allows adding new indicators easily

## Installation

### From PyPI
```bash
pip install pandas_ti
```

### For Development
```bash
git clone https://github.com/JavierCalzadaEspuny/pandas_ti
cd pandas_ti
pip install -e .
```

## Usage

### Basic Usage

```python
import pandas as pd
import pandas_ti

# Load data
df = pd.read_csv('financial_data.csv')

# Calculate indicators
df['TR'] = df.ti.TR()
df['ATR'] = df.ti.ATR(length=14)
```

### Available Indicators List

```python
# View all available indicators
print(df.ti.available_indicators)
```

### Help and Documentation

```python
# View documentation for a specific indicator
df.ti.help('ATR')

# View all available indicators
df.ti.help()
```

### Complete Example

```python
import pandas as pd
import pandas_ti
import yfinance as yf

# Get data from Yahoo Finance
df = yf.Ticker("AAPL").history(period="1y")

# Calculate multiple indicators
df['TR'] = df.ti.TR()
df['ATR_14'] = df.ti.ATR(length=14)
df['ATR_14'] = df.ti.ATR(length=14)

print(df[['TR', 'ATR_14', 'ATR_14']].tail())
```

## Technical Details

### Supported Columns

The library automatically detects OHLCV columns using the following name variations:

| Column | Accepted Variations |
|--------|-------------------|
| Open   | `Open`, `OPEN`, `open`, `O`, `o` |
| High   | `High`, `HIGH`, `high`, `H`, `h` |
| Low    | `Low`, `LOW`, `low`, `L`, `l` |
| Close  | `Close`, `CLOSE`, `close`, `C`, `c` |
| Volume | `Volume`, `VOLUME`, `volume`, `Vol`, `vol`, `V`, `v` |

### Custom Column Mapping

For DataFrames with non-standard column names:

```python
# Configure custom mapping
df.ti.set_column_mapping({
    'Open': 'opening_price',
    'High': 'high_price',
    'Low': 'low_price',
    'Close': 'closing_price',
    'Volume': 'volume_traded'
})
```

## Requirements

### System Requirements
- Python >= 3.9

### Dependencies
- pandas >= 2.0
- numpy >= 1.22
- scipy >= 1.10
- statsmodels >= 0.14

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

**Javier Calzada Espuny**

- GitHub: [@JavierCalzadaEspuny](https://github.com/JavierCalzadaEspuny)
- Repository: [pandas_ti](https://github.com/JavierCalzadaEspuny/pandas_ti)