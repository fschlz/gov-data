from dataclasses import dataclass
from typing import Any
import pandas as pd
import numpy as np
from pathlib import Path
import logging
from src import load, preprocessing, utils

logger = logging.getLogger(__name__)
CONFIG = utils.load_yaml(Path("./config/data_config.yml"))


@dataclass
class ProductData:
    yearly: pd.DataFrame
    quarterly: pd.DataFrame

    @classmethod
    def get(cls, item: str) -> Any:
        return getattr(cls, item)

    @classmethod
    def run_preprocessing(cls):
        logger.info("running preprocessing")
        # yearly
        cls.yearly_metric_cols_rename_mapping = preprocessing.get_metric_cols_rename_mapping(cls.yearly)
        cls.yearly.rename(columns=cls.yearly_metric_cols_rename_mapping, inplace=True)

        preprocessing.set_timestamp_col_yearly_data(cls.yearly)

        preprocessing.replace_empties(cls.yearly, [pd.NA, np.nan], 0)

        # quarterly
        cls.quarterly_metric_cols_rename_mapping = preprocessing.get_metric_cols_rename_mapping(cls.quarterly)
        cls.quarterly.rename(columns=cls.quarterly_metric_cols_rename_mapping, inplace=True)

        preprocessing.set_time_cols_quarterly_data(cls.quarterly)
        preprocessing.set_timestamp_col_quarterly_data(cls.quarterly)

        preprocessing.replace_empties(cls.quarterly, [pd.NA, np.nan], 0)

    @classmethod
    def autoload(cls):
        logger.info("auto. loading files from ./resource/input")

        try:
            cls.yearly = load.read_destatis_flatfile(Path(CONFIG.get("data").get("yearly").get("path")))
            cls.quarterly = load.read_destatis_flatfile(Path(CONFIG.get("data").get("quarterly").get("path")))

            cls.run_preprocessing()

        except FileNotFoundError as exception:
            logger.error("chekc if sample files are in place", exc_info=True)
            raise exception
