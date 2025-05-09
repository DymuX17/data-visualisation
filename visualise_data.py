import os
import time
import pandas as pd
import altair as alt
import streamlit as st
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from init_db_conn import InitDB
import utilis

class Visualise(InitDB):
    def __init__(self):
        super().__init__()
        self.token = os.getenv("INFLUX_TOKEN")
        self.org = os.getenv("INFLUX_ORG")
        self.url = os.getenv("INFLUX_URL")
        self.bucket = os.getenv("INFLUX_BUCKET")
        self.client = InfluxDBClient(url=self.url, token=self.token, org=self.org)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.client.query_api()

        if 'data' not in st.session_state:
            st.session_state.data = {
                'wartosc_zadana': pd.DataFrame(columns=["time", "value"]),
                'temperatura': pd.DataFrame(columns=["time", "value"]),
                'df_IE': pd.DataFrame(columns=["time", "value"]),
                'df_ISE': pd.DataFrame(columns=["time", "value"]),
                'df_IAE': pd.DataFrame(columns=["time", "value"]),
                'uchyb': pd.DataFrame(columns=["time", "value"]),
                'df_max': pd.DataFrame(columns=["time", "value"]),
                'df_min': pd.DataFrame(columns=["time", "value"]),
                'df_mean': pd.DataFrame(columns=["time", "value"]),
                'df_std': pd.DataFrame(columns=["time", "value"]),
            }

    def reset_streaming(self):
        for key in st.session_state.data:
            st.session_state.data[key] = pd.DataFrame(columns=["time", "value"])
        st.info("Wizualizacja została zresetowana.")

    def fetch_all_data(self, bucket):
        query = utilis.write_combined_query(bucket)

        try:
            tables = self.query_api.query(query)
        except Exception as e:
            return

        records = []
        for table in tables:
            for record in table.records:
                records.append({
                    "time": record.get_time().strftime('%H:%M:%S'),
                    "measurement": record.get_measurement(),
                    "field": record.get_field(),
                    "value": record.get_value()
                })

        if not records:
            return

        df = pd.DataFrame(records)

        data_mapping = {
            "test-topic": "wartosc_zadana",
            "test-topic2": "temperatura",
            "IE": "df_IE",
            "ISE": "df_ISE",
            "IAE": "df_IAE",
            "ErrorValues": "uchyb",
            "ErrorStats1": "df_max",
            "ErrorStats11": "df_min",
            "ErrorStats111": "df_mean",
            "ErrorStats1111": "df_std",
        }

        for measurement, key in data_mapping.items():
            if measurement == "ErrorValues":
                filtered_df = df[(df["measurement"] == measurement) & (df["field"] == "error_signal1")]
            elif measurement in ["ErrorStats1", "ErrorStats11", "ErrorStats111", "ErrorStats1111"]:
                filtered_df = df[df["measurement"] == measurement]
            elif "topic" in measurement:
                filtered_df = df[(df["measurement"] == measurement) & (df["field"] == "field3")]
            else:
                filtered_df = df[(df["measurement"] == measurement) & (df["field"] == measurement)]

            filtered_df = filtered_df[["time", "value"]]

            if not filtered_df.empty:
                if st.session_state.data[key].empty:
                    st.session_state.data[key] = filtered_df
                else:
                    st.session_state.data[key] = pd.concat(
                        [st.session_state.data[key], filtered_df],
                        ignore_index=True
                    ).drop_duplicates().sort_values(by="time").tail(1600)

    def render_chart(self, key, title):
        st.subheader(title)
        if not st.session_state.data[key].empty:
            data = st.session_state.data[key]
            chart = alt.Chart(data).mark_line().encode(
                x=alt.X("time", title="Czas"),
                y=alt.Y("value", title="Wartość", scale=alt.Scale(zero=False)),
                tooltip=["time", "value"]
            ).properties(
                width="container",
                height=325
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning(f'Brak dostępnych danych - {title}')

    def render_combined_chart(self, key1, key2, title):
        st.subheader(title)

        if not st.session_state.data[key1].empty and not st.session_state.data[key2].empty:
            df1 = st.session_state.data[key1].copy()
            df2 = st.session_state.data[key2].copy()

            df1['source'] = 'temperatura'
            df2['source'] = 'wartość zad.'

            combined_df = pd.concat([df1, df2], ignore_index=True).drop_duplicates().sort_values(by="time")

            chart = alt.Chart(combined_df).mark_line().encode(
                x=alt.X("time", title="Czas"),
                y=alt.Y("value", title="Wartość", scale=alt.Scale(zero=False)),
                color=alt.Color("source", legend=alt.Legend(title="", orient="top-left")),
                tooltip=["time", "value", "source"]
            ).properties(
                width="container",
                height=325
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning(f'Brak dostępnych danych - {title}')

    def render_combined_chart_with_stats(self, title):
        st.subheader(title)

        data_frames = []
        for key, label in {
            "df_max": "Maksimum",
            "df_min": "Minimum",
            "df_mean": "Średnia",
            "df_std": "Odch. stand."
        }.items():
            if not st.session_state.data[key].empty:
                df = st.session_state.data[key].copy()
                df["source"] = label
                data_frames.append(df)

        if data_frames:
            combined_df = pd.concat(data_frames, ignore_index=True).drop_duplicates().sort_values(by="time")

            chart = alt.Chart(combined_df).mark_line().encode(
                x=alt.X("time", title="Czas"),
                y=alt.Y("value", title="Wartość", scale=alt.Scale(zero=False)),
                color=alt.Color("source", legend=alt.Legend(title="Źródło")),
                tooltip=["time", "value", "source"]
            ).properties(
                width="container",
                height=325
            )
            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning("Brak dostępnych danych dla statystyk.")

    def plot_sin(self):
        st.header('Monitorowanie i analiza jakości sterowania piecem w czasie rzeczywistym - OPC-UA')
        st.caption("Dane są odświeżane co 1 sekundę")

        st.sidebar.button("Zresetuj wizualizację", on_click=self.reset_streaming)

        @st.fragment(run_every=1.0)
        def show_charts():
            self.fetch_all_data(self.bucket)

            row1_column1, row1_column2 = st.columns([2, 2])
            row2_column1, row2_column2 = st.columns([2, 2])

            with row1_column1:
                self.render_combined_chart("wartosc_zadana", "temperatura", "Wykres temperatury i wartości zadanej")

            with row1_column2:
                self.render_combined_chart_with_stats("Wykres statystyk")

            with row2_column1:
                self.render_chart("df_ISE", "Wskaźnik ISE")

            with row2_column2:
                self.render_chart("df_IAE", "Wskaźnik IAE")




        show_charts()