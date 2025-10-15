import os
import json
from kafka import KafkaConsumer
from pymongo import MongoClient
from datetime import datetime
import time
from kafka.errors import NoBrokersAvailable

# Load environment variables
KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:29092")
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongodb:27017")
DB_NAME = os.getenv("MONGO_DB", "crypto")
COLLECTION = os.getenv("MONGO_COLLECTION", "trades_raw")

# Initialize Kafka consumer
while True:
    try:
        consumer = KafkaConsumer(
            "trades",
            bootstrap_servers=[KAFKA_BOOTSTRAP],
            auto_offset_reset="latest",
            group_id="mongo-consumer-group",
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        )
        break
    except NoBrokersAvailable:
        print("Kafka broker not available yet, retrying in 5 seconds...")
        time.sleep(5)

# Initialize MongoDB client
mongo = MongoClient(MONGO_URI)
collection = mongo[DB_NAME][COLLECTION]

print(f"Starting MongoDB consumer, writing to {DB_NAME}.{COLLECTION}")

for message in consumer:
    trade = message.value
    # Enrich timestamp field
    trade["received_at_iso"] = datetime.utcfromtimestamp(trade["received_at"] / 1000).isoformat()
    # Insert into MongoDB
    collection.insert_one(trade)
