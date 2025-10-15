FROM python:3.9-slim
WORKDIR /app
COPY pg_consumer.py .
RUN pip install kafka-python psycopg2-binary
CMD ["python", "pg_consumer.py"]
