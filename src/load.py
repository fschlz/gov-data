import pandas as pd
from pathlib import Path
import os


def read_destatis_csv(path: Path()) -> pd.DataFrame:
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


def load_all_destatis_csvs_in(path: Path()) -> pd.DataFrame:
    for _, _, files in os.walk(path):
        df_list = [read_destatis_csv(path / Path(file)) for file in sorted(files)]
    return pd.concat(df_list, ignore_index=True)
