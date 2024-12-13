from visualise_data import Visualise
import streamlit as st

if __name__ == '__main__':

    if "visualise" not in st.session_state:
        st.session_state.visualise = Visualise()

pages = {
    "General data visualisation": [
        st.Page(lambda: st.session_state.visualise.plot_sin(), title="Sinus Visualisation"),
        st.Page("page1.py", title="Page 1"),
    ],
    "Other aspects visualisation": [
        st.Page("page2.py", title="Page 2"),
    ],
}

# Ustawienie nawigacji
pg = st.navigation(pages)

# Wywołanie bieżącej strony
pg.run()




