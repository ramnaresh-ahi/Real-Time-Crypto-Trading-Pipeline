from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from pymongo import MongoClient
import psycopg2
import logging

# Email configuration for alerts
DEFAULT_EMAIL = "your_email_address: example@gmail.com"

default_args = {
    'owner': 'crypto-pipeline',
    'depends_on_past': False,
    'start_date': datetime(2025, 10, 13),
    'email': [DEFAULT_EMAIL],
    'email_on_failure': True,
    'email_on_retry': False
}

dag = DAG(
    'crypto_data_quality_check',
    default_args=default_args,
    description='Check data freshness in MongoDB and PostgreSQL',
    schedule_interval=None, #set '@hourly' to get hourly notifications when dag fails.
    catchup=False,
    max_active_runs=1
)

def check_mongo_data():
    client = MongoClient('mongodb://mongodb:27017')
    db = client.crypto
    collection = db.trades_raw
    
    # Check count of trades in last 2 hours
    two_hours_ago = datetime.utcnow() - timedelta(hours=2)
    # Convert one_hour_ago to epoch ms for Mongo query on 'T' field (assumed stored as epoch ms)
    two_hours_ago_ms = int(two_hours_ago.timestamp() * 1000)
    # Query documents with 'T' (event timestamp in epoch ms) within the last 2 hours
    recent_count = collection.count_documents({
        'T': {'$gte': two_hours_ago_ms}
    })
    
    logging.info(f"MongoDB recent trades count in last 2 hours: {recent_count}")
    
    if recent_count == 0:
        raise ValueError("No recent trades found in MongoDB in the last 2 hours!")

def check_postgres_data():
    conn = psycopg2.connect(
        host='postgres',
        database='airflow',
        user='airflow',
        password='airflow'
    )
    cur = conn.cursor()
    
    # Check count of aggregated trades in last 2 hours
    cur.execute(
        "SELECT COUNT(*) FROM trades_agg WHERE window_start >= NOW() - INTERVAL '2 hour'"
    )
    count = cur.fetchone()[0]
    
    logging.info(f"Postgres aggregated trades in last 2 hours: {count}")
    
    if count == 0:
        raise ValueError("No recent trades found in Postgres aggregation in the last 2 hours!")
    
    cur.close()
    conn.close()

mongo_check = PythonOperator(
    task_id='check_mongo_data_quality',
    python_callable=check_mongo_data,
    dag=dag
)

postgres_check = PythonOperator(
    task_id='check_postgres_data_quality',
    python_callable=check_postgres_data,
    dag=dag
)

# Optional email alert task if you want to add custom email notifications manually
alert_task = EmailOperator(
    task_id="send_failure_alert",
    to=DEFAULT_EMAIL,
    subject="Crypto Pipeline Data Quality Check Failed",
    html_content="One or more data quality checks failed in your crypto pipeline DAG.",
    trigger_rule='one_failed',
    dag=dag
)

mongo_check >> postgres_check >> alert_task
