#!/bin/bash

SCRIPT_PATH="python extract_data/get_api_data.py"
YEARS=("2024")
MONTHS=("01" "02" "03" "04" "05" "06" "07" "08" "09" "10" "11" "12")

for YEAR in "${YEARS[@]}"; do
    for MONTH in "${MONTHS[@]}"; do
        echo "Treatement : $YEAR-$MONTH..."
        for DAY in $(seq -w 1 31); do
            DATE="$YEAR-$MONTH-$DAY"
            $SCRIPT_PATH --execution_date $DATE
        done
    done
done
