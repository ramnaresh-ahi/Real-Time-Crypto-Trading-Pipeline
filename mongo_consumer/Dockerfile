FROM python:3.9-slim
WORKDIR /app
COPY mongo_consumer.py .
RUN pip install kafka-python pymongo
CMD ["python", "mongo_consumer.py"]
