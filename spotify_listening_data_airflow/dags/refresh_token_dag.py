from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import sys
sys.path.insert(1,"/opt/airflow/code")
from src import refresh_access_token

with DAG(
    dag_id="refresh_token",
    start_date=datetime(2022,11,20),
    schedule_interval="*/50 * * * *",
    catchup=False
   
) as dag:
    refresh_token_task=PythonOperator(
        task_id="refresh_token_task",
        python_callable=refresh_access_token.do_refresh_access_token,
        do_xcom_push=False
    )
    refresh_token_task