import os
import asyncio
import ujson
import websockets
from kafka import KafkaProducer
from dotenv import load_dotenv

# Load config from .env
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../config/.env'))

BINANCE_WS_URL = os.getenv('BINANCE_WS_URL', 'wss://stream.binance.com:9443/ws/btcusdt@trade')
KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:29092')
KAFKA_TOPIC_TRADES = os.getenv('KAFKA_TOPIC_TRADES', 'trades')

print(f'Kafka bootstrap servers from env: {os.getenv("KAFKA_BOOTSTRAP_SERVERS")}')

producer = KafkaProducer(
    bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS.split(','),
    value_serializer=lambda v: ujson.dumps(v).encode('utf-8'),
    linger_ms=0
)

async def consume_trades():
    async for websocket in websockets.connect(BINANCE_WS_URL):
        try:
            async for message in websocket:
                trade_event = ujson.loads(message)
                trade_event['received_at'] = asyncio.get_event_loop().time()
                producer.send(KAFKA_TOPIC_TRADES, trade_event)
                producer.flush()
        except websockets.ConnectionClosed:
            print('WebSocket connection closed, retrying...')
            continue

if __name__ == '__main__':
    print(f'Starting trade ingestion from {BINANCE_WS_URL} to Kafka topic "{KAFKA_TOPIC_TRADES}"...')
    asyncio.run(consume_trades())
