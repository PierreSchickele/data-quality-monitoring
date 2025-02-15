from read_raw_data import get_raw_data
import duckdb
import os

# Load raw rata
df = get_raw_data()
df = df[df["sensor_id"] == "ALL"]

print(df.head())
print(df.describe())

# Group by day
df_day = duckdb.sql(
    "SELECT date, store_name, sensor_id, SUM(visits_count) as visits_count "
    "FROM df "
    "GROUP BY date, store_name, sensor_id "
    "ORDER BY store_name, date"
).df()

print(df_day.head())
print(df_day.describe())

# Remove rows with null values
df_cleaned = df_day.copy().dropna()

print(df_cleaned.head())
print(df_cleaned.describe())

# Add day_of_week column
df_cleaned["day_of_week"] = df_cleaned["date"].dt.dayofweek

print(df_cleaned.head())

# Average on the last 4 similar days
df_4days = duckdb.sql(
    "SELECT date, store_name, sensor_id, visits_count, AVG(visits_count) "
    "OVER (PARTITION BY day_of_week, store_name, sensor_id "
    "ORDER BY date "
    "ROWS BETWEEN 3 PRECEDING AND CURRENT ROW "
    ") AS avg_visits_last_4_same_day "
    "FROM df_cleaned "
    "ORDER BY store_name, date"
).df()

print(df_4days.head())

# Percentage change
df_4days.loc[:, "pct_change"] = (
    df_4days["visits_count"] - df_4days["avg_visits_last_4_same_day"]
) / df_4days["avg_visits_last_4_same_day"]

print(df_4days.head(40))

df_final = df_4days.copy()

# Save DataFrame to Parquet
PROCESSED_DATA_PATH = "./data/processed/"
parquet_path = os.path.join(PROCESSED_DATA_PATH, "final_data.parquet")
df_final.to_parquet(parquet_path, index=False)

print(f"Data saved to {parquet_path}")
