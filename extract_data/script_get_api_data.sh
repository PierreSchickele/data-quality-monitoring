#!/bin/bash

SCRIPT_PATH="python extract_data/get_api_data.py"
STORE_NAME="Lille"

# Loop over jan-2025
for day in {01..31}; do
    DATE="2025-01-$day"
    echo "Execution : $SCRIPT_PATH $DATE $STORE_NAME"
    $SCRIPT_PATH $DATE $STORE_NAME
done

echo "Extraction done for jan-2025"