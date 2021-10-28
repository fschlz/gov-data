from typing import Any, Dict
import pandas as pd
import logging

logger = logging.getLogger(__name__)


def get_quarters(series: pd.Series) -> pd.Series:
    """get quarters from numbers in a series

    Args:
        series (pd.Series): series of numbers that should be renamed to quarters

    Returns:
        pd.Series: series with values that have been mapped/replaced to a quarter
    """
    logger.info("generating clear quarter names")
    return series.map(
        {
            i: f"Q{idx+1}"
            for idx, i in enumerate(sorted(series.unique()))
        }
    )


def get_quarter_timestamp(year: pd.Series, quarter: pd.Series) -> pd.Series:
    assert all(year.index == quarter.index)
    return pd.Series(map(lambda x, y: "-".join([str(x), str(y)]), year, quarter), index=year.index)


def set_time_cols_quarterly_data(df: pd.DataFrame) -> None:
    df["JAHR"] = df.Zeit.copy()
    df["QUARTAL"] = get_quarters(df["2_Auspraegung_Label"])


def set_timestamp_col_quarterly_data(df: pd.DataFrame) -> None:
    df["TS"] = get_quarter_timestamp(df.JAHR, df.QUARTAL)


def set_timestamp_col_yearly_data(df: pd.DataFrame) -> None:
    df["TS"] = df.Zeit.copy()


def get_metric_cols_rename_mapping(df: pd.DataFrame) -> Dict[str, str]:
    old_col_names = df.filter(regex="(?=__)").columns  # get all coulmns that contain doubleunderscores
    new_col_names = [
        "{name} [{metric}]".format(
            name=split_list[1].replace("_", " "), metric=split_list[2]
        )
        for split_list in old_col_names.str.split("__")
    ]
    return {old: new for old, new in zip(old_col_names, new_col_names)}


def replace_empties(
    dataframe: pd.DataFrame,
    to_replace: list = ["-", "...", ".", "..", "/"],
    replace_with: Any = 0
) -> None:
    [
        dataframe.replace(val, replace_with, inplace=True)
        for val in to_replace
    ]
