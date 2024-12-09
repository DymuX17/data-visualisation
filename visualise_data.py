import influxdb_client, os, time
import streamlit as st
from streamlit import fragment
import pandas as pd
from init_db_conn import InitDB
import datetime


class Visualise(InitDB):
    def __init__(self):
        super().__init__()
        st.set_page_config("st.fragment_visualisation", page_icon="*")

    def plot_sin(self):
        st.header('Sinus visualisation')
        st.caption("Every second chart is updated with latest data from `InfluxDB`")

        chart_placeholder = st.empty()

        if st.button("Reset streaming") or "df" not in st.session_state:
            st.session_state.df = pd.DataFrame([])

        @st.fragment(run_every=0.5)
        def write_chart():
            query_sin = f"""
            from(bucket: "{self.bucket}")
            |> range (start: -2s)
            """
            data = []
            tables = self.query_api.query(query_sin)
            for table in tables:
                for record in table.records:
                    formatted_time = record.get_time().strftime('%H:%M:%S')
                    data.append({"time": formatted_time, "value": record.get_value()})
            if data:
                new_data = pd.DataFrame(data)
                st.session_state.df = pd.concat([st.session_state.df, new_data], ignore_index=True)
                df = st.session_state.df
                st.scatter_chart(df, x='time', y='value', color='#add8e6',
                                 use_container_width=True)

        with chart_placeholder:
            write_chart()




            def generate_chart():
                # rng = np.random.default_rng()
                new_data = pd.DataFrame(rng.random((2, 3)), columns=["a", "b", "c"])
                st.session_state.chart_data = pd.concat([st.session_state.chart_data, new_data], ignore_index=True)
                chart_data = st.session_state.chart_data
                columns = st.multiselect("Select columns", chart_data.columns.tolist())
                st.bar_chart(chart_data if not columns else chart_data[columns])
                st.caption(f"Last updated {datetime.datetime.now()}")



