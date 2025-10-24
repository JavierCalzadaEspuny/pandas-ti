from typing import Literal, Callable

registry_funcs_dict = {'dataframe':{}, 'series':{}}
# registry_dict = {'dataframe':{
#                               'TR': 0x000002027BDD5EE0, 
#                               'RTR': 0x000002027BDD5EE0
#                              }, 
#                  'series':{
#                               'SMA': 0x000002027BDD5EE0,
#                               'EMA': 0x000002027BDD5EE0,
#                  }}

registry_names_dict = {'dataframe':{'Indicator': [], 'Full Name': []}, 'series':{'Indicator': [], 'Full Name': []}}
# registry_dict = {'dataframe':{
#                               'TR': 'True Range', 
#                               'RTR': 'Relative True Range'
#                              }, 
#                  'series':{
#                               'SMA': 'Simple Moving Average',
#                               'EMA': 'Exponential Moving Average',
#                  }}



def register_indicator(ti_type: Literal['dataframe', 'series'], extended_name: str) -> Callable[[Callable], Callable]:
    """
    Decorator to register an indicator in the registry.

    When a function is decorated with @register_dataframe_indicator, it is automatically
    added to the 'registry_dict' dictionary under 'dataframe' using its name as the key
    and a tuple of (function, extended_name) as the value.

    Parameters
    ----------
    ti_type : Literal['dataframe', 'series']
        The type of indicator being registered.
    extended_name : str
        The extended name to register the function under.

    Returns
    -------
    Callable
        The decorator function that registers the input function.

    Examples
    --------
    >>> @register_dataframe_indicator(ti_type='dataframe', extended_name='Average True Range')
    >>> def ATR(High: pd.Series, Low: pd.Series, Close: pd.Series) -> pd.Series:
    >>>     ...
    >>> @register_dataframe_indicator(ti_type='series', extended_name='Simple Moving Average')
    >>> def SMA(series: pd.Series, n: int) -> pd.Series:
    >>>     ...
    """
    if ti_type not in ['dataframe', 'series']:
        raise ValueError(f"Invalid ti_type: {ti_type}. Must be 'dataframe' or 'series'.")
    if extended_name is None:
        raise ValueError("Extended Name of the indicator must be provided")
    
    def decorator(func: Callable) -> Callable:
        func_name = func.__name__
        # Register the function in the appropriate registry
        registry_funcs_dict[ti_type][func_name] = func
        # Register the extended name in the appropriate registry
        registry_names_dict[ti_type]['Indicator'].append(func_name)
        registry_names_dict[ti_type]['Full Name'].append(extended_name)
        return func
    return decorator

