FROM apache/airflow:2.7.0

USER airflow

RUN pip install --upgrade pip
RUN pip install --user pymongo
RUN pip install --upgrade apache-airflow-providers-smtp
RUN pip install --upgrade apache-airflow-providers-openlineage>=1.8.0
