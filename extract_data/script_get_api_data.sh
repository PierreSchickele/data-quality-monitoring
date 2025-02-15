#!/bin/bash

SCRIPT_PATH="python extract_data/get_api_data.py"
STORES=("Lille" "Marseille" "Toulouse")
YEARS=("2024")
MONTHS=("01" "02" "03" "04" "05" "06" "07" "08" "09" "10" "11" "12")
SENSORS=("")

for YEAR in "${YEARS[@]}"; do
    for MONTH in "${MONTHS[@]}"; do
        LAST_DAY=$(date -d "$YEAR-$MONTH-01 +1 month -1 day" +"%d")
        for DAY in $(seq -w 1 $LAST_DAY); do
            for STORE in "${STORES[@]}"; do
                DATE="$YEAR-$MONTH-$DAY"
                for SENSOR in "${SENSORS[@]}"; do
                    echo "Execution : $SCRIPT_PATH $DATE $STORE $SENSOR"
                    $SCRIPT_PATH $DATE $STORE $SENSOR
                done
            done
        done
    done
done