import streamlit as st
import duckdb
import plotly.express as px

# Define path of Parquet file
PROCESSED_DATA_PATH = "./data/processed/final_data.parquet"

# Load data with DuckDB
query = f"SELECT * FROM '{PROCESSED_DATA_PATH}'"
df = duckdb.query(query).df()

# Sidebar
# Select the store
st.sidebar.header("Filter data by store")
stores = df["store_name"].unique()
selected_store = st.sidebar.selectbox("Select a store :", stores)

# Select the sensors
filtered_df = df[df["store_name"] == selected_store]
sensors = filtered_df["sensor_id"].unique()
selected_sensor = st.sidebar.selectbox("Select a sensor :", sensors)

# Select the period
period_options = {"Week": 7, "Month": 30, "Year": 365}
selected_period = st.sidebar.radio("Print data for:", list(period_options.keys()))

# Filter data for the selected period
filtered_df = filtered_df[filtered_df["sensor_id"] == selected_sensor]
filtered_df = filtered_df.sort_values("date", ascending=True)
filtered_df = filtered_df.iloc[-period_options[selected_period] :]

st.write(f"You selected sensor: {selected_sensor}")

# Ensure the date column is in datetime format
filtered_df["date"] = filtered_df["date"].astype("datetime64[ns]")

# Sort data by date
filtered_df = filtered_df.sort_values(by="date", ascending=True)

# Print the dataframe for the selected sensor
st.dataframe(filtered_df.reset_index(drop=True))

# Trace the plot
fig = px.line(
    filtered_df,
    x="date",
    y=["visits_count", "avg_visits_last_4_same_day"],
    title=f"Daily Visits and 4-Day Moving Average for Sensor {selected_sensor}",
    labels={"value": "Visits Count", "date": "Date"},
)

fig.update_traces(mode="lines+markers")

st.plotly_chart(fig)
