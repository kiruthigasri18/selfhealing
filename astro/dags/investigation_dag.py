from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

import os
import sys

sys.path.append(os.path.dirname(__file__))

from investigation_task import investigate

with DAG(
        dag_id="investigation_dag",
        start_date=datetime(2025,1,1),
        catchup=False,
        schedule=None,
        tags=["llm"]
) as dag:

    investigation = PythonOperator(
        task_id="investigation_task",
        python_callable=investigate
    )