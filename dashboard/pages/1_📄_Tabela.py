import streamlit as st
from pages.utils.table import get_table

if "full_df" not in st.session_state:
    st.session_state.full_df = get_table()
full_df = st.session_state.full_df

num_rows = 100
page_num = st.slider("Page number", 1, (len(full_df) // num_rows) + 1)

start_index = (page_num - 1) * num_rows
end_index = start_index + num_rows
calculated_height = (num_rows + 1) * 35 + 3
st.dataframe(full_df[start_index:end_index], height=3550)
