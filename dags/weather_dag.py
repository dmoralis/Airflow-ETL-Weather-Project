from airflow import DAG
from datetime import timedelta, datetime
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.operators.python import PythonOperator
from io import StringIO
import json
import pandas as pd
import boto3


def kelvinToCelsius(kelvin):
    return kelvin - 273.15


def transform_load_data(task_instance):
    data = task_instance.xcom_pull(task_ids="extract_weather_data")
    city = data["name"]
    weather_description = data["weather"][0]['description']
    temp_c = kelvinToCelsius(data["main"]["temp"])
    feels_like_c = kelvinToCelsius(data["main"]["feels_like"])
    temp_min_c = kelvinToCelsius(data["main"]["temp_min"])
    temp_max_c = kelvinToCelsius(data["main"]["temp_max"])
    pressure = data["main"]["pressure"]
    humidity = data["main"]["humidity"]
    wind_speed = data["wind"]["speed"]
    time_of_record = datetime.utcfromtimestamp(data['dt'] + data['timezone'])
    sunrise_time = datetime.utcfromtimestamp(data['sys']['sunrise'] + data['timezone'])
    sunset_time = datetime.utcfromtimestamp(data['sys']['sunset'] + data['timezone'])    

    transformed_data=[{
        "City":city,
        "Description":weather_description,
        "Temperature_(C)":temp_c,
        "Feels_Like":feels_like_c,
        "Minimum_Temperature_(C)":temp_min_c,
        "Maximum_Temperature_(C)":temp_max_c,
        "Pressure":pressure,
        "Humidity":humidity,
        "Wind_Speed":wind_speed,
        "Time_of_Record":time_of_record.strftime('%d/%M/%Y %H%M'),
        "Sunrise_(LocalTime)":sunrise_time.strftime('%d/%M/%Y %H%M'),
        "Sunset_(LocalTime)":sunset_time.strftime('%d/%M/%Y %H%M')
    }]
    df_data = pd.DataFrame(transformed_data)
    aws_creds = {
        "key": "****6T",
        "secret": "****nMW",
        "token": "*******+A=="
    }
    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_creds['key'],
        aws_secret_access_key=aws_creds['secret'],
        aws_session_token=aws_creds['token']
    )

    now = datetime.now()
    dt_string = now.strftime("%d%m%Y%H:%M:%S")
    dt_string = 'current_weather_data_thessaloniki' + dt_string
    bucket_name = '*****les'
    
    csv_buffer = StringIO()
    file_name = f'{dt_string}.csv'
    df_data.to_csv(csv_buffer, index=False)
    s3.put_object(
        Bucket=bucket_name,
        Key=file_name,
        Body=csv_buffer.getvalue()
    )
    #df_data.to_csv(f"s3://airflowetlweathermorales/{dt_string}.csv", index=False, storage_options=aws_creds)


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

    
    is_weather_api_ready = HttpSensor(
        task_id="API_readiness_check_call",
        http_conn_id='weathermap_api',
        endpoint=f'/data/2.5/weather?lat=40.6403167&lon=22.9352716&appid=35d0d7526bceb84756b29a9ece8b28f3'
    )


    extract_weather_data = SimpleHttpOperator(
        task_id='extract_weather_data',
        http_conn_id='weathermap_api',
        endpoint=f'/data/2.5/weather?lat=40.6403167&lon=22.9352716&appid=35d0d7526bceb84756b29a9ece8b28f3',
        method='GET',
        response_filter=lambda r: json.loads(r.text),
        log_response=True
    )


    transform_load_data = PythonOperator(
        task_id='transform_load_weather_data',
        python_callable=transform_load_data
    )
    
    
    is_weather_api_ready >> extract_weather_data >> transform_load_data