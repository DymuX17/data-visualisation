# data-visualisation

This project visualizes data from an InfluxDB bucket using Streamlit. It provides a real-time scatter chart for sinusoidal data visualization. This project is a preliminary version of a project created to read process data from an automation system stored in 'InfluxDB' time database. The final version will visualise various data on web browser page using Streamlit library. The data will be got from the real automation system that is plant for heat generation and distribution.

Project Structure

init_db_conn.py: Initializes the connection to InfluxDB.

visualise_data.py: Queries and visualizes the data.

main.py: Entry point for running the visualization.

## Features

- **Initialize InfluxDB Connection**: Handles connecting to the InfluxDB instance.
- **Queries the database**: gets data previously stored in InfluxDB time database.
- **Plots Sinusoidal Data**: Generates web app and plots scatter chart on web browser.
- **Refresh visualisation**: Uses `streamlit_autorefresh` for data refresh and provide real time visualisation.

## Project Structure

- **`init_db_conn.py`**: Contains the `InitDB` class responsible for connecting to InfluxDB using environment variables for configuration.
- **`visualise_data.py`**: Gets data previously stored in InfluxDB time database and generates web app and plots scatter chart on web browser.
- **`main.py`**: The entry point of the project, functions are executed there. 


## Dependencies

- Python 3.x
- InfluxDB (best to run it as a docker image)
- Required Python libraries:
  - `influxdb-client`
  - `numpy`
  - `pandas`
  - `python-dotenv`
  - `streamlit-autorefresh`


Install the required libraries using:

```bash
pip install influxdb-client numpy pandas matplotlib python-dotenv streamlit-autorefresh
