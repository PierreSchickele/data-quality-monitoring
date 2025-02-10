from read_raw_data import get_raw_data
import duckdb

# Load raw rata
df = get_raw_data()
df_cleaned = df[df['sensor_id'] == 'ALL']

print(df_cleaned.head())
print(df_cleaned.describe())

# Group by day
df_cleaned = (
    duckdb
    .sql(
        "SELECT date, store_name, sensor_id, SUM(visits_count)"
        "FROM df_cleaned "
        "GROUP BY date, store_name, sensor_id"
    )
    .df()
)
print(df_cleaned.head())
print(df_cleaned.describe())

# Remove rows with null values
df_cleaned = df.dropna()
print(df_cleaned.head())
print(df_cleaned.describe())

df_cleaned["day_of_week"] = df_cleaned["date"].dt.dayofweek
# print(df_cleaned.head())

# Average on the last 4 days
df_cleaned = (
    duckdb
    .sql(
        "SELECT date, store_name, sensor_id, visits_count, AVG(visits_count) "
        "OVER (PARTITION BY day_of_week, store_name, sensor_id "
        "ORDER BY date "
        "ROWS BETWEEN 3 PRECEDING AND CURRENT ROW "
        ") AS avg_visits_last_4_same_day "
        "FROM df_cleaned"
    )
    .df()
)

print(df_cleaned)
