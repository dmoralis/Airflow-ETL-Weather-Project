from airflow import DAG
from datetime import timedelta, datetime
from airflow.providers.http.sensors.http import HttpSensor
import json


default_args = {
    'owner':'airflow',
    'depends_on_past':False,
    'start_date':datetime(2023, 9, 26),
    'email':[],
    'email_on_failure':False,
    'email_on_retry':False,
    'retries':1,
    'retry_delay':timedelta(minutes=2.0)
}


with DAG('weather_dag',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False) as dag:

    lat = '40.6403167'
    lon = '22.9352716'
    api_key = '800bbfb2f56e6861f7f1ae1bebce4528'
    is_weather_api_ready = HttpSensor(
        task_id="API_readiness_check_call",
        http_conn_id='weathermap_api',
        endpoint='/data/3.0/onecall?lat={lat}&lon={lon}&appid={api_key}'
    )
    