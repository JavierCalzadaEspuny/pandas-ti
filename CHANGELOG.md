# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [1.0.1] - 2025-10-27

### Fixed
- Fixed incorrect import references from `test_pandas_ti` to `pandas_ti` in accessor files
- Resolved critical bug in version 1.0.0 that prevented proper module imports
- Corrected import statements in `accessor_series.py` and `accessor_dataframe.py`

## [1.0.0] - 2025-10-27

### Added
- DataFrame accessor system with `.ti` namespace for technical indicators
- Series accessor system with `.ti` namespace for series-based indicators
- Automatic OHLCV column detection and mapping
- Registry system for managing indicators
- Built-in help system with `df.ti.help()` and `series.ti.help()`
- DataFrame indicators:
  - `TR()` - True Range
  - `ATR(n)` - Average True Range
  - `RTR()` - Relative True Range
  - `ARTR(n)` - Average Relative True Range
  - `SRTR(n, N, expand, method, full)` - Standardized Relative True Range
- Series indicators:
  - `SMA(n)` - Simple Moving Average
  - `EMA(n)` - Exponential Moving Average
- Support for Python 3.12+
- Rich console output for help system
- Extensible architecture with decorator pattern
- MIT License
