import streamlit as st
import duckdb

# Define path of Parquet file
PROCESSED_DATA_PATH = "./data/processed/final_data.parquet"

# Load data with DuckDB
query = f"SELECT * FROM '{PROCESSED_DATA_PATH}'"
df = duckdb.query(query).df()

# Selectbox of the existing sensors
sensor_ids = df["sensor_id"].unique()
selected_sensor = st.selectbox("Select a sensor :", sensor_ids)

st.write(f"You chose sensor: {selected_sensor}")

# Print the dataframe for the selected sensor
st.dataframe(df[df["sensor_id"] == selected_sensor].reset_index(drop=True))
