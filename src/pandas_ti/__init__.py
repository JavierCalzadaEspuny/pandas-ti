import importlib
import pkgutil
# Import indicator packages (folders, not modules yet)
from . import indicators_dataframe, indicators_series
# Import accessors to register them with pandas
from .accessor_series import SeriesTechnicalIndicatorsAccessor
from .accessor_dataframe import DataframeTechnicalIndicatorsAccessor 
# Import registry dicts (empty at this point, will be populated below)
from .registry import registry_funcs_dict, registry_names_dict


# Auto-import all indicator modules in the indicators packages
def auto_import_package(package):
    """Auto-import in the specified order"""
    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        importlib.import_module(f"{package.__name__}.{module_name}")

# Auto-import all indicators to register them
auto_import_package(indicators_dataframe)
auto_import_package(indicators_series)


# Expose all registered indicators at package level for direct import
# This allows: import pandas_ti as ti; ti.SMA(...)
def __getattr__(name):
    """
    Dynamically expose registered indicators at package level.
    
    This allows users to call indicators directly:
        import pandas_ti as ti
        result = ti.ZigZag(high_series, low_series, pct=0.05)
    
    While still supporting the accessor pattern:
        df.ti.ZigZag(pct=0.05)  # with auto-inject
    """
    # Check dataframe indicators
    if name in registry_funcs_dict['dataframe']:
        return registry_funcs_dict['dataframe'][name]
    # Check series indicators
    if name in registry_funcs_dict['series']:
        return registry_funcs_dict['series'][name]
    # Not found
    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")


def __dir__():
    """Show all available indicators when using dir() or autocomplete."""
    return (
        list(globals().keys()) + 
        list(registry_funcs_dict['dataframe'].keys()) + 
        list(registry_funcs_dict['series'].keys())
    )

# Defines what is exported when using 'from pandas_ti import *'
__all__ = [
    'SeriesTechnicalIndicatorsAccessor', 
    'DataframeTechnicalIndicatorsAccessor', 
    'registry_funcs_dict', 
    'registry_names_dict'
]