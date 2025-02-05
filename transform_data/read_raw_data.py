import duckdb
import os
import glob
import pandas as pd

# Path to CSV files
RAW_DATA_PATH = "./data/raw"

# Check if path exists
if not os.path.exists(RAW_DATA_PATH):
    raise FileNotFoundError(f"Directory {RAW_DATA_PATH} does not exist.")

print("Path exists")

# Read all CSV files in the repository
csv_files = glob.glob(f"{RAW_DATA_PATH}/*.csv")

print(f"CSV files found: {len(csv_files)} files")

if not csv_files:
    raise FileNotFoundError(f"No CSV files found in {RAW_DATA_PATH}.")

# Create DuckDB connection in memory
con = duckdb.connect(database=":memory:")

print("Connection OK")

# Load CSV files in chunks and concatenate
df_list = []
for file in csv_files:
    print(f"Loading file: {file}")
    df = con.execute(f"SELECT * FROM read_csv_auto('{file}')").fetchdf()
    df_list.append(df)

print("All files loaded, concatenating...")

# Concatenate all data
df_final = pd.concat(df_list, ignore_index=True)

print("Final DataFrame created")

# Print DataFrame
print(df_final)

# Close the DuckDB connection
con.close()

print("Connection closed correctly")
