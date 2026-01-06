# SUMO Real-time Traffic Monitoring System 🚦

A comprehensive traffic simulation and monitoring system that integrates **SUMO (Simulation of Urban MObility)** with modern data streaming and visualization tools. This project simulates vehicle traffic, collects telemetry data in real-time, streams it through **Kafka**, stores it in **PostgreSQL**, and visualizes it in **Grafana** dashboards.

---

## 📋 Table of Contents

* Requirements
* Project Structure
* Quick Start
* Architecture & Workflow
* Services Overview
* SUMO Configuration
* Docker Setup
* Kafka & Zookeeper
* Database Setup
* Grafana Dashboards
* File Descriptions
* Usage Instructions
* Troubleshooting
* Extensions & Customizations

---

## 🎯 Requirements

### System Requirements

* **OS:** Windows 10/11 (64-bit) or Linux/macOS
* **RAM:** Minimum 8GB (16GB recommended)
* **Storage:** 5GB free space
* **Processor:** x64 architecture

### Software Dependencies

| Software       | Version | Purpose                       |
| -------------- | ------- | ----------------------------- |
| Docker Desktop | 20.10+  | Container runtime             |
| Docker Compose | 2.0+    | Multi-container orchestration |
| Python         | 3.8+    | Data collection & processing  |
| Git            | 2.30+   | Version control               |
| SUMO           | 1.15.0+ | Traffic simulation            |

### Python Packages

All Python dependencies are listed in `requirements.txt`:

```
sumolib
traci
pandas
kafka-python
matplotlib
sqlite3
psycopg2-binary
requests
```

---

## 📁 Project Structure

```
SMARTMOBILITY1/
├── .venv/                          # Python virtual environment
├── grafana/
│   └── provisioning/
│       ├── dashboards/
│       │   ├── dashboard.yml       # Grafana dashboard provisioning
│       │   └── sumo-dashboard.json # Main dashboard definition
│       └── datasources/
│           └── datasources.yml     # PostgreSQL datasource config
├── docker-compose.yml              # Main Docker configuration
├── collector.py                    # SUMO data collector (Kafka producer)
├── consumer_storage.py             # Kafka consumer & database storage
├── network.net.xml                 # SUMO network definition
├── network.rou.xml                 # SUMO vehicle routes
├── network.settings.xml            # SUMO visualization settings
├── requirements.txt                # Python dependencies
├── start-system.bat                # Windows startup script
└── README.md                       # This file
```

---

## 🚀 Quick Start

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/sumo-traffic-monitoring.git
cd sumo-traffic-monitoring
```

### 2. Install Prerequisites

#### Windows Installation

* Install **Docker Desktop**

  * Download from Docker Desktop for Windows
  * Enable WSL 2 backend during installation
  * Start Docker Desktop after installation

* Install **Python 3.8+**

  * Download from python.org
  * Check **Add Python to PATH** during installation
  * Verify: `python --version`

* Install **SUMO**

  * Download from SUMO Download
  * Install to default location: `C:/Program Files (x86)/Eclipse/Sumo/`
  * Add SUMO to PATH environment variable

#### Linux/macOS Installation

```bash
# Install Docker & Docker Compose
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo apt-get install docker-compose

# Install Python dependencies
sudo apt-get install python3 python3-pip python3-venv

# Install SUMO (Ubuntu/Debian)
sudo add-apt-repository ppa:sumo/stable
sudo apt-get update
sudo apt-get install sumo sumo-tools sumo-doc
```

### 3. Set Up Python Environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# Linux/macOS
source .venv/bin/activate

pip install -r requirements.txt
```

### 4. Start the System

```bash
# Windows
start-system.bat

# Linux/macOS
docker-compose up -d
```

### 5. Run the Simulation

Open two terminals:

**Terminal 1 – Data Consumer**

```bash
python consumer_storage.py
```

**Terminal 2 – SUMO Collector**

```bash
python collector.py
```

---

## 🏗 Architecture & Workflow

```
┌─────────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   SUMO Traffic  │    │   Kafka     │    │ PostgreSQL  │    │   Grafana   │
│   Simulation    │────▶   Broker    │────▶  Database   │────▶  Dashboard  │
│   (collector.py)│    │             │    │             │    │             │
└─────────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

**Data Flow**

* SUMO Simulation → Generates vehicle telemetry (position, speed, lane)
* Kafka Producer (`collector.py`) → Streams data to topic `vehTelemetry`
* Kafka Consumer (`consumer_storage.py`) → Stores data in PostgreSQL
* Grafana → Queries PostgreSQL and displays real-time dashboards

---

## 🔧 Services Overview

| Service            | Port  | URL                                            | Credentials                                     |
| ------------------ | ----- | ---------------------------------------------- | ----------------------------------------------- |
| Grafana            | 3000  | [http://localhost:3000](http://localhost:3000) | admin / admin                                   |
| Kafka UI (Kafdrop) | 9000  | [http://localhost:9000](http://localhost:9000) | –                                               |
| pgAdmin            | 5050  | [http://localhost:5050](http://localhost:5050) | [admin@sumo.com](mailto:admin@sumo.com) / admin |
| PostgreSQL         | 5432  | localhost:5432                                 | sumouser / sumopass                             |
| Kafka Broker       | 9092  | localhost:9092                                 | –                                               |
| Kafka (External)   | 29092 | localhost:29092                                | –                                               |
| Zookeeper          | 2181  | localhost:2181                                 | –                                               |

---

## 🚦 SUMO Configuration

### Network Definition (`network.net.xml`)

* 6-junction traffic network
* Junction types: priority, right_before_left, internal
* 24 edges with specific lanes and connections
* Coordinate system for vehicle positioning

### Vehicle Routes (`network.rou.xml`)

* Vehicle types: `normal`, `slow`, `fast`
* Initial vehicles: `veh0`, `veh1`, `veh2`
* Random flow vehicles (20% probability)

### Simulation Settings (`network.settings.xml`)

* Viewport centered at (50, 75)
* 100% zoom
* 200ms delay between steps

---

## 🐳 Docker Setup

Services include **Zookeeper**, **Kafka**, **Kafdrop**, **PostgreSQL**, **pgAdmin**, and **Grafana**.

### Volumes

```yaml
volumes:
  postgres_data:
  grafana_data:
```

---

## 📊 Kafka & Zookeeper

* **Topic:** `vehTelemetry`
* **Format:** JSON vehicle telemetry
* **Partitions:** 1
* **Replication:** 1

Producer and consumer configurations are defined in `collector.py` and `consumer_storage.py`.

---

## 🗄 Database Setup

```sql
CREATE TABLE vehicle_telemetry (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT NOW(),
    simulation_time DOUBLE PRECISION,
    vehicle_id VARCHAR(50),
    x DOUBLE PRECISION,
    y DOUBLE PRECISION,
    speed DOUBLE PRECISION,
    lane VARCHAR(100),
    edge VARCHAR(100),
    created_at TIMESTAMP DEFAULT NOW()
);
```

---

## 📈 Grafana Dashboards

* Vehicle speed over time
* Vehicle count over time
* Per-vehicle speed tracking
* Real-time statistics with thresholds

Dashboards are auto-provisioned from `grafana/provisioning/`.

---

## 🛠 Usage Instructions

* Start Docker services
* Start consumer and collector scripts
* Access Grafana at [http://localhost:3000](http://localhost:3000)
* Monitor Kafka at [http://localhost:9000](http://localhost:9000)
* Manage DB at [http://localhost:5050](http://localhost:5050)

---

## 🔍 Troubleshooting

Common issues include Docker not running, port conflicts, SUMO path issues, Kafka initialization delays, and database startup delays. Check logs using:

```bash
docker-compose logs
```

---

## 🚀 Extensions & Customizations

* Add vehicle types
* Extend SUMO networks
* Collect additional metrics (CO₂, fuel, noise)
* Create new Grafana dashboards
* Scale Kafka cluster
* Add advanced analytics consumers

---

## 📚 Learning Resources

* SUMO Documentation
* TraCI Python API
* Apache Kafka Documentation
* Grafana Documentation
* Docker & Docker Compose Reference
