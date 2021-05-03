from datetime import timedelta
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import sys

sys.path.insert(0,"/Users/gajdulj/Dev/data_engineering/dags/scripts")
import scripts.check_follow_changes as script

default_args = {
    'owner': 'airflow',
    'start_date': days_ago(0,0,0,0,0),
    'email': ['example@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

twitter_kwargs = {
    "user_to_check":'elonmusk',
    "output_path":'/Users/gajdulj/Dev/data_engineering/data_store/'
}

dag = DAG(
    'test_dag',
    default_args=default_args,
    description='Our first DAG with ETL process!',
    schedule_interval=timedelta(days=1),
)

def example_function(**kwargs):
    username=kwargs['user_to_check'], 
    output_path=kwargs['output_path']
    print(username, output_path)
    print("Function that ran inside of DAG (python callable)")

run_etl = PythonOperator(
    task_id='reconcile_friends',
    python_callable=script.check_follow_changes,
    dag=dag,
    op_kwargs=twitter_kwargs
)

run_etl
