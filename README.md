# Real-Time Crypto Trading Pipeline

> **⚠️ Project Status: Incomplete - On Hold**
> 
> This project is currently incomplete and has been paused due to time constraints and complexity. I plan to resume and complete it in the future when time permits. The current implementation demonstrates a working foundation for real-time data streaming and processing.

## 📋 Project Overview

A comprehensive real-time data engineering pipeline designed to ingest, process, and analyze cryptocurrency trading data using modern streaming technologies. The project demonstrates end-to-end data engineering principles including real-time streaming, data quality monitoring, and workflow orchestration.

## 🎯 Project Goal

Build a production-grade, scalable real-time data pipeline that:
- Ingests live cryptocurrency trade data via streaming APIs
- Processes and transforms data in real-time using Apache Kafka
- Stores raw trades in MongoDB for flexibility
- Aggregates and stores analytical data in PostgreSQL
- Orchestrates workflows and data quality checks using Apache Airflow
- Provides monitoring and visualization capabilities

## 🏗️ Architecture

```
[Binance WebSocket API] 
        ↓
    [Producer]
        ↓
   [Apache Kafka]
        ↓
    ┌───────┴───────┐
    ↓               ↓
[MongoDB Consumer] [Postgres Consumer]
    ↓               ↓
[MongoDB]       [PostgreSQL]
    ↓               ↓
[Apache Airflow DAGs - Data Quality & Orchestration]
```

## 🛠️ Technology Stack

### Core Technologies
- **Apache Kafka** (v7.4.0) - Message broker for real-time streaming
- **Apache Zookeeper** (v7.4.0) - Kafka coordination service
- **MongoDB** (v6.0) - NoSQL database for raw trade storage
- **PostgreSQL** (v13) - Relational database for aggregated analytics
- **Apache Airflow** (v2.7.0) - Workflow orchestration and scheduling
- **Docker & Docker Compose** - Containerization and service orchestration

### Python Libraries
- `kafka-python` - Kafka client
- `pymongo` - MongoDB driver
- `psycopg2-binary` - PostgreSQL adapter
- `websockets` - WebSocket client for real-time data
- `python-dotenv` - Environment configuration
- `streamlit` & `plotly` - Dashboard and visualization (planned)

## 📁 Project Structure

```
Real-Time-Crypto-Trading-Pipeline/
├── airflow/                    # Airflow configuration and metadata
│   ├── postgres_data/         # Airflow metadata database
│   ├── airflow.cfg            # Airflow configuration
│   └── webserver_config.py    # Webserver settings
├── config/                    # Configuration files
│   ├── .env                   # Environment variables
│   └── json_schemas/          # Data validation schemas
├── dags/                      # Airflow DAG definitions
│   └── data_quality_dag.py    # Data quality monitoring DAG
├── dashboard/                 # Monitoring dashboard (planned)
│   └── dashboard.py
├── mongo_consumer/            # MongoDB Kafka consumer
│   ├── Dockerfile
│   └── mongo_consumer.py
├── pg_consumer/               # PostgreSQL Kafka consumer
│   ├── Dockerfile
│   └── pg_consumer.py
├── producer/                  # Kafka message producer
│   ├── Dockerfile
│   └── producer.py
├── scripts/                   # Utility scripts
│   └── init_mongo.sh          # MongoDB initialization
├── tests/                     # Test suites
│   ├── test_mongo_loader.py
│   ├── test_producer.py
│   └── test_transformer.py
├── transformer/               # Data transformation logic
│   ├── Dockerfile
│   └── transformer.py
├── validation/                # Schema validation
│   └── trade_event.json       # Trade event JSON schema
├── docker-compose.yml         # Docker services configuration
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation
```

## ✅ What Has Been Completed

### 1. Infrastructure Setup
- [✔] Docker Compose configuration for all services
- [✔] Custom Docker network (`rt-crypto-net`) for inter-container communication
- [✔] Service dependencies and health checks configured

### 2. Data Ingestion Layer
- [✔] Kafka broker and Zookeeper setup
- [✔] Kafka UI for monitoring (accessible at `localhost:8081`)
- [✔] Producer implementation for streaming trade data
- [✔] WebSocket integration for real-time data ingestion

### 3. Data Processing Layer
- [✔] MongoDB consumer implementation
  - Successfully consuming messages from Kafka topics
  - Storing raw trades in `trades_raw` collection
  - Minimal consumer lag achieved
- [✔] PostgreSQL consumer implementation
  - Consuming and aggregating trade data
  - Storing aggregated metrics in `trades_agg` table
  - Working with minimal lag

### 4. Storage Layer
- [✔] MongoDB replica set configuration
- [✔] PostgreSQL database setup with Airflow integration
- [✔] Database connection strings and environment variables configured

### 5. Orchestration Layer (Partial)
- [✔] Airflow scheduler setup
- [✔] Basic data quality DAG created
- [✔] DAG file structure and imports configured
- [✔] Requirements.txt with all necessary dependencies
- [✔] Webserver fully operational
- [✔] Complete DAG implementation with real data quality checks
- [✔] Email notifications and alerting configured
- [✔] Scheduled batch processing jobs


### 6. Monitoring
- [✔] Kafka UI for consumer lag monitoring
- [✔] Docker container health monitoring
- [✔] Consumer group metrics tracking

## 🚧 Known Issues & Incomplete Work

### Issues Encountered

1. **Airflow Webserver Timeout**
   - Gunicorn master not responding within 120 seconds
   - Webserver container exits after timeout
   - Scheduler runs successfully but webserver fails to start completely

2. **Python Dependencies in Airflow**
   - `pymongo` and `psycopg2-binary` installation challenges in Airflow containers
   - Requirements.txt mounting and installation timing issues

3. **Resource Constraints**
   - Worker timeout errors in Airflow scheduler
   - Potential memory exhaustion (SIGKILL signals observed)

### Incomplete Components

1.. **Data Quality & Validation**
   - [ ] JSON schema validation in producer/consumers
   - [ ] Data quality checks integrated into DAGs
   - [ ] Monitoring for duplicates and schema drift
   - [ ] Automated data quality tests

2. **Monitoring & Visualization**
   - [ ] Dashboard implementation with Streamlit
   - [ ] Prometheus/Grafana integration for metrics
   - [ ] Custom alerting system
   - [ ] Performance monitoring dashboards

3. **Testing**
   - [ ] Comprehensive unit tests for all components
   - [ ] Integration tests for end-to-end flow
   - [ ] Contract tests for schema conformance
   - [ ] CI/CD pipeline setup

4. **Documentation**
   - [ ] Setup instructions and prerequisites
   - [ ] Troubleshooting guide
   - [ ] Architecture diagrams
   - [ ] API documentation

5. **Security**
   - [ ] Authentication on MongoDB and Kafka
   - [ ] Encryption for data in transit
   - [ ] Secrets management
   - [ ] Access control lists

## 🚀 Quick Start (Current State)

### Prerequisites
- Docker Desktop installed and running
- At least 8GB RAM available
- Ports available: 8080, 8081, 9092, 27017, 5432

### Running the Pipeline

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd Real-Time-Crypto-Trading-Pipeline
   ```

2. **Create virtual environment & activate it**
   ```bash
   python -m venv myvenv
   ```

   ```bash
   myvenv\Scripts\activate
   ```

3. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Start services**
   ```bash
   docker-compose up -d
   ```

5. **Verify running services**
   ```bash
   docker ps
   ```

6. **Run kafka producer**
   ```bash
   python producer/producer.py
   ```

7. **Access Kafka UI & airflow**
   - Open browser: `http://localhost:8081`
   - Monitor consumer groups and message flow

   - Open browser: `http://localhost:8080`
   - Monitor crypto_data_quality_check dag

8. **Check consumer logs**
   ```bash
   docker logs mongo-consumer -f
   docker logs pg-consumer -f
   ```

### Stopping the Pipeline

```bash
docker-compose down
```

To remove volumes and clean up completely:
```bash
docker-compose down -v
```

## 📊 Current Data Flow

1. **Producer** → Generates/streams trade messages to Kafka topic
2. **Kafka** → Distributes messages to consumer groups
3. **MongoDB Consumer** → Reads from Kafka, stores raw trades in MongoDB
4. **Postgres Consumer** → Reads from Kafka, aggregates and stores in PostgreSQL
5. **Kafka UI** → Monitors consumer lag and message throughput
6. **Airflow UI** → Monitor crypto_data_quality_check dag

### Verified Working
- ✅ Producer successfully producing messages
- ✅ Consumers successfully consuming with minimal lag (typically <100 messages)
- ✅ Data flowing into both MongoDB and PostgreSQL
- ✅ Consumer groups stable and healthy
- ✅ Network connectivity between all containers

## 🔧 Configuration

### Environment Variables

Key configurations in `config/.env`, `airflow/airflow.cfg` and `docker-compose.yml`:

```yaml
# Kafka
KAFKA_BOOTSTRAP_SERVERS=kafka:9092

# MongoDB
MONGO_URI=mongodb://mongodb:27017
MONGO_DB=crypto
MONGO_COLLECTION=trades_raw

# PostgreSQL
POSTGRES_CONN=host=postgres port=5432 dbname=airflow user=airflow password=airflow

# Airflow
AIRFLOW__CORE__EXECUTOR=LocalExecutor
AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow
```

## 📝 Lessons Learned

1. **Docker Networking**: Custom bridge networks enable reliable DNS-based service discovery
2. **Consumer Lag Management**: Proper Kafka partitioning and consumer group configuration is critical
3. **Resource Management**: Airflow requires careful tuning of worker timeouts and memory limits
4. **Dependency Management**: Installing Python packages in Docker requires proper requirements file mounting and build steps
5. **Modular Architecture**: Separation of concerns across folders aids maintainability and debugging

## 🎯 Future Roadmap (When Resuming)

### Phase 1: Data Transformation
- Handle missing values
- Data types
- Naming convention

### Phase 2: Data Quality
- Implement schema validation
- Add data quality tests in DAGs
- Set up monitoring and alerts

### Phase 3: Visualization
- Complete dashboard implementation
- Add real-time metrics visualization
- Integrate Grafana for monitoring

### Phase 4: Testing & CI/CD
- Write comprehensive test suites
- Set up GitHub Actions for CI/CD
- Add automated deployment

### Phase 5: Production Hardening
- Add security layers (auth, encryption)
- Implement backup and disaster recovery
- Performance optimization and scaling

## 🤝 Contributing

This project is currently on hold and not accepting contributions. However, feel free to fork and experiment with the codebase for learning purposes.

## 📜 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👤 Author

**Your Name**
- GitHub: [@ramnaresh-ahi](https://github.com/ramnaresh-ahi)
- LinkedIn: [Ramnaresh Ahirwar](https://www.linkedin.com/in/ramnaresh-ahirwar-77abc/)

## 🙏 Acknowledgments

- Binance API for providing real-time cryptocurrency data
- Apache Kafka, MongoDB, PostgreSQL, and Airflow communities
- Docker and containerization ecosystem

---

## 📌 Why This Project is On Hold

This project has been temporarily paused due to:

1. **Time Constraints**: The project requires significant time investment for debugging, testing, and completing remaining features
2. **Complexity**: Real-time data engineering with multiple technologies requires careful orchestration and troubleshooting
3. **Resource Requirements**: Running all services simultaneously demands substantial local system resources
4. **Learning Curve**: Some technical challenges (especially Airflow configuration) require deeper investigation

**I will continue this project in the future** when I have more dedicated time to properly complete the implementation, testing, and documentation.

### Current Status Summary
- ✅ Core streaming pipeline working (Producer → Kafka → Consumers → Databases)
- ✅ Airflow orchestration working (crypto_data_quality_check dag, email alert)
- ❌ Monitoring, testing, and security features incomplete

Despite being incomplete, this project demonstrates:
- Real-time data streaming architecture
- Microservices design with Docker
- Kafka consumer implementation
- Database integration (NoSQL and SQL)
- Modern data engineering practices

Thank you for your interest in this project! Stars ⭐ and feedback are appreciated.

---

*Last Updated: October 16, 2025*
