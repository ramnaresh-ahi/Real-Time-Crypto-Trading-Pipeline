import os
import json
import psycopg2
from kafka import KafkaConsumer
from datetime import datetime
import time
from kafka.errors import NoBrokersAvailable

# Load environment variables
KAFKA_BOOTSTRAP = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "localhost:29092")
PG_CONN = os.getenv("POSTGRES_CONN", "dbname=airflow user=airflow password=airflow host=postgres port=5432")
GROUP_ID = "pg-consumer-group"

# Initialize Kafka consumer
while True:
    try:
        consumer = KafkaConsumer(
            "trades",
            bootstrap_servers=[KAFKA_BOOTSTRAP],
            auto_offset_reset="latest",
            group_id=GROUP_ID,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        )
        break
    except NoBrokersAvailable:
        print("Kafka broker not available, retrying in 5 seconds...")
        time.sleep(5)

# Initialize Postgres connection
conn = psycopg2.connect(PG_CONN)
cursor = conn.cursor()

print("Starting PostgreSQL consumer, writing to trades_agg table")

# Ensure table exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS trades_agg (
    symbol TEXT,
    window_start TIMESTAMP,
    vwap NUMERIC,
    volume NUMERIC,
    trade_count INTEGER,
    PRIMARY KEY (symbol, window_start)
)
""")
conn.commit()

# Rolling window state
window_size_sec = 60
state = {}  # {symbol: [(price*qty, qty, timestamp), ...]}

for msg in consumer:
    trade = msg.value
    symbol = trade["s"]
    price = float(trade["p"])
    qty = float(trade["q"])
    ts = datetime.fromtimestamp(trade["T"] / 1000)

    # Initialize state
    if symbol not in state:
        state[symbol] = []

    # Append and prune old records
    state[symbol].append((price * qty, qty, ts))
    cutoff = ts.timestamp() - window_size_sec
    state[symbol] = [(pv, q, t) for (pv, q, t) in state[symbol] if t.timestamp() >= cutoff]

    # Compute VWAP and total volume
    total_pv = sum(pv for pv, q, t in state[symbol])
    total_qty = sum(q for pv, q, t in state[symbol])
    vwap = total_pv / total_qty if total_qty else 0

    # Upsert into Postgres
    window_start = datetime.fromtimestamp(cutoff)
    cursor.execute("""
    INSERT INTO trades_agg (symbol, window_start, vwap, volume, trade_count)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (symbol, window_start) DO UPDATE
    SET vwap = EXCLUDED.vwap,
        volume = EXCLUDED.volume,
        trade_count = EXCLUDED.trade_count
    """, (symbol, window_start, vwap, total_qty, len(state[symbol])))
    conn.commit()
