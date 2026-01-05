# Smart Mobility 🚗💨

A real-time traffic simulation and big data pipeline system for urban mobility analysis using **SUMO**, **Apache Kafka**, and database/storage technologies.

---

## 📋 Project Overview

This project simulates urban traffic using **SUMO** (Simulation of Urban MObility), streams telemetry data through **Apache Kafka**, stores it in **SQLite** / **PostgreSQL** databases, and provides visualization and analysis tools. It's designed as a complete data pipeline for smart mobility research and data engineering demonstrations.

---

## 🏗️ Architecture

```
┌─────────────────┐   ┌─────────────┐   ┌─────────────────┐   ┌──────────────┐
│ SUMO Traffic    │──▶│ Apache      │──▶│ Database        │──▶│ Data         │
│ Simulation      │   │ Kafka       │   │ Storage         │   │ Analysis &   │
│ (collector.py)  │   │             │   │ (SQLite/Postgres)│  │ Viz Tools    │
└─────────────────┘   └─────────────┘   └─────────────────┘   └──────────────┘
```

---

## 📁 Project Structure

```
smart-mobility/
├── network.net.xml           # SUMO network definition (roads, junctions)
├── network.rou.xml           # Vehicle routes and types
├── network.settings.xml      # SUMO visualization settings
├── network.sumocfg           # SUMO configuration file
├── collector.py              # SUMO simulator & Kafka producer
├── consumer_storage.py       # Kafka consumer & database storage
├── analyze_stored_data.py    # Data analysis & visualization
├── requirements.txt          # Python dependencies
├── docker-compose.yml        # Kafka & Zookeeper services
├── docker-compose-db.yml     # PostgreSQL & PgAdmin services
└── README.md
```

---

## 🚀 Quick Start

### Prerequisites

* Python 3.8+
* SUMO installed (Windows example: `C:/Program Files (x86)/Eclipse/Sumo/`)
* Docker & Docker Compose
* Git

### Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/smart-mobility.git
cd smart-mobility
```

2. **Install Python dependencies**

```bash
pip install -r requirements.txt
```

3. **Start Kafka services**

```bash
docker-compose up -d
```

Verify Kafka web UI (Kafdrop) at `http://localhost:9000` (if configured).

---

## 🎯 Usage Guide

**Step 1: Start the Simulation Pipeline**

* Terminal 1 — Start the data consumer:

```bash
python consumer_storage.py
```

* Terminal 2 — Start the SUMO simulation (collector):

```bash
python collector.py
```

**Step 2: Analyze the Data**

Once simulation data is collected, run the analysis:

```bash
python analyze_stored_data.py
```

This will:

* Display statistical summaries
* Generate trajectory plots
* Create speed-over-time visualizations
* Export data to CSV format

**Step 3: Database Management**

Using SQLite (default):

* Data automatically stored in `sumo_data.db`
* Access with: `sqlite3 sumo_data.db`

Using PostgreSQL:

```bash
docker-compose -f docker-compose-db.yml up -d
```

* Access PgAdmin at `http://localhost:5050`
* Email: `admin@sumo.com`
* Password: `admin`

Update `consumer_storage.py` to use `storage_type='postgres'`.

---

## 🔧 Configuration

**Kafka Configuration**

* Bootstrap Server: `localhost:29092`
* Topic: `vehTelemetry`
* Kafdrop UI: `http://localhost:9000`

**SUMO Configuration**

* Binary Path (example): `C:/Program Files (x86)/Eclipse/Sumo/bin/sumo-gui`
* Max Simulation Steps: `1000`
* Update Interval: `0.05` seconds

**Vehicle Types Defined**

* `normal`: Standard vehicle (50 km/h max)
* `slow`: Slower vehicle (45 km/h max)
* `fast`: Faster vehicle (55 km/h max)

---

## 📊 Data Schema

```sql
CREATE TABLE vehicle_telemetry (
    id INTEGER PRIMARY KEY,
    timestamp DATETIME,
    simulation_time REAL,
    vehicle_id TEXT,
    x REAL,
    y REAL,
    speed REAL,
    lane TEXT,
    edge TEXT,
    created_at DATETIME
);
```

---

## 📈 Sample Analysis Output

The analysis script provides:

* **Basic Statistics:** Record counts, unique vehicles, speed metrics
* **Vehicle Trajectories:** Movement paths visualization
* **Speed Analysis:** Per-edge speed patterns
* **Time Series:** Speed changes over simulation time
* **Vehicle Classification:** Performance by vehicle type

---

## 🐳 Docker Services

**Kafka Cluster**

```bash
# Start all services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f kafka

# Stop services
docker-compose down
```

**Database Stack**

```bash
# Start PostgreSQL & PgAdmin
docker-compose -f docker-compose-db.yml up -d

# Access PgAdmin: http://localhost:5050
```

---

## 🧪 Testing the Pipeline

* Verify Kafka is receiving messages: check Kafdrop at `http://localhost:9000`
* Monitor consumer output for message counts
* Verify data storage:

  * SQLite: check `sumo_data.db` file size
  * PostgreSQL: query the `vehicle_telemetry` table
* Run validation analysis:

```bash
python analyze_stored_data.py
```

---

## 🔍 Troubleshooting

**Common Issues**

* **SUMO not found:**

  * Update `SUMO_TOOLS` path in `collector.py`
  * Ensure SUMO is installed correctly

* **Kafka connection errors:**

  * Check Docker containers are running: `docker-compose ps`
  * Verify port `29092` is available
  * Restart services: `docker-compose restart`

* **Database connection issues:**

  * SQLite: check file permissions
  * PostgreSQL: ensure Docker container is running

* **No data in analysis:**

  * Run simulation first (`collector.py`)
  * Ensure consumer is running (`consumer_storage.py`)
  * Check Kafka topic has messages

---

## 📚 Documentation

**Key Components**

* `collector.py` — SUMO simulation controller; Kafka producer for vehicle telemetry; real-time data streaming
* `consumer_storage.py` — Kafka consumer with configurable storage; supports SQLite and PostgreSQL; data validation and error handling
* `analyze_stored_data.py` — Statistical analysis and visualization; export capabilities; interactive data exploration

**Data Flow**

1. SUMO generates vehicle positions/speeds
2. Collector publishes to Kafka topic
3. Consumer stores in database
4. Analyzer processes and visualizes

---

## 🤝 Contributing

* Fork the repository
* Create a feature branch
* Commit your changes
* Push to the branch
* Open a Pull Request

---

## 📄 License

This project is licensed under the **MIT License** — see the `LICENSE` file for details.

---

## 🙏 Acknowledgments

* SUMO - Simulation of Urban MObility
* Apache Kafka - Distributed streaming platform
* Docker - Containerization platform
* Pandas - Data analysis library
* Matplotlib - Visualization library

---

## 📞 Support

For issues and questions:

* Check the Troubleshooting section
* Open a GitHub Issue and provide simulation logs and error messages

---

*Generated file: `SMART-MOBILITY.md`*
