from typing import Any
import numpy as np
import pandas as pd
import base64
import yaml
from pathlib import Path


def get_columns(df: pd.DataFrame):
    return df.columns.tolist()


def download(df: pd.DataFrame):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    encoding = "latin-1"
    csv = df.to_csv(index=False, encoding=encoding, sep=";", decimal=",")
    b64 = base64.b64encode(csv.encode(encoding=encoding)).decode(encoding=encoding)  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}" download="produktions_daten.csv">Download produktions_daten.csv</a>'
    return href


def load_yaml(path: Path) -> dict:
    """basic wrapper function to load yaml file as python dict

    Args:
        path (Path): file path

    Returns:
        dict: data from the yaml file in a dict
    """
    with open(path, mode="r") as f:
        return yaml.load(f, yaml.FullLoader)


def check_if_valid(value: Any, unaccepted_values: list = [np.inf, -np.inf, np.nan]) -> bool:
    return value not in unaccepted_values
