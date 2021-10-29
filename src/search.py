import pandas as pd


def search_simple_pattern(search_term: str, series: pd.Series, use_regex=False) -> pd.Series:
    """simple search via built-in methods
    regex matching possible

    Args:
        search_term (str): string you want to search for
        series (pd.Series): data to search through
        use_regex (bool, optional): to use regex or not. Defaults to False.

    Returns:
        pd.Series: part of series that matches the search term
    """
    match_series = series.str.contains(pat=search_term, regex=use_regex)

    series_lower = series.str.lower()
    match_series_lower = series_lower.str.contains(pat=search_term, regex=use_regex)

    return series[match_series | match_series_lower]


def get_ids_from_search(
    search_series: pd.Series, id_series: pd.Series
) -> pd.Series:
    return id_series.iloc[search_series.index]
