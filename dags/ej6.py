from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
import logging

#parametros por defecto
default_args ={
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retr_delay': timedelta(minutes=5),
}

def warning():
    logging.warning('error found')

def bosonit(x):
    return x + " te ayuda a obtener conocimientos sobre Airflow" 

#definir DAG
with DAG(
    'ej6',
    default_args=default_args,
    description = '2 tareas python paralelo + 1 bash',
    schedule_interval=timedelta(days=3),
    start_date=days_ago(1),
    tags=['example6'],
) as dag:
#creacion tareas
    t1 = PythonOperator(task_id="warning", python_callable=warning)
    t2 = PythonOperator(
    task_id='bosonit',
    python_callable= bosonit,
    op_kwargs = {"x" : "Bosonit"},
    dag=dag,
    )
    t3 = BashOperator(task_id='bash-task', bash_command="cat /usr/local/airflow/dags/command.sh")
    #especificar dependencias (órden)
    [t2, t1] >> t3