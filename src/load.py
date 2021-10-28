import pandas as pd
from pathlib import Path


def read_destatis_flatfile(path: Path()) -> pd.DataFrame:
    """read in flatfile CSV's from Genesis DB

    Args:
        path (Path): file path

    Returns:
        pd.DataFrame: loaded pandas dataframe
    """    
    return pd.read_csv(
        path,
        sep=";",
        decimal=",",
        encoding="latin-1",
        na_values=["-", ".", "..."]
    )
