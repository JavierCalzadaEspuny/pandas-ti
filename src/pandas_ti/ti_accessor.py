import pandas as pd
from pandas.api.extensions import register_dataframe_accessor
import inspect
from typing import Optional, Dict, Callable
from functools import wraps
from . import indicators


@register_dataframe_accessor("ti")
class TechnicalIndicatorsAccessor:
    """
    A pandas DataFrame accessor for technical indicators, providing easy access to OHLCV-based calculations.

    This accessor dynamically adds methods from the `indicators` module, mapping DataFrame columns to
    function parameters for open, high, low, close, and volume data. It supports custom column mappings
    and automatic column detection.

    Examples
    --------
    >>> df.ti.sma(period=14)  # Calculate Simple Moving Average
    """

    def __init__(self, df: pd.DataFrame, column_mapping: Optional[Dict[str, str]] = None):
        """
        Initialize the Technical Indicators accessor.

        Parameters
        ----------
        df : pandas.DataFrame
            The input DataFrame containing financial data.
        column_mapping : dict of str, optional
            Dictionary mapping standard OHLCV names ('open', 'high', 'low', 'close', 'volume') 
            to actual DataFrame column names. Example: {'open': 'OPEN', 'high': 'HIGH', ...}. 
            If None, columns are auto-detected.

        Raises
        ------
        ValueError
            If required columns are missing from the DataFrame.
        """
        self._df = df
        self._column_mapping = self._initialize_column_mapping(column_mapping)
        self._validate_columns()
        self._register_indicators()

    def _initialize_column_mapping(self, column_mapping: Optional[Dict[str, str]]) -> Dict[str, str]:
        """
        Initialize or auto-detect column mappings for OHLCV data.

        Parameters
        ----------
        column_mapping : dict of str, optional
            User-provided column mapping.

        Returns
        -------
        dict of str
            Mapping of standard OHLCV names to DataFrame column names.
        """
        default_mapping = {
            'open': 'Open',
            'high': 'High',
            'low': 'Low',
            'close': 'Close',
            'volume': 'Volume'
        }

        if column_mapping:
            return {**default_mapping, **{k.lower(): v for k, v in column_mapping.items()}}

        common_variations = {
            'open': ['Open', 'OPEN', 'open', 'O', 'PriceOpen'],
            'high': ['High', 'HIGH', 'high', 'H', 'PriceHigh'],
            'low': ['Low', 'LOW', 'low', 'L', 'PriceLow'],
            'close': ['Close', 'CLOSE', 'close', 'C', 'PriceClose', 'Adj Close'],
            'volume': ['Volume', 'VOLUME', 'volume', 'Vol', 'V']
        }

        auto_mapping = {}
        for key, variations in common_variations.items():
            for var in variations:
                if var in self._df.columns:
                    auto_mapping[key] = var
                    break
            else:
                auto_mapping[key] = default_mapping[key]

        return auto_mapping

    def _validate_columns(self) -> None:
        """
        Validate that required columns exist in the DataFrame.

        Raises
        ------
        ValueError
            If any required OHLCV columns are missing.
        """
        missing_cols = [
            col_name for key, col_name in self._column_mapping.items()
            if col_name not in self._df.columns
        ]
        if missing_cols:
            raise ValueError(
                f"Missing required columns: {', '.join(missing_cols)}. "
                "Ensure the DataFrame contains these columns or provide a valid column_mapping."
            )

    def _register_indicators(self) -> None:
        """
        Register all indicator functions from the indicators module as methods of this accessor.
        """
        for name in dir(indicators):
            if name.startswith("_"):
                continue
            func = getattr(indicators, name)
            if callable(func):
                self._add_indicator(func, name)

    def _add_indicator(self, func: Callable, name: str) -> None:
        """
        Create a method for an indicator, mapping OHLCV columns to function parameters.

        Parameters
        ----------
        func : callable
            The indicator function to register.
        name : str
            The name of the indicator function.
        """
        @wraps(func)
        def wrapper(*args, **kwargs):
            call_kwargs = {}
            for param in inspect.signature(func).parameters.values():
                param_name = param.name.lower()
                if param_name in self._column_mapping:
                    call_kwargs[param.name] = self._df[self._column_mapping[param_name]]
                elif param.name in self._df.columns:
                    call_kwargs[param.name] = self._df[param.name]
            call_kwargs.update(kwargs)
            return func(*args, **call_kwargs)

        setattr(self, name, wrapper)
        setattr(self, name.lower(), wrapper)

    def set_column_mapping(self, column_mapping: Dict[str, str]) -> None:
        """
        Update the OHLCV column mapping.

        Parameters
        ----------
        column_mapping : dict of str
            Dictionary mapping standard OHLCV names to DataFrame column names.
            Example: {'open': 'OPEN', 'high': 'HIGH', ...}

        Raises
        ------
        ValueError
            If any required columns are missing after updating the mapping.
        """
        self._column_mapping = self._initialize_column_mapping(column_mapping)
        self._validate_columns()

    @property
    def column_mapping(self) -> Dict[str, str]:
        """
        Get the current column mapping.

        Returns
        -------
        dict of str
            Mapping of standard OHLCV names to DataFrame column names.
        """
        return self._column_mapping