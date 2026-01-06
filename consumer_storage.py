import json
import sqlite3
import psycopg2
from kafka import KafkaConsumer
from datetime import datetime

class DataStorage:
    def __init__(self, storage_type='sqlite'):
        self.storage_type = storage_type
        self.setup_database()
    
    def setup_database(self):
        if self.storage_type == 'sqlite':
            # SQLite (Simplest option - no external dependencies)
            self.conn = sqlite3.connect('sumo_data.db')
            self.cursor = self.conn.cursor()
            self.create_table_sqlite()
        
        elif self.storage_type == 'postgres':
            # PostgreSQL (More scalable)
            self.conn = psycopg2.connect(
                host='localhost',
                database='sumodb',
                user='sumouser',
                password='sumopass',
                port=5432
            )
            self.cursor = self.conn.cursor()
            self.create_table_postgres()
        
        print(f"Connected to {self.storage_type} database")
    
    def create_table_sqlite(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS vehicle_telemetry (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                simulation_time REAL,
                vehicle_id TEXT,
                x REAL,
                y REAL,
                speed REAL,
                lane TEXT,
                edge TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        self.conn.commit()
    
    def create_table_postgres(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS vehicle_telemetry (
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
            )
        ''')
        self.conn.commit()
    
    def store_data(self, data):
        try:
            if self.storage_type == 'sqlite':
                self.cursor.execute('''
                    INSERT INTO vehicle_telemetry 
                    (simulation_time, vehicle_id, x, y, speed, lane, edge)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    data['time'],
                    data['veh_id'],
                    data['x'],
                    data['y'],
                    data['speed'],
                    data['lane'],
                    data['edge']
                ))
            else:  # postgres
                self.cursor.execute('''
                    INSERT INTO vehicle_telemetry 
                    (simulation_time, vehicle_id, x, y, speed, lane, edge)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                ''', (
                    data['time'],
                    data['veh_id'],
                    data['x'],
                    data['y'],
                    data['speed'],
                    data['lane'],
                    data['edge']
                ))
            
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error storing data: {e}")
            self.conn.rollback()
            return False
    
    def close(self):
        self.conn.close()

def run_consumer(storage_type='sqlite'):
    print("Starting Kafka Consumer with Storage...")
    
    # Initialize storage
    storage = DataStorage(storage_type)
    
    # Initialize Kafka Consumer
    consumer = KafkaConsumer(
        'vehTelemetry',
        bootstrap_servers=['localhost:29092'],
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        group_id='sumo-storage-group',
        value_deserializer=lambda x: json.loads(x.decode('utf-8'))
    )
    
    print("Waiting for messages...")
    message_count = 0
    
    try:
        for message in consumer:
            data = message.value
            print(f"Received: Time={data['time']}, Vehicle={data['veh_id']}")
            
            # Store in database
            if storage.store_data(data):
                message_count += 1
            
            # Simple progress indicator
            if message_count % 50 == 0:
                print(f"Stored {message_count} messages so far...")
                
    except KeyboardInterrupt:
        print("\nStopping consumer...")
    finally:
        consumer.close()
        storage.close()
        print(f"Total messages stored: {message_count}")

if __name__ == "__main__":
    # Choose storage type: 'sqlite' or 'postgres'
    run_consumer(storage_type='postgres')