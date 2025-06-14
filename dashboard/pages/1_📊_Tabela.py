import streamlit as st
from pages.utils.table import get_table

if "df" not in st.session_state:
    df = get_table()
    st.session_state.df = df

df = st.session_state.df

page_size = 100
page_num = st.slider("Page number", 1, (len(df) // page_size) + 1)

start_index = (page_num - 1) * page_size
end_index = start_index + page_size
st.dataframe(df[start_index:end_index])
