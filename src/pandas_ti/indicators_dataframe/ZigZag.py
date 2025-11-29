import numpy as np
import pandas as pd
from typing import Literal
from ..registry import register_indicator


class ZigZagClass:
    """
    A stateful ZigZag indicator implementation for real-time price data processing.
    
    The ZigZag indicator identifies significant price reversals by filtering out smaller 
    price movements below a specified percentage threshold. It detects swing highs and 
    swing lows, confirming pivots only when the price moves by at least the specified 
    percentage in the opposite direction.
    
    Parameters
    ----------
    pct : float
        The minimum percentage change required to confirm a pivot point.
        For example, 0.05 means a 5% price movement is needed to confirm a reversal.
        Must be greater than 0.
    debug : bool, default=False
        If True, stores detailed internal state information at each update for 
        debugging purposes. Access this data using the `debug_df()` method.
    
    Attributes
    ----------
    last_confirmed_type : {'High', 'Low', None}
        The type of the last confirmed pivot. None if no pivots confirmed yet.
    last_confirmed_price : float or None
        The price level of the last confirmed pivot.
    last_confirmed_idx : any or None
        The index (timestamp) of the last confirmed pivot.
    candidate_price : float or None
        The current candidate pivot price that hasn't been confirmed yet.
    candidate_idx : any or None
        The index (timestamp) of the current candidate pivot.
    pct : float
        The minimum percentage change threshold.
    
    Methods
    -------
    update(high, low, idx)
        Process new price data and update the ZigZag state.
    series(include_candidate=False)
        Return pivot prices as a Series (aligned with original df index).
    dataframe(include_candidate=False)
        Return complete data as DataFrame with pivot, extreme, and type columns.
    df()
        Return raw historical data as a DataFrame (includes High, Low, pivot, extreme).
    debug_df()
        Return detailed internal state history as a DataFrame (if debug=True).
    
    Examples
    --------
    >>> zz = ZigZagClass(pct=0.05)
    >>> for idx, row in df.iterrows():
    ...     zz.update(high=row['High'], low=row['Low'], idx=idx)
    >>> 
    >>> # Extract pivots as Series
    >>> pivots_series = zz.series()
    >>> 
    >>> # Get full DataFrame with metadata
    >>> pivots_df = zz.dataframe(include_candidate=True)
    >>> 
    >>> # Check current state
    >>> print(f"Candidate: {zz.candidate_price} at {zz.candidate_idx}")
    
    Notes
    -----
    - The indicator requires at least one price movement >= pct to identify the first pivot
    - Candidate pivots are continuously updated but not confirmed until the reversal threshold is met
    - The algorithm prevents intra-candle zigzags by using elif logic in swing updates
    - Historical data includes all processed candles, but only confirmed pivots have non-NaN pivot values
    - Use series() for simple pivot extraction, dataframe() for detailed analysis with metadata
    """
    def __init__(self, pct: float, debug: bool = False):
        if pct <= 0:
            raise ValueError("pct must be > 0")
        self.pct = pct
        self.debug = debug
        # None: no pivots yet
        # 'High': last confirmed was high (updating low & searching for new high to confirm low)
        # 'Low': last confirmed was low (updating high & searching for new low to confirm high)
        self.last_confirmed_type = None
        self.last_confirmed_price = None
        self.last_confirmed_idx = None
        self._confirmed = False
        self._swing_high = -np.inf
        self._swing_high_idx = None
        self._swing_low = np.inf
        self._swing_low_idx = None
        self.candidate_price = None
        self.candidate_idx = None
        self._historic_dic = {'index': [], 'High': [], 'Low': [], 'pivot': [], 'extreme': []}
        self._index_to_pos = {}
        if debug:
            self._debug_dic = {'index': [], 'High': [], 'Low': [], 'swing_high': [], 
                              'swing_high_idx': [], 'swing_low': [], 'swing_low_idx': [], 
                              'candidate_price': [], 'candidate_idx': [], 'confirmed': [], 
                              'last_confirmed_type': [], 'last_confirmed_price': [], 
                              'last_confirmed_idx': []}


    # == Data Storage ==
    def _update_df(self, high: float, low: float, idx) -> None:
        """Update the historic data dictionary with new values."""
        self._historic_dic['index'].append(idx)
        self._historic_dic['High'].append(high)
        self._historic_dic['Low'].append(low)
        self._historic_dic['pivot'].append(np.nan)
        self._historic_dic['extreme'].append(np.nan)
        self._index_to_pos[idx] = len(self._historic_dic['index']) - 1

    def df(self) -> pd.DataFrame:
        """
        Return raw historical data as a DataFrame.
        
        Returns DataFrame with columns: High, Low, pivot, extreme (no 'type' column).
        For processed data with 'type' column, use dataframe() method instead.
        """
        return pd.DataFrame(self._historic_dic).set_index('index')


    # == Debug ==
    def _debug_state(self, high: float, low: float, idx) -> None:
        """Store the internal state for debugging purposes."""
        debug_dic = self._debug_dic
        debug_dic['index'].append(idx)
        debug_dic['High'].append(high)
        debug_dic['Low'].append(low)
        debug_dic['swing_high'].append(self._swing_high)
        debug_dic['swing_high_idx'].append(self._swing_high_idx)
        debug_dic['swing_low'].append(self._swing_low)
        debug_dic['swing_low_idx'].append(self._swing_low_idx)
        debug_dic['candidate_price'].append(self.candidate_price)
        debug_dic['candidate_idx'].append(self.candidate_idx)
        debug_dic['confirmed'].append(self._confirmed)
        debug_dic['last_confirmed_type'].append(self.last_confirmed_type)
        if self._confirmed:
            debug_dic['last_confirmed_price'].append(self.last_confirmed_price)
            debug_dic['last_confirmed_idx'].append(self.last_confirmed_idx)
        else:
            debug_dic['last_confirmed_price'].append(np.nan)
            debug_dic['last_confirmed_idx'].append(np.nan)
        self._debug_dic = debug_dic

    def debug_df(self) -> pd.DataFrame:
        """Return the debug data as a DataFrame."""
        return pd.DataFrame(self._debug_dic).set_index('index')


    # == Logic Helper ==
    @staticmethod
    def _pct_change(reference: float, new: float) -> float:
        """Calculate the percentage change from reference to new."""
        return (new - reference) / reference

    # == Logic ==
    def _update_swings(self, confirmed: Literal['High', 'Low', None], high: float, low: float, idx) -> None:
        """Update swing highs and lows based on last confirmed pivot type."""
        # Initial state: no confirmed pivots yet update both swings to find first pivot
        if confirmed is None:
            if high > self._swing_high:
                self._swing_high = high
                self._swing_high_idx = idx
            if low < self._swing_low:
                self._swing_low = low
                self._swing_low_idx = idx

        # High: last confirmed was high (updating low & searching for new high to confirm low)
        elif confirmed == 'High':
            if low < self._swing_low:
                self._swing_low = low
                self._swing_low_idx = idx
                self._reset_swings(confirmed='High', high=high, low=low, idx=idx)
            elif high > self._swing_high:    # IMPORTANT: `elif` → blocks opposite extreme in same candle (prevents intra-candle zig-zag & duplicate pivots errors)
                self._swing_high = high
                self._swing_high_idx = idx
        
        # Low: last confirmed was low (updating high & searching for new low to confirm high)
        elif confirmed == 'Low':
            if self._swing_high < high:
                self._swing_high = high
                self._swing_high_idx = idx
                self._reset_swings(confirmed='Low', high=high, low=low, idx=idx)
            elif low < self._swing_low:  # IMPORTANT: # `elif` → blocks opposite extreme in same candle (prevents intra-candle zig-zag & duplicate pivots errors)
                self._swing_low = low
                self._swing_low_idx = idx

    def _reset_swings(self, confirmed: Literal['High', 'Low'], high: float, low: float, idx) -> None:
        """Reset the swing extreme that was just confirmed for _update_swings logic."""
        if confirmed == 'High':
            self._swing_high = -np.inf
            self._swing_high_idx = idx
        elif confirmed == 'Low':
            self._swing_low = np.inf
            self._swing_low_idx = idx


    def _confirm_pivot(self, price: float, idx, extreme_type: Literal['High', 'Low']) -> None:
        """Confirm a pivot and update historic data."""
        pos = self._index_to_pos[idx]
        self._historic_dic['pivot'][pos] = price
        self._historic_dic['extreme'][pos] = extreme_type
        self.last_confirmed_type = extreme_type
        self.last_confirmed_price = price
        self.last_confirmed_idx = idx
        # For debug purposes
        self._confirmed = True
        # Reset candidate after confirmation
        self.candidate_price, self.candidate_idx = None, None


    def update(self, high: float, low: float, idx):
        """
        Class method to update the ZigZag indicator with new the data.

        Parameters
        ----------
        high : float
            The high price of the current candle.
        low : float
            The low price of the current candle.
        idx : any
            The index of the current candle (e.g., timestamp).
        """
        # 1. Update & Validate new data
        self._update_df(high, low, idx)
        if pd.isna(high) or pd.isna(low) or high < low:
            return

        # 2. Update swings
        self._update_swings(self.last_confirmed_type, high, low, idx)

        # 3. System logic
        # Initial state: Select a direction to start and confirm the first pivot
        self._confirmed = False
        if self.last_confirmed_type is None:
            # Up [low (candidate to confirm) -> high (next candidate)]
            if self._swing_low_idx < self._swing_high_idx:
                change = self._pct_change(reference=self._swing_low, new=self._swing_high)
                if change >= self.pct:
                    self._confirm_pivot(price=self._swing_low, idx=self._swing_low_idx, extreme_type='Low')
                    self._reset_swings(confirmed='Low', high=high, low=low, idx=idx)  
                # SET CANDIDATE AFTER CONFIRMATION LOGIC
                self.candidate_price, self.candidate_idx = self._swing_low, self._swing_low_idx

            # Down [high (candidate to confirm) -> low (next candidate)]
            elif self._swing_high_idx < self._swing_low_idx:
                change = self._pct_change(reference=self._swing_high, new=self._swing_low)
                if change >= self.pct:
                    self._confirm_pivot(price=self._swing_high, idx=self._swing_high_idx, extreme_type='High')
                    self._reset_swings(confirmed='High', high=high, low=low, idx=idx)
                # SET CANDIDATE AFTER CONFIRMATION LOGIC
                self.candidate_price, self.candidate_idx = self._swing_high, self._swing_high_idx


        # Low: last confirmed was low (updating high & searching for new low to confirm high)
        # High (last confirmed) -> Low (candidate) -> High (last relevant candle)
        elif self.last_confirmed_type == 'High':
            change = self._pct_change(reference=self._swing_low, new=self._swing_high)
            if change >= self.pct:
                self._confirm_pivot(price=self._swing_low, idx=self._swing_low_idx, extreme_type='Low')
                self._reset_swings(confirmed='Low', high=high, low=low, idx=idx)
            # SET CANDIDATE AFTER CONFIRMATION LOGIC
            self.candidate_price, self.candidate_idx = self._swing_low, self._swing_low_idx


        # High: last confirmed was high (updating low & searching for new high to confirm low)
        # Low (last confirmed) -> high (candidate) -> low (last relevant candle)
        elif self.last_confirmed_type == 'Low':
            change = -self._pct_change(reference=self._swing_high, new=self._swing_low)
            if change >= self.pct:
                self._confirm_pivot(price=self._swing_high, idx=self._swing_high_idx, extreme_type='High')
                self._reset_swings(confirmed='High', high=high, low=low, idx=idx)
            # SET CANDIDATE AFTER CONFIRMATION LOGIC
            self.candidate_price, self.candidate_idx = self._swing_high, self._swing_high_idx

        # 4. Debug
        if self.debug:
            self._debug_state(high=high, low=low, idx=idx)

    
    # == Return Types ==
    def series(self, include_candidate: bool = False) -> pd.Series:
        """
        Return pivot prices as a Series (aligned with original dataframe index).
        
        Parameters
        ----------
        include_candidate : bool, default=False
            If True, includes the current unconfirmed candidate pivot.
        
        Returns
        -------
        pd.Series
            Series with pivot prices. Non-pivot candles have NaN values.
        """
        pivots = pd.Series(self._historic_dic['pivot'], index=self._historic_dic['index'])
        if include_candidate and self.candidate_idx is not None:
            pivots.loc[self.candidate_idx] = self.candidate_price
        return pivots

    def dataframe(self, include_candidate: bool = False) -> pd.DataFrame:
        """
        Return complete ZigZag data as DataFrame with metadata.
        
        Parameters
        ----------
        include_candidate : bool, default=False
            If True, includes the current unconfirmed candidate pivot.
        
        Returns
        -------
        pd.DataFrame
            DataFrame with columns:
            - High: High prices
            - Low: Low prices
            - pivot: Pivot prices (NaN for non-pivots)
            - extreme: 'High' or 'Low' for pivots (NaN for non-pivots)
            - type: 'confirmed' or 'candidate' (NaN for non-pivots)
        """
        df = pd.DataFrame(self._historic_dic).set_index('index')
        
        # Add type column (confirmed vs candidate)
        df['type'] = np.nan
        confirmed_mask = df['pivot'].notna()
        df.loc[confirmed_mask, 'type'] = 'confirmed'
        
        # Add candidate if requested
        if include_candidate and self.candidate_idx is not None:
            df.loc[self.candidate_idx, 'pivot'] = self.candidate_price
            # Determine candidate extreme (High or Low)
            candidate_extreme = 'High' if self.candidate_price == df.loc[self.candidate_idx, 'High'] else 'Low'
            df.loc[self.candidate_idx, 'extreme'] = candidate_extreme
            df.loc[self.candidate_idx, 'type'] = 'candidate'
        df = df.drop(columns=['High', 'Low'])

        return df

    
    


@register_indicator(ti_type='dataframe', extended_name='ZigZag')
def ZigZag(High: pd.Series, Low: pd.Series, pct: float) -> 'ZigZagClass':
    """
    ZigZag Indicator

    Identifies significant price reversals by detecting swing highs and lows,
    confirming pivots only when price moves by at least the specified percentage
    in the opposite direction.

    Required Columns
    ----------------
    High : pd.Series
        Series of high prices (Automatically injected).
    Low : pd.Series
        Series of low prices (Automatically injected).

    Parameters
    ----------
    pct : float
        Minimum percentage change required to confirm a reversal pivot.
        Must be greater than 0. For example, 0.05 means a 5% price movement.

    Returns
    -------
    ZigZagClass
        Stateful ZigZag instance with extraction methods:
        
        .series(include_candidate=False) -> pd.Series
            Returns pivot prices as Series (aligned with df index, NaN for non-pivots).
        
        .dataframe(include_candidate=False) -> pd.DataFrame
            Returns complete data with columns: pivot, extreme, type.
        
        Direct attribute access:
            .candidate_price, .candidate_idx
            .last_confirmed_price, .last_confirmed_idx, .last_confirmed_type

    Examples
    --------
    >>> # Via accessor
    >>> zz = df.ti.ZigZag(pct=0.05)
    >>> df['pivots'] = zz.series()
    >>> df['pivots_live'] = zz.series(include_candidate=True)
    >>> pivot_df = zz.dataframe()
    >>> 
    >>> # Direct import
    >>> import pandas_ti as ti
    >>> zz = ti.ZigZag(High=df['High'], Low=df['Low'], pct=0.05)
    >>> df['pivots'] = zz.series()
    """
    df = pd.DataFrame({'High': High, 'Low': Low}, index=High.index)
    zz = ZigZagClass(pct=pct)
    highs = df['High'].to_numpy()
    lows = df['Low'].to_numpy()
    index = df.index
    for i in range(len(df)):
        zz.update(highs[i], lows[i], index[i])
    return zz