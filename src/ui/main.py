import streamlit as st

from src.ui.configs import get_streamlit_config

streamlit_config = get_streamlit_config()
st.set_page_config(
    page_title=streamlit_config["page_title"],
    page_icon=streamlit_config["page_icon"],
    layout=streamlit_config["layout"],
)

st.write("# Agents playground")
