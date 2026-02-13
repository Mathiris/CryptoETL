from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

# Chemins basés sur ta structure Lydia
BASE_PATH = "/home/gianotti/Documents/CrytoETL"
DBT_PATH = f"{BASE_PATH}/dbt"

default_args = {
    'owner': 'gianotti',
    'depends_on_past': False,
    'email_on_failure': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'eth_daily_pipeline',
    default_args=default_args,
    description='ETL Extraction with python Transform on dbt',
    schedule_interval='@daily',
    start_date=datetime(2026, 2, 14),
    catchup=False,
) as dag:

    extract_load = BashOperator(
        task_id='python_extract',
        bash_command=f'cd {BASE_PATH} && uv run python scripts/extract.py'
    )

    dbt_run = BashOperator(
        task_id='dbt_transformations',
        bash_command=f'cd {DBT_PATH} && uv run dbt run --profiles-dir .'
    )

    dbt_test = BashOperator(
        task_id='dbt_test_quality',
        bash_command=f'cd {DBT_PATH} && uv run dbt test --profiles-dir .'
    )
    
    extract_load >> dbt_run >> dbt_test