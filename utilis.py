import streamlit as st
# from init_db_conn import InitDB
# from visualise_data import Visualise

# vis = Visualise()
# bucket = st.session_state.b


def write_combined_query(bucket):
    query = f"""
    from(bucket: "{bucket}")
    |> range(start: -1m, stop: now())  // Zakres czasowy ostatnich 1 minut
    |> filter(fn: (r) =>
        r["_measurement"] == "ErrorStats1" or
        r["_measurement"] == "ErrorStats11" or
        r["_measurement"] == "ErrorStats111" or
        r["_measurement"] == "ErrorStats1111" or
        r["_measurement"] == "ErrorStats2" or
        r["_measurement"] == "ErrorStats22" or
        r["_measurement"] == "ErrorStats222" or
        r["_measurement"] == "ErrorStats2222" or
        r["_measurement"] == "ErrorValues" or
        r["_measurement"] == "sin_val1" or
        r["_measurement"] == "test-topic" or
        r["_measurement"] == "test-topic2" or
        r["_measurement"] == "test-topic3" or
        r["_measurement"] == "test-topic4" or
        r["_measurement"] == "IE" or
        r["_measurement"] == "ISE" or
        r["_measurement"] == "IAE" or
        r["_measurement"] == "IE2" or
        r["_measurement"] == "ISE2" or
        r["_measurement"] == "IAE2"
    )
    |> filter(fn: (r) =>
        r["_field"] == "error_signal" or
        r["_field"] == "error_signal1" or
        r["_field"] == "error_signal2" or
        r["_field"] == "max" or
        r["_field"] == "mean" or
        r["_field"] == "min" or
        r["_field"] == "std" or
        r["_field"] == "value" or
        r["_field"] == "field2" or
        r["_field"] == "field3" or
        r["_field"] == "IE" or
        r["_field"] == "ISE" or
        r["_field"] == "IAE" or
        r["_field"] == "IE2" or
        r["_field"] == "ISE2" or
        r["_field"] == "IAE2"
    )
    |> aggregateWindow(every: 1s, fn: last, createEmpty: false)  // Agregacja danych co sekundę
    |> yield(name: "last")
    """
    return query







    # sin_val1
    # field2
