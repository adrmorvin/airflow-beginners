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
    'padron',
    default_args=default_args,
    description = ' padronMadrid ',
    schedule_interval=timedelta(days=1),
    start_date=days_ago(1),
    tags=['Madrid'],
) as dag:
#creacion tareas
    crea = HiveOperator(
    hql = "hql/hive_createMadrid.hql",
    task_id = "create_hql_task",
    hive_cli_conn_id = "hive_local",
    dag = dag
    )
    ctas = HiveOperator(
    hql = "hql/ctas.hql",
    task_id = "ctas",
    hive_cli_conn_id = "hive_local",
    dag = dag
    )
    
    commands = """
    SELECT SUM(EspanolesHombres) AS Hespanoles, SUM(EspanolesMujeres) AS Mespanoles,
        SUM(ExtranjerosHombres) AS HExtranjeros, SUM(ExtranjerosMujeres) AS MExtranjeros,
        SUM(Hespanoles+HExtranjeros) AS Hombres, SUM(MExtranjeros+Mespanoles) AS Mujeres,
        SUM(Hombres+Mujeres) AS Personas
    
    FROM padron2
    GROUP BY DESC_DISTRITO
    """
    sql_job = SparkSqlOperator(sql=commands, master="local", task_id="sql_job")

    #especificar dependencias (órden)
    crea >> ctas >> sql_job
    