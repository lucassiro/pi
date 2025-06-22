import altair as alt
import pandas as pd
import streamlit as st


def create_bar_plot(
    df: pd.DataFrame,
    x: str,
    y: str,
    x_label: str,
    y_label: str,
    title: str,
    limit: int | None = None,
    agg_function: str = "sum",
) -> None:
    df[y] = df[y].astype(str)

    match agg_function:
        case "sum":
            grouped_df = df[[y, x]].groupby(y).sum()

        case "count":
            grouped_df = df[[y, x]].groupby(y).count()

        case "mean":
            grouped_df = df[[y, x]].groupby(y).mean()

        case "median":
            grouped_df = df[[y, x]].groupby(y).median()

        case "max":
            grouped_df = df[[y, x]].groupby(y).max()

        case "min":
            grouped_df = df[[y, x]].groupby(y).min()
        case _:
            grouped_df = df[[y, x]].groupby(y).sum()

    grouped_df = grouped_df.reset_index()
    print(len(grouped_df))
    print(type(len(grouped_df)))

    bar_limit = 100
    if limit is None and len(grouped_df) > bar_limit:
        st.warning(f"A quantidade de resultados é de {len(grouped_df)}, limitando aos {bar_limit} maiores resultados.")
        limit = bar_limit

    if limit:
        grouped_df = grouped_df.sort_values(by=x, ascending=False).iloc[:limit]

    st.write(
        alt.Chart(grouped_df)
        .mark_bar()
        .encode(
            y=alt.Y(y, title=y_label, sort="-x"),
            x=alt.X(x, title=x_label),
        )
        .properties(title=title)
    )
