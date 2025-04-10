from visualise_data import Visualise
from visualise_data_snap7 import VisualiseSnap7
import streamlit as st

st.set_page_config("st.fragment_visualisation", page_icon="*", layout="wide")

if "visualise1" not in st.session_state and "visualise2" not in st.session_state:
    st.session_state.visualise1 = Visualise()
    st.session_state.visualise2 = VisualiseSnap7()


def home():
    st.session_state.visualise1.plot_sin()


pages = {
    "General data visualisation OPC-UA": [
        st.Page(home, title="OPC-UA", icon="📈"),
    ],
    "Second data visualisation snap7": [
        st.Page(lambda: st.session_state.visualise2.plot_sin(), title="S7Conn", icon="📉"),
    ],
}

pg = st.navigation(pages)
pg.run()
