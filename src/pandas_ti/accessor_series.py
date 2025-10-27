import pandas as pd
import types
from functools import wraps
from rich.console import Console
from rich.panel import Panel
from pandas_ti.registry import registry_funcs_dict, registry_names_dict

# Dictionary of series functions
series_registry_funcs = registry_funcs_dict['series']
series_registry_names = registry_names_dict['series']

# Global Rich Console instance
console = Console()


def create_method(func):
    """
    Injects the Series as the first argument automatically.
    """
    @wraps(func)
    def method(self, **kwargs):
        call_kwargs = {'series': self._series}
        call_kwargs.update(kwargs)
        return func(**call_kwargs)
    return method


@pd.api.extensions.register_series_accessor("ti")
class SeriesTechnicalIndicatorsAccessor:
    def __init__(self, series):
        self._series = series
        self._add_registry_methods()

    def _add_registry_methods(self):
        # Dynamically add methods from the registry
        for name, func in series_registry_funcs.items():
            method = create_method(func)
            setattr(self, name, types.MethodType(method, self))

    def indicators(self):
        """Returns the list of available indicators."""
        return pd.DataFrame(series_registry_names)

    def help(self, indicator_name):
        """Shows the documentation for an indicator."""
        func = series_registry_funcs.get(indicator_name)
        if not func:
            console.print(f"Indicator '{indicator_name}' not found")
            return

        doc_text = func.__doc__ or "Indicator has no documentation"
        console.print(
            Panel(doc_text, title=f"Documentation for {indicator_name}")
        )
