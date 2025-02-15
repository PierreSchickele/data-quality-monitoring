import duckdb
import os
import glob
import pandas as pd

# Path to CSV files
RAW_DATA_PATH = "./data/raw"


def check_data_path(path):
    """Check if the data path exists."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Directory {path} does not exist.")
    print("Path exists")


def get_csv_files(path):
    """Retrieve all CSV files in the given directory."""
    csv_files = glob.glob(f"{path}/*.csv")
    if not csv_files:
        raise FileNotFoundError(f"No CSV files found in {path}.")
    print(f"CSV files found: {len(csv_files)} files")
    return csv_files


def load_data(csv_files):
    """Load CSV files using DuckDB and return a concatenated DataFrame."""
    con = duckdb.connect(database=":memory:")
    print("Connection OK")

    df_list = []
    for file in csv_files:
        print(f"Loading file: {file}")
        df = con.execute(f"SELECT * FROM read_csv_auto('{file}')").fetchdf()
        df_list.append(df)

    print("All files loaded, concatenating...")

    # Close the DuckDB connection
    con.close()
    print("Connection closed correctly")

    return pd.concat(df_list, ignore_index=True)


def get_raw_data():
    """Main function to get the raw data DataFrame."""
    check_data_path(RAW_DATA_PATH)
    csv_files = get_csv_files(RAW_DATA_PATH)
    return load_data(csv_files)


# Execute only if run as a script
if __name__ == "__main__":
    df_raw_data = get_raw_data()
    print("DataFrame created")
    print(df_raw_data)
