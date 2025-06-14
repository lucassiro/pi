import streamlit as st
from pages.utils.table import get_table

if "df" not in st.session_state:
    df = get_table()
    st.session_state.df = df


df = st.session_state.df

st.title("Gráficos")

years: list = df["ano"].unique().tolist()

option = st.selectbox("Selecione um ano", years)

st.write("You selected:", option)

with st.expander("Valor Total X Tipo de Despesa"):
    df_grouped_1 = df[["tipo_despesa", "valor_liquido"]].groupby("tipo_despesa").sum()
    st.bar_chart(df_grouped_1, horizontal=True, x_label="Valor total em R$")

with st.expander("Valor Total X Deputado"):
    df_grouped_2 = df[["nome_deputado", "valor_liquido"]].groupby("nome_deputado").sum()
    st.bar_chart(df_grouped_2, horizontal=True, x_label="Valor total em R$")

df_grouped = df
st.dataframe(df_grouped)
