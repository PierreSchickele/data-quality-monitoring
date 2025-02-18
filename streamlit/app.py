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

# Sort by date
df_selected = df_selected.sort_values(by="date")

# Plot the evolution of the visits count per day and the 4-day average
fig = px.line(
    df_selected,
    x="date",
    y=["visits_count", "avg_visits_last_4_same_day"],
    title=f"Daily Visits and 4-Day Moving Average for Sensor {selected_sensor}",
    labels={"value": "Visits Count", "date": "Date"},
)

fig.update_traces(mode="lines+markers")

st.plotly_chart(fig)
