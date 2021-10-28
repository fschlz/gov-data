import pandas as pd
from typing import List


def search_products(search_term: str, series: pd.Series, use_regex=False) -> List[str]:

    match_series = series.str.contains(pat=search_term, regex=use_regex)

    series_lower = series.str.lower()
    match_series_lower = series_lower.str.contains(pat=search_term, regex=use_regex)

    return set(series[match_series | match_series_lower])
