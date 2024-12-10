import influxdb_client, os, time
import streamlit as st
from streamlit import fragment
import pandas as pd
from init_db_conn import InitDB
import datetime


class Visualise(InitDB):
    def __init__(self):
        super().__init__()
        st.set_page_config("st.fragment_visualisation", page_icon="*", layout="wide")

        # Repeat the chart placement logic here

    def plot_sin(self):
        st.header('Sinus visualisation')
        st.caption("Every second chart is updated with latest data from `InfluxDB`")

        chart_placeholder = st.empty()
        chart_placeholder_v2 = st.empty()

        if st.button("Reset streaming"): # or "df" not in st.session_state:
            st.session_state.df = pd.DataFrame([])

        if 'df_chart' not in st.session_state:
            st.session_state.df_chart = pd.DataFrame(columns=["time", "value"])

        if 'df_opcua' not in st.session_state:
            st.session_state.df_opcua = pd.DataFrame(columns=["time", "value"])


        @st.fragment(run_every=0.5)
        def write_chart():
            query_sin = f"""
            from(bucket: "{self.bucket}")
            |> range (start: -2s)
            |> filter(fn: (r) => r._measurement == "sin_val1")
            |> filter(fn: (r) => r._field == "field2")
            """
            data = []
            tables = self.query_api.query(query_sin)
            for table in tables:
                for record in table.records:
                    formatted_time = record.get_time().strftime('%H:%M:%S')
                    data.append({"time": formatted_time, "value": record.get_value()})
            if data:
                new_data = pd.DataFrame(data)
                st.session_state.df_chart = pd.concat([st.session_state.df_chart, new_data], ignore_index=True)
                df = st.session_state.df_chart
                st.scatter_chart(df, x='time', y='value', color='#add8e6',
                                 use_container_width=True)

        @st.fragment(run_every=0.5)
        def write_opcua():
            query_sin = f"""
            from(bucket: "{self.bucket}")
            |> range (start: -2s)
            |> filter(fn: (r) => r._measurement == "opc_val1")
            |> filter(fn: (r) => r._field == "field3")
            """
            data = []
            tables = self.query_api.query(query_sin)
            for table in tables:
                for record in table.records:
                    formatted_time = record.get_time().strftime('%H:%M:%S')
                    data.append({"time": formatted_time, "value": record.get_value()})
            if data:
                new_data = pd.DataFrame(data)
                st.session_state.df_opcua = pd.concat([st.session_state.df_opcua, new_data], ignore_index=True)
                df = st.session_state.df_opcua
                st.scatter_chart(df, x='time', y='value', color='#add8e6',
                                 use_container_width=True)

        row1_column1, row1_column2 = st.columns([2, 2])
        row2_column1, row2_column2 = st.columns([2, 2])

        with row1_column1:
            write_chart()
        with row1_column2:
            write_opcua()
        with row2_column1:
            write_chart()
        with row2_column2:
            write_opcua()

        '''
        with chart_placeholder:
            write_chart()
        with chart_placeholder_v2:
            write_chart()
        '''


'''
            def generate_chart():
                # rng = np.random.default_rng()
                new_data = pd.DataFrame(rng.random((2, 3)), columns=["a", "b", "c"])
                st.session_state.chart_data = pd.concat([st.session_state.chart_data, new_data], ignore_index=True)
                chart_data = st.session_state.chart_data
                columns = st.multiselect("Select columns", chart_data.columns.tolist())
                st.bar_chart(chart_data if not columns else chart_data[columns])
                st.caption(f"Last updated {datetime.datetime.now()}")


'''
