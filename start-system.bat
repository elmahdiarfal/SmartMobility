@echo off
echo ==========================================
echo SUMO Real-time Traffic Monitoring System
echo ==========================================
echo.

echo Checking Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not installed!
    exit /b 1
)

docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker Compose is not installed!
    exit /b 1
)

echo ✓ Docker and Docker Compose are installed
echo.

echo Stopping existing containers...
docker-compose down
echo ✓ Existing containers stopped
echo.

echo Starting Docker containers...
docker-compose up -d
echo ✓ Docker containers started
echo.

echo Waiting for services to initialize...
timeout /t 30 /nobreak >nul
echo.

echo ==========================================
echo          SERVICES ARE RUNNING
echo ==========================================
echo.
echo 📊 MONITORING DASHBOARDS
echo    • Grafana Dashboard:     http://localhost:3000
echo      - Username: admin
echo      - Password: admin
echo.
echo    • Kafka Web UI (Kafdrop): http://localhost:9000
echo.
echo    • PostgreSQL Web UI (pgAdmin): http://localhost:5050
echo      - Email: admin@sumo.com
echo      - Password: admin
echo.
echo 🔧 BACKEND SERVICES
echo    • PostgreSQL Database:   localhost:5432
echo    • Kafka Broker:          localhost:9092
echo    • Kafka (external):      localhost:29092
echo    • Zookeeper:             localhost:2181
echo.
echo 📝 DATABASE CREDENTIALS
echo    • Database: sumodb
echo    • Username: sumouser
echo    • Password: sumopass
echo.
echo ==========================================
echo.
echo ==========================================
echo           NEXT STEPS
echo ==========================================
echo.
echo 1. Open three separate Command Prompt windows
echo.
echo 2. In Command Prompt 1 - Start the Data Consumer/Storage:
echo    cd %cd%
echo    python consumer_storage.py
echo.
echo 3. In Command Prompt 2 - Start the SUMO Collector:
echo    cd %cd%
echo    python collector.py
echo.
echo 5. To stop everything:
echo    Press Ctrl+C in Command Prompts 1 & 2
echo    Then run: docker-compose down
echo.
echo ==========================================
echo.
echo ✓ System startup complete! Follow the next steps above.
echo.
pause