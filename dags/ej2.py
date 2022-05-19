from datetime import timedelta

from airflow import DAG

from airflow.operators.python import PythonOperator
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

def welcome():
    print("Bienvenido !")



#definir DAG
with DAG(
    'ej2',
    default_args=default_args,
    description = '2 tareas python secuencial',
    schedule_interval=timedelta(days=3),
    start_date=days_ago(1),
    tags=['example2'],
) as dag:
#creacion tareas
    t1 = PythonOperator(task_id="warning", python_callable=warning)
    t2 = PythonOperator(task_id="welcome", python_callable=welcome)
    
    #especificar dependencias (órden)
    t1 >> t2 