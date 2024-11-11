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

        # while True:
        @st.fragment(run_every=1)
        def write_chart():
            query = f"""
            from(bucket: "{self.bucket}")
            |> range (start: -1m)
            """
            data = []
            tables = self.query_api.query(query)
            for table in tables:
                for record in table.records:
                    data.append({"time": record.get_time(), "value": record.get_value()})
            if data:
                st.session_state.df = pd.DataFrame(data)

                st.session_state.df['time'] = pd.to_datetime(st.session_state.df['time'])
                st.session_state.df['time_formatted'] = st.session_state.df['time'].dt.strftime('%H:%M:%S')
                st.session_state.df = st.session_state.df.drop(columns=['time'])
                st.scatter_chart(st.session_state.df, x='time_formatted', y='value', color='#add8e6',
                                 use_container_width=True)

        with chart_placeholder:
            write_chart()

