from datetime import timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.apache.hive.operators.hive import HiveOperator
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

#definir DAG
with DAG(
    'ej8',
    default_args=default_args,
    description = ' DAG 8 ',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(1),
    tags=['example8'],
) as dag:
#creacion tareas
    crea = HiveOperator(
    hql = "hql/hive_create.hql",
    task_id = "create_hql_task",
    hive_cli_conn_id = "hive_local",
    dag = dag
    )
    carga = HiveOperator(
    hql = "hql/hive_load.hql",
    task_id = "load_hql_task",
    hive_cli_conn_id = "hive_local",
    dag = dag
    )
    guardar = BashOperator(task_id="save",
    bash_command='hive -e "SELECT * FROM players WHERE salary > 20000000" > hdfs://sandbox.bosonit.com:8020/root/tmp/adrian_moreno',
    dag=dag
    )
    #especificar dependencias (órden)
    crea >> carga >> guardar