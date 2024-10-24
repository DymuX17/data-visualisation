import influxdb_client, os, time
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import streamlit as st
import datetime
from dotenv import load_dotenv


class InitDB:
    _conn_init = False
    load_dotenv()

    def __init__(self):
        if not InitDB._conn_init:
            self.token = os.getenv("INFLUX_TOKEN")
            self.org = os.getenv("INFLUX_ORG")
            self.url = os.getenv("INFLUX_URL")
            self.bucket = os.getenv("INFLUX_BUCKET")
            self.client = None
            self.write_api = None
            self.query_api = None
            self.name = None

            self.connect()
            InitDB._conn_init = True

    def connect(self):
        self.client = InfluxDBClient(url=self.url, token=self.token, org=self.org)
        self.write_api = self.client.write_api(write_options=SYNCHRONOUS)
        self.query_api = self.client.query_api()

    def get_formatted_time(self):
        st.session_state[self.name] = datetime.datetime.now().strftime("%H:%M:%S")
