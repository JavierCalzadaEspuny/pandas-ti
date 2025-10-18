# pandas_ti 📈

[![PyPI version](https://badge.fury.io/py/pandas-ti.svg)](https://badge.fury.io/py/pandas-ti)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**pandas_ti** is a lightweight, extensible technical indicators library for pandas DataFrames with automatic OHLCV column detection and mapping.

## ✨ Key Features

- 🎯 **Automatic Column Mapping**: Works with any DataFrame structure - automatically detects `Open`, `High`, `Low`, `Close`, `Volume` columns and their variations
- 🔧 **Easy to Use**: Simple pandas accessor syntax `df.ti.ATR()`
- 📚 **Self-Documenting**: Built-in help system with `help()` for each indicator
- 🚀 **Extensible**: Add custom indicators by simply decorating a function
- 🎨 **Clean API**: No need to specify column names for each call

---

## 📦 Installation

```bash
pip install pandas_ti
```

For development:
```bash
git clone https://github.com/JavierCalzadaEspuny/pandas_ti
cd pandas_ti
pip install -e .
```

---

## 🚀 Quick Start

```python
import pandas as pd
import pandas_ti

# Load your data
df = pd.read_csv('your_data.csv')

# Automatically uses the right columns
df['TR'] = df.ti.TR()
df['ATR_14'] = df.ti.ATR(length=14)
df['SRTR'] = df.ti.SRTR(N=1000, n=14)

# Get help on any indicator
df.ti.help('SRTR')

# List all available indicators
print(df.ti.available_indicators)
```

### Works with any column naming convention:

```python
# Standard naming
df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']

# All caps
df.columns = ['DATE', 'OPEN', 'HIGH', 'LOW', 'CLOSE', 'VOLUME']

# Single letters
df.columns = ['date', 'O', 'H', 'L', 'C', 'V']

# All work automatically!
df.ti.ATR(length=14)
```

### Custom column mapping:

```python
# For non-standard column names
df.ti.set_column_mapping({
    'High': 'HighPrice',
    'Low': 'LowPrice',
    'Close': 'ClosePrice'
})
```

---

## 🔧 Technical Details

### Column Detection

The library automatically detects OHLCV columns by trying common variations:

| Standard | Variations |
|----------|------------|
| Open     | `Open`, `OPEN`, `open`, `O`, `o` |
| High     | `High`, `HIGH`, `high`, `H`, `h` |
| Low      | `Low`, `LOW`, `low`, `L`, `l` |
| Close    | `Close`, `CLOSE`, `close`, `C`, `c` |
| Volume   | `Volume`, `VOLUME`, `volume`, `Vol`, `vol`, `V`, `v` |

### Requirements

- Python >= 3.9
- pandas >= 2.0
- numpy >= 1.22
- scipy >= 1.10
- statsmodels >= 0.14

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built on top of pandas' powerful DataFrame accessor system
- Inspired by the need for a personal, clean, extensible technical indicators library

---

## 📮 Contact

**Javier Calzada Espuny**

- GitHub: [@JavierCalzadaEspuny](https://github.com/JavierCalzadaEspuny)
- Repository: [pandas_ti](https://github.com/JavierCalzadaEspuny/pandas_ti)

---

**Made for the quantitative trading community**