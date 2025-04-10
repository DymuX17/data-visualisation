import os
import time
import pandas as pd
import altair as alt
import streamlit as st
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from init_db_conn import InitDB
import utilis

class VisualiseSnap7(InitDB):
    def __init__(self):
        super().__init__()
        self.token = os.getenv("INFLUX_TOKEN")
        self.org = os.getenv("INFLUX_ORG")
        self.url = os.getenv("INFLUX_URL")
        self.bucket = os.getenv("INFLUX_BUCKET")
        self.client = InfluxDBClient(url=self.url, token=self.token, org=self.org)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.client.query_api()

        if 'data_snap7' not in st.session_state:
            st.session_state.data_snap7 = {
                'wartosc_zadana1': pd.DataFrame(columns=["time", "value"]),
                'temperatura1': pd.DataFrame(columns=["time", "value"]),
                'df_IE2': pd.DataFrame(columns=["time", "value"]),
                'df_ISE2': pd.DataFrame(columns=["time", "value"]),
                'df_IAE2': pd.DataFrame(columns=["time", "value"]),
                'df_max2': pd.DataFrame(columns=["time", "value"]),
                'df_min2': pd.DataFrame(columns=["time", "value"]),
                'df_mean2': pd.DataFrame(columns=["time", "value"]),
                'df_std2': pd.DataFrame(columns=["time", "value"]),
            }

    def reset_streaming(self):
        for key in st.session_state.data_snap7:
            st.session_state.data_snap7[key] = pd.DataFrame(columns=["time", "value"])
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
            "test-topic3": "wartosc_zadana1",
            "test-topic4": "temperatura1",
            "IE2": "df_IE2",
            "ISE2": "df_ISE2",
            "IAE2": "df_IAE2",
            "ErrorStats2": "df_max2",
            "ErrorStats22": "df_min2",
            "ErrorStats222": "df_mean2",
            "ErrorStats2222": "df_std2",
        }

        for measurement, key in data_mapping.items():
            if measurement in ["ErrorStats2", "ErrorStats22", "ErrorStats222", "ErrorStats2222"]:
                filtered_df = df[df["measurement"] == measurement]
            elif "topic" in measurement:
                filtered_df = df[(df["measurement"] == measurement) & (df["field"] == "field3")]
            else:
                filtered_df = df[(df["measurement"] == measurement) & (df["field"] == measurement)]

            filtered_df = filtered_df[["time", "value"]]

            if not filtered_df.empty:
                if st.session_state.data_snap7[key].empty:
                    st.session_state.data_snap7[key] = filtered_df
                else:
                    st.session_state.data_snap7[key] = pd.concat(
                        [st.session_state.data_snap7[key], filtered_df],
                        ignore_index=True
                    ).drop_duplicates().sort_values(by="time").tail(1600)

    def render_chart(self, key, title):
        st.subheader(title)
        if not st.session_state.data_snap7[key].empty:
            data = st.session_state.data_snap7[key]
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
        """
        Renderuje wykres łączony dla dwóch kluczy danych.
        """
        st.subheader(title)

        # Sprawdzenie, czy oba klucze mają dane
        if not st.session_state.data_snap7[key1].empty and not st.session_state.data_snap7[key2].empty:
            df1 = st.session_state.data_snap7[key1].copy()
            df2 = st.session_state.data_snap7[key2].copy()

            # Dodanie kolumny źródła, aby rozróżnić dane
            df1['source'] = 'Temperatura'
            df2['source'] = 'Wartość zadana'

            # Połączenie danych w jeden DataFrame
            combined_df = pd.concat([df1, df2], ignore_index=True).drop_duplicates().sort_values(by="time")

            # Tworzenie wykresu za pomocą Altair
            chart = alt.Chart(combined_df).mark_line().encode(
                x=alt.X("time", title="Czas"),
                y=alt.Y("value", title="Wartość", scale=alt.Scale(zero=False)),
                color=alt.Color("source", legend=alt.Legend(title="Źródło")),
                tooltip=["time", "value", "source"]
            ).properties(
                width="container",
                height=325
            )

            # Wyświetlenie wykresu
            st.altair_chart(chart, use_container_width=True)
        else:
            st.warning(f"Brak dostępnych danych dla {title}")


    def render_combined_chart_with_stats(self, title):
        st.subheader(title)

        data_frames = []
        for key, label in {
            "df_max2": "Maksimum",
            "df_min2": "Minimum",
            "df_mean2": "Średnia",
            "df_std2": "Odch. stand."
        }.items():
            if not st.session_state.data_snap7[key].empty:
                df = st.session_state.data_snap7[key].copy()
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
        st.header('Monitorowanie i analiza jakości sterowania piecem w czasie rzeczywistym - S7Conn')
        st.caption("Dane są odświeżane co 1 sekundę")

        st.sidebar.button("Zresetuj wizualizację", on_click=self.reset_streaming)

        @st.fragment(run_every=1.0)
        def show_charts():
            self.fetch_all_data(self.bucket)

            row1_column1, row1_column2 = st.columns([2, 2])
            row2_column1, row2_column2 = st.columns([2, 2])

            with row1_column1:
                self.render_combined_chart("wartosc_zadana1", "temperatura1", "Wykres temperatury i wartości zadanej")

            with row1_column2:
                self.render_combined_chart_with_stats("Wykres statystyk")

            with row2_column1:
                self.render_chart("df_ISE2", "Wskaźnik ISE")

            with row2_column2:
                self.render_chart("df_IAE2", "Wskaźnik IAE")

        show_charts()