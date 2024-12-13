import streamlit as st
# from init_db_conn import InitDB
# from visualise_data import Visualise

# vis = Visualise()
# bucket = st.session_state.b


def write_query(bucket, measurement_n, field_n):
    vis = st.session_state.visualise
    query_sin = f"""
    from(bucket: "{bucket}")
    |> range (start: -2s)
    |> filter(fn: (r) => r._measurement == "{measurement_n}")
    |> filter(fn: (r) => r._field == "{field_n}")
    """
    return query_sin

    # sin_val1
    # field2