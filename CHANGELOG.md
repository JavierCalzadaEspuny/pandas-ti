# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2025-12-16

### Added
- **ZigZag indicator** - New stateful indicator for detecting significant price reversals
  - `ZigZagClass` - Core class for real-time/streaming data processing with `.update()` method
  - `ZigZag()` - Wrapper function for batch processing of complete datasets
  - Multiple output methods: `.series()`, `.dataframe()`, and direct attribute access
  - Support for both confirmed pivots and candidate pivots
  - Configurable percentage threshold for pivot confirmation
  - Debug mode for detailed internal state tracking

### Changed
- **Import system enhancement** - Indicators can now be imported directly without requiring accessor
  - New: `from pandas_ti import RTR, ZigZag, ZigZagClass` - Direct import support
  - Still supported: `df.ti.ZigZag()` - Accessor pattern with auto-injection
  - Improved: `__getattr__` implementation for dynamic indicator exposure at package level
- **ZigZag architecture** - Refactored for modularity and flexibility
  - Separated stateful class (`ZigZagClass`) from wrapper function (`ZigZag`)
  - Stateful design allows real-time processing with persistent state
  - Batch wrapper processes complete datasets and returns configured instance
- **SRTR architecture** - Refactored to use stateful class pattern for consistency
  - New `SRTRClass` - Stores all SRTR components (rtr, mu_N, sigma, mu_n, z_score, percentile)
  - Removed `full` parameter - use `.series()` for percentiles or `.dataframe()` for complete data
  - Direct attribute access: `srtr.percentile`, `srtr.z_score`, `srtr.mu_n`, etc.
  - Consistent API with ZigZag for better user experience
  - Index preservation: `.dataframe()` maintains original date index

### Fixed
- **DataFrame type warnings** - Fixed FutureWarning in ZigZag when setting 'type' column
  - Changed from `np.nan` initialization to explicit `pd.Series(dtype='object')`
  - Prevents dtype incompatibility warnings when mixing NaN with string values

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
