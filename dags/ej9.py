from datetime import timedelta
from airflow import DAG
from airflow.providers.apache.pig.operators.pig import PigOperator
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago


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
    'ej9',
    default_args=default_args,
    description = 'pig',
    schedule_interval=timedelta(days=2),
    start_date=days_ago(2),
    tags=['exercise9'],
)


pig = PigOperator(
    task_id="pig",
    pig="dfs -copyFromLocal ~/data/datacovid.csv /user/covid;",
    pig_opts="-x local",
    dag=dag,
)
commands = """
hive -e create external table if not exists covid19 (country string, date string, total_cases int, total_deaths int, total_vaccinations int)
    comment 'the importance of vaccination'
    row format delimited
    fields terminated by ','
    stored as textfile
    location '/user/covid';
"""

external = BashOperator(task_id="table",
bash_command= commands,
dag=dag
)

guardar = BashOperator(task_id="save",
bash_command='hive -e "SELECT * FROM covid19 GROUPBY country" > hdfs://sandbox.bosonit.com:8020/root/tmp/adrian_moreno/covid19.csv',
dag=dag
)
pig >> external >> guardar
    