from airflow import DAG
from datetime import timedelta, datetime
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
import json


default_args = {
    'owner':'airflow',
    'depends_on_past':False,
    'start_date':datetime(2023, 9, 27),
    'email':[],
    'email_on_failure':False,
    'email_on_retry':False,
    'retries':0,
    'retry_delay':timedelta(minutes=2.0)
}


with DAG('weather_dag',
    default_args=default_args,
    schedule_interval='@daily',
    catchup=False) as dag:

    #lat = '40.6403167'
    #lon = '22.9352716'
    #api_key = '35d0d7526bceb84756b29a9ece8b28f3'
    
    is_weather_api_ready = HttpSensor(
        task_id="API_readiness_check_call",
        http_conn_id='weathermap_api',
        endpoint=f'/data/2.5/forecast?lat=40.6403167&lon=22.9352716&appid=35d0d7526bceb84756b29a9ece8b28f3'
    )

    extract_weather_data = SimpleHttpOperator(
        task_id='extract_weather_data',
        http_conn_id='weathermap_api',
        endpoint=f'/data/2.5/forecast?lat=40.6403167&lon=22.9352716&appid=35d0d7526bceb84756b29a9ece8b28f3',
        method='GET',
        response_filter=lambda r: json.loads(r.text),
        log_response=True
    )
    
    is_weather_api_ready >> extract_weather_data