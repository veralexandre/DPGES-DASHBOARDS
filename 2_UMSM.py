import pandas as pd
import plotly.express as px
import streamlit as st
from PIL import Image
from openpyxl.styles.builtins import total

st.set_page_config(page_title="Carreta da Mulher - Dashboard", page_icon=":bar_chart:", layout="wide")
st.header('Dados de Atendimento da Unidade Móvel de Saúde da Mulher 2023')
st.text('Dados disponilizados pelo Relatório de Ações Governamentais - RAG.')
st.text('Atualização novembro 2023.')
col1, col2 = st.columns(2)
col3, Col4= st.columns([2, 1])

@st.cache_data
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

with st.sidebar:
    st.subheader('Dashboard Unidade Móvel de Saúde da Mulher')
    logo_sub = Image.open('datasets/icone.png')
    st.image(logo_sub, use_column_width=True)
    st.subheader('Seleção de Filtro')

    # Converte a coluna "Mês" para o formato "Mês/Ano"
    df['Mês'] = df['Mês'].dt.strftime('%b/%Y')

    # Cria uma lista com os meses únicos
    meses = ["Todos"] + list(df['Mês'].unique())

    fmes = st.selectbox(
        "Selecione o mês:",
        options=meses,
        index=0
    )

    # Cria uma lista com os serviços únicos
    servicos = ["Todos"] + list(df['Serviço'].unique())

    fservico = st.selectbox(
        "Selecione o tipo de Serviço:",
        options=servicos,
        index=0
    )
# Lógica de filtro
servico_selecionado = fservico if fservico != "Todos" else None
mes_selecionado = fmes if fmes != "Todos" else None

if mes_selecionado is not None:
    if servico_selecionado is not None:
        dadosUsuario = df.loc[(df['Mês'] == mes_selecionado) & (df['Serviço'] == servico_selecionado)]
    else:
        dadosUsuario = df.loc[df['Mês'] == mes_selecionado]
else:
    dadosUsuario = df.copy()

# mostrar legendas dos dados selecionados
st.markdown('** Mês Selecionado: **' + fmes)
st.markdown('** Serviço Selecionado: **' + fservico)

# Cria o gráfico de barras agrupadas
fig = px.bar(
    dadosUsuario,
    x='Mês',
    y='Quantidade',
    color='Serviço',
    barmode='group',
    category_orders={'Mês': meses},
    labels={'Quantidade': 'Total de Atendimentos'},
    height=500,
    width=1420,
    title='Atendimentos da Carreta da Mulher por Mês e Serviço'
)

# Dicionário de cores
cores = {
    "Serviço A": "#e7edea",
    "Serviço B": "#ffc52c",
    "Serviço C": "#fb0c06",
    "Serviço D": "#030d4f",
    "Serviço E": "#ceecef",
    "Serviço F": "#7abf66",
    "Serviço G": "#c789f2",
}

# Atualiza o layout para melhor visualização
fig.update_layout(
    xaxis_title='Mês',
    yaxis_title='Quantidade de Atendimentos',
    legend_title='Serviço',
    legend_orientation="h",
    margin=dict(l=150, r=50, b=20, t=40),
    font_family="Arial",
    plot_bgcolor='white',
    paper_bgcolor='white',
)

# Exibe o gráfico no Streamlit
with col3:
    st.plotly_chart(fig)

def gerar_grafico_pizza(df, mes_selecionado, servico_selecionado):
    # Filtra os dados pelo mês e serviço selecionados
    df_filtrado = df.copy()
    if mes_selecionado is not None:
        df_filtrado = df_filtrado.loc[df_filtrado['Mês'] == mes_selecionado]
    if servico_selecionado is not None:
        df_filtrado = df_filtrado.loc[df_filtrado['Serviço'] == servico_selecionado]

    # Cria um dicionário com cores para cada serviço
    cores = {
        "Serviço A": "#e7edea",
        "Serviço B": "#ffc52c",
        "Serviço C": "#fb0c06",
        "Serviço D": "#030d4f",
        "Serviço E": "#ceecef",
        "Serviço F": "#7abf66",
        "Serviço G": "#c789f2",
    }

    # Cria o gráfico de pizza
    fig_pizza = px.pie(
        df_filtrado,
        values='Quantidade',
        names='Serviço',
        color='Serviço',
        hole=.3,
        title='Percentual Atendimentos por Serviço',
        height=500,
        labels={'Quantidade': 'Total de Atendimentos'}
    )

    # Atualiza o layout para melhor visualização
    fig_pizza.update_layout(
        font_family="Arial",
        plot_bgcolor='white',
        paper_bgcolor='white',
        # legend_title='Serviço',
        legend_orientation="v",
        margin=dict(l=20, r=20, b=20, t=40),
        colorway=list(cores.values())
    )

    return fig_pizza

# Gera o gráfico de pizza
fig_pizza = gerar_grafico_pizza(df, mes_selecionado, servico_selecionado)

# Exibe o gráfico de pizza no Streamlit
with col2:
    st.plotly_chart(fig_pizza)

def gerar_grafico_linhas(df, servico_selecionado):
    # Filtra os dados pelo serviço selecionado
    df_filtrado = df.copy()
    if servico_selecionado is not None:
        df_filtrado = df_filtrado.loc[df_filtrado['Serviço'] == servico_selecionado]

    # Cria o gráfico de linhas
    fig_linhas = px.line(
        df_filtrado,
        x='Mês',
        y='Quantidade',
        color='Serviço',
        labels={'Quantidade': 'Total de Atendimentos'},
        title='Atendimentos por Mês',
        height=500,
        width=700,

    )

    # Atualiza o layout para melhor visualização
    fig_linhas.update_layout(
        xaxis_title='Mês',
        yaxis_title='Quantidade de Atendimentos',
        legend_title='Serviço',
        legend_orientation="h",
        margin=dict(l=20, r=20, b=20, t=40),
        font_family="Arial",
        plot_bgcolor='white',
        paper_bgcolor='white',
    )

    return fig_linhas

# Gera o gráfico de linhas
fig_linhas = gerar_grafico_linhas(df, servico_selecionado)

# Exibe o gráfico de linhas no Streamlit
with col1:
    st.plotly_chart(fig_linhas)

# Exibe o total como métrica com cor e ícone
st.metric(label="Total de Atendimentos", value=total_servicos_formatado, delta="10%", delta_color="green", icon="‍⚕️")
