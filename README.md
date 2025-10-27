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

## Development

```bash
# Clone the repository
git clone https://github.com/JavierCalzadaEspuny/pandas-ti
cd pandas_ti

# Install in development mode
pip install -e .[dev]
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

**Javier Calzada Espuny**

- GitHub: [@JavierCalzadaEspuny](https://github.com/JavierCalzadaEspuny)
- Linkedin: [JavierCalzadaEspuny](https://www.linkedin.com/in/javiercalzadaespuny/)
- Repository: [pandas_ti](https://github.com/JavierCalzadaEspuny/pandas_ti)
