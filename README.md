# pandas_ti

[![PyPI version](https://badge.fury.io/py/pandas-ti.svg)](https://badge.fury.io/py/pandas-ti)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A lightweight and extensible technical analysis library for pandas DataFrames and Series.

## Features

- **Zero Configuration** - Automatic OHLCV column detection with multiple naming conventions
- **Pandas Native** - Seamless integration via `.ti` accessor for DataFrames and Series
- **Self-Documenting** - Built-in help system with rich console output
- **Extensible** - Easy to add custom indicators with decorator pattern
- **Fast & Lightweight** - Minimal dependencies, maximum performance

## Quick Start

### Installation

```bash
pip install pandas-ti
```

### Basic Usage

There are two ways to use indicators in pandas_ti:

#### 1. Accessor Pattern (Recommended)

Use the `.ti` accessor for seamless integration with pandas. High and Low columns are auto-injected from your DataFrame.

```python
import pandas as pd
import pandas_ti
import yfinance as yf

# Get market data
df = yf.Ticker("AAPL").history(period="1y")

# DataFrame indicators - automatic OHLCV detection
df['ATR_14'] = df.ti.ATR(n=14)
df['RTR'] = df.ti.RTR()
zz = df.ti.ZigZag(pct=0.05)

# Series indicators - work on any Series
df['SMA_20'] = df['Close'].ti.SMA(n=20)
df['EMA_50'] = df['Close'].ti.EMA(n=50)
```

#### 2. Direct Import (Manual)

Import indicators directly for more control. You must explicitly pass the required data.

```python
import pandas_ti as ti
import yfinance as yf

df = yf.Ticker("AAPL").history(period="1y")

# Import and use indicators directly
from pandas_ti import ATR, RTR, ZigZag, SMA, EMA

# DataFrame indicators - must specify columns
df['ATR_14'] = ATR(High=df['High'], Low=df['Low'], Close=df['Close'], n=14)
df['RTR'] = RTR(High=df['High'], Low=df['Low'], Close=df['Close'])
zz = ZigZag(High=df['High'], Low=df['Low'], pct=0.05)

# Series indicators - pass Series directly
df['SMA_20'] = SMA(series=df['Close'], n=20)
df['EMA_50'] = EMA(series=df['Close'], n=50)

# Alternative: use package-level access
df['ATR_14'] = ti.ATR(High=df['High'], Low=df['Low'], Close=df['Close'], n=14)
```

### Built-in Help System

#### Help with Accessor Pattern

```python
# List all available indicators
df.ti.indicators()
df['Close'].ti.indicators()

# Get detailed help for specific indicator
df.ti.help('ATR')
df['Close'].ti.help('SMA')
```

#### Help with Direct Import

```python
from pandas_ti import ZigZag, ATR

# Using help() function
help(ZigZag)
help(ATR)

# Using __doc__ attribute
print(ZigZag.__doc__)
print(ATR.__doc__)
```

## Available Indicators

### DataFrame Indicators (require OHLCV data)

These indicators require High, Low, and Close columns (auto-detected with accessor pattern).

| Indicator | Description | Parameters | Return Type |
|-----------|-------------|------------|-------------|
| **TR** | True Range | None | `pd.Series` |
| **ATR** | Average True Range | `n` (window size) | `pd.Series` |
| **RTR** | Relative True Range  | None | `pd.Series` |
| **ARTR** | Average Relative True Range | `n` (window size) | `pd.Series` |
| **SRTR** | Standardized Relative True Range | `n`, `N=1000`, `expand=False`, `method='cluster'` | `SRTRClass` |
| **ZigZag** | Significant price reversals detector | `pct` (percentage threshold) | `ZigZagClass` |

### Series Indicators (work on any Series)

These indicators work on any pandas Series.

| Indicator | Description | Parameters | Return Type |
|-----------|-------------|------------|-------------|
| **SMA** | Simple Moving Average | `n` (window size) | `pd.Series` |
| **EMA** | Exponential Moving Average | `n` (span) | `pd.Series` |


## Technical Details

### Automatic Column Detection

The library automatically detects OHLCV columns using common naming variations:

| Column Type | Accepted Names |
|-------------|----------------|
| **Open**    | `Open`, `OPEN`, `open`, `O`, `o` |
| **High**    | `High`, `HIGH`, `high`, `H`, `h` |
| **Low**     | `Low`, `LOW`, `low`, `L`, `l` |
| **Close**   | `Close`, `CLOSE`, `close`, `C`, `c` |
| **Volume**  | `Volume`, `VOLUME`, `volume`, `Vol`, `vol`, `V`, `v` |


## Requirements

### Core Dependencies
- **Python** >= 3.12
- **pandas** >= 2.3.3
- **numpy** >= 2.3.3
- **rich** >= 14.2.0
- **scipy** >= 1.16.2
- **statsmodels** >= 0.14.5

### Optional dependencies
- **yfinance** >= 0.2.66 (for examples and testing)
- **matplotlib** >= 3.10.7 (for visualization)
- **mplfinance** >= 0.12.10b0 (for financial charts)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Javier Calzada Espuny**

- GitHub: [@JavierCalzadaEspuny](https://github.com/JavierCalzadaEspuny)
- Linkedin: [JavierCalzadaEspuny](https://www.linkedin.com/in/javiercalzadaespuny/)
- Repository: [pandas_ti](https://github.com/JavierCalzadaEspuny/pandas_ti)
