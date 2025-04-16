# 📊 Process Data Visualization Dashboard

This project is a continuation of the process data acquisition system and is designed for **visualizing, monitoring, and analyzing real-time process data**. The data comes from two parallel industrial process simulations (transmitted via OPC UA and S7Comm communication protocols), previously acquired and stored in **InfluxDB**.

---

## 🔍 Project Overview

The application allows you to:

- Display real-time charts of setpoint and temperature values  
- Visualize statistics: maximum, minimum, mean, and standard deviation  
- Monitor control quality indicators: **ISE**, **IAE**  
- Compare data from two communication sources: **OPC UA** and **S7Comm**

The app is built using **Streamlit** and uses **Altair** for generating interactive charts.

---

## 🧱 System Architecture

### Data Flow:
1. Data is generated and stored in InfluxDB in a separate project.  
2. This visualization app retrieves the data using **InfluxDBClient**.  
3. Streamlit renders a user interface with charts updated every second.

---


## 🗺️ System Diagram

  <img width="183" alt="InfluxDB-Streamlit" src="https://github.com/user-attachments/assets/70100a1c-5c7f-4116-aee9-8aaf6f13a0ca" />


---


## 🖥️ User Interface

The app contains two separate views:
- **OPC-UA** – displays data acquired via the OPC UA protocol  
- **S7Comm** – displays data acquired via the S7comm protocol

Each tab includes:
- A chart comparing setpoint and measured temperature  
- A chart with statistical data (min, max, mean, std)  
- A chart showing control quality index IAE  
- A chart showing control quality index ISE  
- A reset button to clear visualization data

---

## 📸  UI View

Below are the screenshots of the application running:

**Page view with charts and an expanded sidebar with a possible choice of two available visualizations and a reset button**

![System_UI_1](https://github.com/user-attachments/assets/96d1ed34-b76f-4477-9b2c-3b62185cc9f9)

**Zoom in on the statistics chart**

![System_UI_2_statistics_chart](https://github.com/user-attachments/assets/28006d7a-7dc0-4354-8538-00c51e4ba4d7)

**Standard view of charts with sidebar collapsed**

![System_UI_3](https://github.com/user-attachments/assets/7ec43070-d6b9-4ea2-8153-1bd7e2c107ad)




---

## 📁 Project Structure

```
📂 project_root/
│
├── main.py                    # Main Streamlit application
├── visualise_data.py          # Class for handling OPC UA data
├── visualise_data_snap7.py    # Class for handling S7comm data
├── init_db_conn.py            # InfluxDB connection initializer
├── utilis.py                  # Flux query builder for InfluxDB
├── .env                       # Environment variable configuration (see below)
```
---


## ⚙️ Requirements

- Python 3.9  
- Docker (for running InfluxDB)  
- Streamlit  
- InfluxDB Python Client  
- Altair  
- Pandas, NumPy  

---

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/DymuX17/data-visualisation.git
   cd data-visualisation
   ```

3. Install dependencies:
   ```bash
   pip install streamlit influxdb-client altair pandas numpy python-dotenv

   ```
5. Create a `.env` file with your InfluxDB configuration:
   ```bash
   INFLUX_URL=http://localhost:8086
   INFLUX_TOKEN=your_token
   INFLUX_ORG=your_org
   INFLUX_BUCKET=your_bucket
   ```

7. Run the application:
   ```bash
   streamlit run main.py
   ```
   
---


## 🛡️ Technologies Used

- Python 3.9
- Streamlit – for fast web UI development  
- Altair – for interactive visualizations  
- InfluxDB – time-series database  
- Docker – container for running InfluxDB  
- Pandas / NumPy – for data processing  

---

## 📌 Notes

This project assumes a pre-configured simulation running in TIA Portal with communication over OPC UA and/or S7comm.  
This module **does not generate data**, it only fetches and visualizes existing data.

---
