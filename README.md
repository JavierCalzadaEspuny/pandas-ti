# pandas_ti

[![PyPI version](https://badge.fury.io/py/pandas-ti.svg)](https://badge.fury.io/py/pandas-ti)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
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

```python
import pandas as pd
import pandas_ti
import yfinance as yf

# Get some market data
df = yf.Ticker("AAPL").history(period="1y")

# DataFrame indicators - automatic OHLCV detection
df['atr_14'] = df.ti.ATR(n=14)
df['rtr'] = df.ti.RTR()

# Series indicators - work on any Series
df['sma_20'] = df['Close'].ti.SMA(n=20)
df['ema_50'] = df['Close'].ti.EMA(n=50)

print(df[['Close', 'atr_14', 'sma_20', 'ema_50']].tail())
```

### Built-in Help System

```python
# List all available indicators
df.ti.indicators()

# Get detailed help for specific indicator
df.ti.help('ATR')

# Series indicators help
df['Close'].ti.help('SMA')
```

## Available Indicators

### DataFrame Indicators (require OHLCV data)

| Indicator | Description | Parameters |
|-----------|-------------|------------|
| **TR** | True Range | None |
| **ATR** | Average True Range | `n` (window size) |
| **RTR** | Relative True Range (normalized) | None |
| **ARTR** | Average Relative True Range | `n` (window size) |
| **SRTR** | Standardized Relative True Range | `n`, `N=1000`, `expand=True`, `method='cluster'`, `full=False` |

### Series Indicators (work on any Series)

| Indicator | Description | Parameters |
|-----------|-------------|------------|
| **SMA** | Simple Moving Average | `n` (window size) |
| **EMA** | Exponential Moving Average | `n` (span) |

## Examples

### Volatility Analysis

```python
import pandas as pd
import pandas_ti
import yfinance as yf

# Download data
df = yf.Ticker("AAPL").history(period="1y")

# Calculate volatility indicators
df['true_range'] = df.ti.TR()
df['atr_14'] = df.ti.ATR(n=14)
df['atr_21'] = df.ti.ATR(n=21)
df['relative_tr'] = df.ti.RTR()

# Advanced: Standardized volatility with HAC/Newey-West adjustment
df['srtr_iid'] = df.ti.SRTR(n=14, method='iid')
df['srtr_cluster'] = df.ti.SRTR(n=14, method='cluster')

print(df[['Close', 'true_range', 'atr_14', 'relative_tr', 'srtr_cluster']].tail())
```

### Moving Averages and Trend Analysis

```python
# Multiple timeframe moving averages
df['sma_10'] = df['Close'].ti.SMA(n=10)
df['sma_20'] = df['Close'].ti.SMA(n=20)
df['sma_50'] = df['Close'].ti.SMA(n=50)

# Exponential moving averages
df['ema_12'] = df['Close'].ti.EMA(n=12)
df['ema_26'] = df['Close'].ti.EMA(n=26)

# Golden Cross detection
df['golden_cross'] = (df['sma_50'] > df['sma_200']).astype(int)
```

### Custom Column Names

The library automatically detects OHLCV columns regardless of naming convention:

```python
# All these DataFrames work automatically
df_yahoo = yf.Ticker("AAPL").history(period="1mo")  # Capital case: Open, High, Low, Close
df_crypto = ...  # lowercase: open, high, low, close
df_custom = ...  # Short form: O, H, L, C

# All work the same way
df_yahoo['atr'] = df_yahoo.ti.ATR(n=14)
df_crypto['atr'] = df_crypto.ti.ATR(n=14)
df_custom['atr'] = df_custom.ti.ATR(n=14)
```

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

### Indicator Registration

Adding custom indicators is straightforward:

```python
from pandas_ti.registry import register_indicator

@register_indicator(ti_type='dataframe', extended_name='My Indicator')
def MY_INDICATOR(High, Low, Close, n=14):
    """
    My custom technical indicator.
    
    Parameters
    ----------
    n : int, default 14
        Lookback period
    """
    # Your calculation here
    return result
```

Once registered, the indicator is automatically available:

```python
df['my_ind'] = df.ti.MY_INDICATOR(n=20)
```

## Requirements

### Core Dependencies
- **Python** >= 3.9
- **pandas** >= 2.0.0
- **numpy** >= 1.24.0
- **rich** >= 13.0.0

### Optional Dependencies
- **scipy** >= 1.10.0 (for SRTR statistical calculations)
- **statsmodels** >= 0.14.0 (for HAC/Newey-West estimation)
- **yfinance** >= 0.2.0 (for examples and testing)

## Development

```bash
# Clone the repository
git clone https://github.com/JavierCalzadaEspuny/pandas_ti
cd pandas_ti

# Install in development mode
pip install -e .

# Run tests (if available)
pytest
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Javier Calzada Espuny**

- GitHub: [@JavierCalzadaEspuny](https://github.com/JavierCalzadaEspuny)
- Linkedin: [JavierCalzadaEspuny](https://www.linkedin.com/in/javiercalzadaespuny/)
- Repository: [pandas_ti](https://github.com/JavierCalzadaEspuny/pandas_ti)
