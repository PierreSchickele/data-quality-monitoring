#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from __future__ import annotations

import datetime

import pendulum

from airflow.models.dag import DAG
from airflow.operators.bash import BashOperator

with DAG(
    dag_id="extract_transform",
    schedule="30 * * * *",
    start_date=pendulum.datetime(2024, 1, 1, tz="UTC"),
    end_date=pendulum.datetime(2024, 12, 31, tz="UTC"),
    catchup=True,
    dagrun_timeout=datetime.timedelta(minutes=60),
    tags=["extract", "transform"],
    params={"example_key": "example_value"},
) as dag:
    extract_operator = BashOperator(
        task_id="extract_operator",
        bash_command="cd ~/data-quality-monitoring/ && python extract_data/get_api_data.py --execution_date '{{ ds }}' --execution_hour {{ execution_date.hour }}",
    )
    transform_operator = BashOperator(
        task_id="transform_operator",
        bash_command="cd ~/data-quality-monitoring/ && python transform_data/clean_data.py",
    )

    extract_operator >> transform_operator

if __name__ == "__main__":
    dag.test()
