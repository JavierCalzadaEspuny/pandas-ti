import importlib
import pkgutil
from . import indicators_dataframe, indicators_series
from .accessor_series import SeriesTechnicalIndicatorsAccessor
from .accessor_dataframe import DataframeTechnicalIndicatorsAccessor
from .registry import registry_funcs_dict, registry_names_dict


def auto_import_package(package):
    """Auto-import in the specified order"""
    for _, module_name, _ in pkgutil.iter_modules(package.__path__):
        importlib.import_module(f"{package.__name__}.{module_name}")

auto_import_package(indicators_dataframe)
auto_import_package(indicators_series)

__all__ = ['SeriesTechnicalIndicatorsAccessor', 'DataframeTechnicalIndicatorsAccessor', 'registry_funcs_dict', 'registry_names_dict']