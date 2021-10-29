from io import StringIO
from numpy import number
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
from streamlit import caching
from src import data, search, utils, stats
from pathlib import Path
import datetime as dt
import os

CONFIG = utils.load_yaml(Path("./config/data_config.yml"))
TITLE = "Deutsche Produktionsstatistik"
TODAY = dt.datetime.now().strftime("%Y-%m-%d")

######
# META
st.set_page_config(
    page_title=TITLE,
    page_icon="🇩🇪",
    layout='wide',
    initial_sidebar_state="expanded"
)


#####################
# STREAMLIT FUNCITONS
@st.cache(allow_output_mutation=True)
def get_data():
    productdata = data.ProductData
    productdata.autoload()
    return productdata


@st.cache(allow_output_mutation=True)
def get_search(series: pd.Series, search_term: str) -> str:
    return search.search_simple_pattern(search_term, series)


@st.cache(allow_output_mutation=True)
def get_ids(
    search_series: pd.Series, search_term: str, id_series: pd.Series
) -> set:
    return set(id_series[search_series == search_term].values)


@st.cache(allow_output_mutation=True)
def subset_data(df: pd.DataFrame, uids: set, id_col: str) -> pd.DataFrame:
    df_subset = df.loc[
        df[id_col].isin(uids)
    ]
    return df_subset.reset_index(drop=True)


##############
# GENERAL DATA
productdata = get_data()


########
# HEADER
st.title(f"🇩🇪 {TITLE}")
st.markdown("#### brought to you by **NicheMates**")
st.markdown("---")


################
# Authentication
USER = st.sidebar.text_input("User")
PSW = st.sidebar.text_input("Password", type="password")
if ((os.environ.get("PASSWORD") != PSW) | (os.environ.get("USER") != USER)):
    st.sidebar.error("Sry mate you're not authorized")
    st.stop()

#######
# INPUT
st.markdown("### Suche nach deinen Daten 👇🏼")

granularity_container, _ = st.columns([3, 7])
with granularity_container:
    granularity = st.selectbox(label="Wähle eine Granularität", options=["quarterly", "yearly"])


df_full = productdata.get(granularity)
label_col = CONFIG.get("data").get(granularity).get("label_col")
id_col = CONFIG.get("data").get(granularity).get("id_col")


search_input_container, subset_container, _ = st.columns([3, 4, 3])
with search_input_container:
    search_term = st.text_input(label="Gib einen Suchbegriff ein", value="Ananas", key="findus")

with subset_container:
    search_series = get_search(productdata.get(granularity)[label_col], search_term)
    subset_term = st.selectbox(
        label="Wähle eine Ausprägung deines Suchbegriffs",
        options=set(search_series)
    )
    subset_ids = get_ids(
        search_series,
        subset_term,
        search.get_ids_from_search(search_series, productdata.get(granularity)[id_col])
    )

st.markdown("---")


#################
# DATA CONTAINERS
st.markdown("### Hier ist deine Datenauswahl 💾")

data_container = st.container()
with data_container:
    df_subset = subset_data(df_full, subset_ids, id_col)
    keep_cols = ["TS"] + list(getattr(productdata, f"{granularity}_metric_cols_rename_mapping").values())
    st.dataframe(df_subset[keep_cols])

st.download_button(
    label="Tabelle downloaden",
    data=df_subset.to_csv(sep=";", decimal=",", encoding="latin1"),
    file_name=f"produktions_daten_{TODAY}.csv",
    mime="text/csv"
)

st.markdown("---")


#########
# VISUALS
# line plot
st.markdown("### Visualisiere deine Auswahl")

info_container, _ = st.columns([4, 6])

with info_container:
    y_axis = st.selectbox("Wähle eine Kennzahl", productdata.quarterly_metric_cols_rename_mapping.values())

    # only consider values that are not zero
    cagr = stats.calc_cagr(
        df_subset.loc[df_subset[y_axis] > 0.0, y_axis].to_numpy(),
        float(df_subset.TS.nunique())
    )
    st.markdown(f"""## CAGR = {round(cagr * 100, 3)}%""")

    price_amount = round(
        stats.calc_unit_price(
            df_subset[CONFIG.get("column_mapping").get("sales_return")].to_numpy(),
            df_subset[CONFIG.get("column_mapping").get("sales_amount_bm")].to_numpy()
        ),
        3
    )
    if utils.check_if_valid(price_amount):
        st.markdown(f"""## {price_amount} EUR/Stk.""")

    price_weight = round(
        stats.calc_unit_price(
            df_subset[CONFIG.get("column_mapping").get("sales_return")].to_numpy(),
            df_subset[CONFIG.get("column_mapping").get("sales_weight_kg")].to_numpy()
        ),
        3
    )
    if utils.check_if_valid(price_weight):
        st.markdown(f"""## {price_weight} EUR/kg""")

    # df_sum = df_subset[productdata.quarterly_metric_cols_rename_mapping.values()].sum(axis=0)
    # st.dataframe(df_sum)

plot_container = st.container()
with plot_container:
    px_chart = px.bar(
        df_subset,
        x="TS",
        y=y_axis,
        # marginal="box", hover_data=HabitData.data.columns
    )
    st.plotly_chart(px_chart, use_container_width=True)

st.markdown("---")
st.markdown("\* alle Daten aus der Genesis-Datenbank")
