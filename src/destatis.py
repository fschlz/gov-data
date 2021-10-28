import requests
import pandas as pd
from io import StringIO
import streamlit as st
import logging
logger = logging.getLogger()

uname = "DEST12N7ME"
psw = "SYk^BUUZnfrQd^$S4X8V"


@st.cache(allow_output_mutation=True)
def get_genesis(
    params: dict,
    domain: str = "data",
    response_type: str = "table",
    api_type: str = "rest",
    api_version: str = "2020"
) -> requests.models.Response:

    url = f"https://www-genesis.destatis.de/genesisWS/{api_type}/{api_version}/{domain}/{response_type}"
    logger.info("sending request to base URL: ", url)

    try:
        res = requests.get(url, params)
    except Exception:
        logger.error("something went wrong", exc_info=True)

    logger.info("request status code:", res.status_code)

    return res
