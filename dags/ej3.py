from datetime import timedelta

from airflow import DAG

#from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago

#import logging
import os
import sys
#parametros por defecto
default_args ={
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
}

#definir DAG
dag = DAG(
    'ej3',
    default_args=default_args,
    description = '2 tareas java secuencial',
    schedule_interval='1 * 3 * *',
    start_date=days_ago(2),
    tags=['exercise3'],
)
#creacion tareas
t1 = BashOperator(
  task_id = 'usgs_fetch'
  , dag = dag
  , bash_command = 'java -cp /mnt/c/Users/img/Documents/GitHub/backbone/target/kafkaUSGS-1.0-SNAPSHOT.jar KafkaUSGS'

)
t2 = BashOperator(
  task_id = 'usgs_fetch2'
  , dag = dag
  , bash_command = 'java -cp /mnt/c/Users/img/Documents/GitHub/backbone/target/kafkaUSGS-1.2-SNAPSHOT.jar KafkaUSGS'

)

    #especificar dependencias (órden)
t1 >> t2 