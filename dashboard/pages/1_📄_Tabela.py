import streamlit as st
from pages.utils.table import get_table

if "full_df" not in st.session_state:
    st.session_state.full_df = get_table()
full_df = st.session_state.full_df

page_size = 100
page_num = st.slider("Page number", 1, (len(full_df) // page_size) + 1)

start_index = (page_num - 1) * page_size
end_index = start_index + page_size
st.dataframe(full_df[start_index:end_index])
