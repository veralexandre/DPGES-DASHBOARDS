import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image

st.set_page_config(page_title="Painel de Dados", page_icon=":bar_chart:", layout="wide")
st.header('Dados de Serviços 2023')
st.text('Dados disponilizados pelo Relatório de Ações Governamentais - RAG.')
st.text('Atualização novembro 2023.')
col1, col2 = st.columns(2)
col3, Col4= st.columns([2, 1])

#@st.cache_data
def gerar_df():
    df = pd.read_excel(
        io="datasets/carreta_dados.xlsx",
        engine="openpyxl",
        sheet_name="pl1",
        usecols="A:C",
        nrows=199
    )
    return df

df = gerar_df()