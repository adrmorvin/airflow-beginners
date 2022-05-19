from datetime import timedelta

from airflow import DAG

#from airflow.operators.python import PythonOperator
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
    'retry_delay': timedelta(minutes=5),
}


#definir DAG
dag = DAG(
    'ej1',
    default_args=default_args,
    description = '2 tareas bash secuencial',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(2),
    tags=['exercise1'],
)
#creacion tareas
t1 = BashOperator(task_id="say-hello", bash_command='echo "hello world"', dag=dag)
t2 = BashOperator(task_id="print-date", bash_command='date', dag=dag)


    #especificar dependencias (órden)
t1 >> t2 