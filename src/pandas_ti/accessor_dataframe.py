import pandas as pd
import inspect
import types
from functools import wraps
from rich.console import Console
from rich.panel import Panel
from pandas_ti.registry import registry_funcs_dict, registry_names_dict

# Dictionary of registered dataframe indicator functions
dataframe_registry_funcs = registry_funcs_dict['dataframe']
dataframe_registry_names = registry_names_dict['dataframe']

# Common OHLCV column variations
COLUMN_VARIATIONS = {
    'Open': ['Open', 'OPEN', 'open', 'O', 'o'],
    'High': ['High', 'HIGH', 'high', 'H', 'h'], 
    'Low': ['Low', 'LOW', 'low', 'L', 'l'],
    'Close': ['Close', 'CLOSE', 'close', 'C', 'c'],
    'Volume': ['Volume', 'VOLUME', 'volume', 'Vol', 'vol', 'V', 'v']
}

# Single global Rich Console instance
console = Console()


def create_method(func):
    """
    Automatically injects OHLCV columns when calling a registered
    technical indicator function from a pandas DataFrame accessor.
    """
    sig = inspect.signature(func)
    required_ohlcv = [name for name in sig.parameters if name in COLUMN_VARIATIONS.keys()]

    @wraps(func)  # Preserve the original function’s name and docstring
    def method(self, **kwargs):
        # Build a dictionary with all available OHLCV columns in the DataFrame
        call_kwargs = {
            name: getattr(self, name)
            for name in required_ohlcv
            if hasattr(self, name)
        }
        call_kwargs.update(kwargs)
        return func(**call_kwargs)

    return method


@pd.api.extensions.register_dataframe_accessor("ti")
class DataframeTechnicalIndicatorsAccessor:
    """Pandas DataFrame accessor for technical indicators."""

    def __init__(self, df: pd.DataFrame):
        self._df = df
        self._map_columns()
        self._add_registry_methods()

    def _map_columns(self):
        """Detect OHLCV columns in the DataFrame and map them as attributes."""
        for key, variations in COLUMN_VARIATIONS.items():
            for col in self._df.columns:
                if str(col) in variations:
                    setattr(self, key, self._df[col])
                    break

    def _add_registry_methods(self):
        """Register all dataframe indicator functions as accessor methods."""
        for name, func in dataframe_registry_funcs.items():
            method = create_method(func)
            setattr(self, name, types.MethodType(method, self))

    def indicators(self):
        """Return a DataFrame of available dataframe technical indicators with full names."""
        return pd.DataFrame(dataframe_registry_names)
        

    def help(self, indicator_name: str):
        """Display the documentation of a dataframe indicator."""
        func = dataframe_registry_funcs.get(indicator_name)
        if not func:
            console.print(f"Indicator '{indicator_name}' not found")
            return

        doc_text = func.__doc__ or "Indicator has no documentation"
        console.print(
            Panel(doc_text, title=f"Documentation for {indicator_name}")
        )
