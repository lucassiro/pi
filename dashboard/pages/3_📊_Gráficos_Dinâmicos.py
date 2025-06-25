import streamlit as st
from pages.utils.plots import create_bar_plot
from pages.utils.table import get_table

st.markdown("# Gráficos Dinâmicos")
# ----------------------------
if "full_df" not in st.session_state:
    st.session_state.full_df = get_table()
full_df = st.session_state.full_df

# ----------------------------

y_columns = [
    "tipo_despesa",
    "nome_deputado",
    "ano",
    "mes",
    "sigla_partido",
    "sigla_uf",
    "nome_fornecedor",
]

y: str = st.selectbox("Selecione a variável de interesse:", y_columns)
x: str = st.selectbox("Selecione a coluna que será agregada:", ["valor_documento"])
operation = st.selectbox(
    "Selecione a função de agregação:", ["soma", "quantidade", "media", "mediana", "valor máximo", "valor mínimo"]
)

match operation:
    case "soma":
        agg_function = "sum"

    case "quantidade":
        agg_function = "count"

    case "media":
        agg_function = "mean"

    case "mediana":
        agg_function = "median"

    case "valor máximo":
        agg_function = "max"

    case "valor mínimo":
        agg_function = "min"

    case _:
        agg_function = "sum"

create_bar_plot(
    df=full_df,
    x=x,
    y=y,
    x_label=f"{x} ({operation})",
    y_label=y,
    title=f"{y} X {x} ({operation})",
    agg_function=agg_function,
)
