from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.apache.hive.operators.hive import HiveOperator
from airflow.operators.bash import BashOperator
from airflow.providers.apache.sqoop.operators.sqoop import SqoopOperator
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

#definir DAG
with DAG(
    'ej10',
    default_args=default_args,
    description = ' DAG 10 ',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(1),
    tags=['example10'],
) as dag:
#creacion tareas
    crea = SqoopOperator(conn_id='sqoop',
                                   table='food',
                                   username='root',
                                   password='123456',
                                   driver='jdbc:mysql://mysql.example.com/recipes',
                                   cmd_type='import')
    
    
    guarda = BashOperator(task_id="save",
    bash_command='hive -e "SELECT * FROM food WHERE category === "vegan" " > hdfs://sandbox.bosonit.com:8020/root/tmp/adrian_moreno/myfood.csv',
    dag=dag
    )
    #especificar dependencias (órden)
    crea >> guarda


