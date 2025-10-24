# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- DataFrame accessor system with `.ti` namespace for technical indicators
- Series accessor system with `.ti` namespace for series-based indicators
- Automatic OHLCV column detection and mapping
- Registry system for managing indicators
- Built-in help system with `df.ti.help()` and `series.ti.help()`
- DataFrame volatility indicators:
  - `TR()` - True Range
  - `ATR(length)` - Average True Range
  - `RTR()` - Relative True Range
  - `ARTR(length)` - Average Relative True Range
  - `SRTR(N, expand, n, method, L, full)` - Standardized Relative True Range
- Series indicators:
  - `SMA(length)` - Simple Moving Average
  - `EMA(length)` - Exponential Moving Average
- Support for Python 3.9+
- Rich console output for help system
- Extensible architecture with decorator pattern
- MIT License
