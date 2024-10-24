import influxdb_client, os, time
import streamlit as st
import pandas as pd
from init_db_conn import InitDB
from streamlit_autorefresh import st_autorefresh


class Visualise(InitDB):
    def __init__(self):
        super().__init__()

    def plot_sin(self):
        st_autorefresh(interval=2000, key="st.session_state.df")

        chart_placeholder = st.empty()

        if "df" not in st.session_state:
            st.session_state.df = pd.DataFrame([])

        while True:
            query = f"""
            from(bucket: "{self.bucket}")
            |> range (start: -5m)
            """
            data = []
            tables = self.query_api.query(query)
            for table in tables:
                for record in table.records:
                    data.append({"time": record.get_time(), "value": record.get_value()})
            if data:
                st.session_state.df = pd.DataFrame(data)

                st.session_state.df['time'] = pd.to_datetime(st.session_state.df['time'])
                st.session_state.df['time_formatted'] = st.session_state.df['time'].dt.strftime('%H:%M:%S:%MS')
                st.session_state.df = st.session_state.df.drop(columns=['time'])

                with chart_placeholder:
                    st.header('Sinus visualisation')
                    st.scatter_chart(st.session_state.df, x='time_formatted', y='value', color='#add8e6',
                                     use_container_width=True)

            print(st.session_state.df.dtypes)

            time.sleep(2)
