import streamlit as st
from babel.numbers import format_compact_decimal, format_currency
from pages.utils.plots import create_bar_plot
from pages.utils.table import get_table

# ----------------------------
if "full_df" not in st.session_state:
    st.session_state.full_df = get_table()
full_df = st.session_state.full_df

# ----------------------------
with st.sidebar:
    # option = st.selectbox("Selecione um ano", years)
    st.markdown("### Filtros")
    years: list = full_df["ano"].unique().tolist()
    options = st.multiselect("Selecione um ou mais anos", years, years)
    df = full_df[full_df["ano"].isin(options)]

st.markdown("# Relatório Analítico")

# ----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("### Total de gastos:")
    value = str(df["valor_documento"].sum())
    format_value = format_currency(value, "BRL", locale="pt_BR")
    compact_value = format_compact_decimal(value, locale="pt_BR")
    st.markdown(f"{format_value}")
    st.markdown(f"(R$ {compact_value})")

with col2:
    st.markdown("### Quantidade de Deputados:")
    st.markdown(f"{len(df['nome_deputado'].unique())}")

with col3:
    st.markdown("### Quantidade de partidos:")
    st.markdown(f"{len(df['sigla_partido'].unique())}")

# ----------------------------
st.markdown("## Gráficos")


create_bar_plot(
    df=df,
    x="valor_documento",
    y="tipo_despesa",
    x_label="Valor Total (R$)",
    y_label="Tipo de Despesa",
    title="Valor Total X Tipo de Despesa",
)

create_bar_plot(
    df=df,
    x="valor_documento",
    y="nome_deputado",
    x_label="Valor Total (R$)",
    y_label="Nome do Deputado",
    title="Valor Total X Deputado",
    limit=10,
)

create_bar_plot(
    df=df,
    x="valor_documento",
    y="nome_fornecedor",
    x_label="Valor Total (R$)",
    y_label="Nome do Fornecedor",
    title="Valor Total X 10 Maiores Fornecedores",
    limit=10,
)
