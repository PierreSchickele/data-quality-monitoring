import streamlit as st
import duckdb
import plotly.express as px

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

# Filter data for the selected sensor
df_selected = df[df["sensor_id"] == selected_sensor].copy()

# Ensure the date column is in datetime format
df_selected["date"] = df_selected["date"].astype("datetime64[ns]")

# Plot the evolution of the visits count per day
fig = px.line(
    df_selected,
    x="date",
    y="visits_count",
    title=f"Daily Visits for Sensor {selected_sensor}",
    labels={"visits_count": "Visits Count", "date": "Date"},
)

st.plotly_chart(fig)
