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




#definir DAG
with DAG(
    'ej7',
    default_args=default_args,
    description = ' comprobar fichero hdfs',
    schedule_interval=timedelta(days=3),
    start_date=days_ago(1),
    tags=['example7'],
) as dag:
#creacion tareas
    commands = """
    if [ params.t1 -neq 0 ]; then
        hdfs dfs -put /root/Hadoop/solutions.txt hdfs://sandbox.bosonit.com:8020/root/tmp/adrian_moreno
    fi 
    """
    t1 = BashOperator(task_id='test', bash_command="hdfs dfs -test -e hdfs://sandbox.hortonworks.com:8020/root/tmp/adrian_moreno/solutions.txt")
    t2 = BashOperator(task_id='nonexist', bash_command=commands, params={'t1': t1})
    t3 = BashOperator(task_id='exist', bash_command="/usr/local/airflow/dags/exists.sh", params={'t1': t1})
    
    
    #especificar dependencias (órden)
    t1 >> [t2,t3]