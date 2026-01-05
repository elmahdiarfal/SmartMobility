import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

class DataAnalyzer:
    def __init__(self, db_name='sumo_data.db'):
        self.conn = sqlite3.connect(db_name)
        self.table_name = 'vehicle_telemetry'  # Changed from vehicle_data
        print(f"Connected to database: {db_name}")
        print(f"Using table: {self.table_name}")
    
    def basic_statistics(self):
        """Show basic statistics about the stored data"""
        query = f"""
        SELECT 
            COUNT(*) as total_records,
            COUNT(DISTINCT vehicle_id) as unique_vehicles,
            MIN(simulation_time) as first_timestamp,
            MAX(simulation_time) as last_timestamp,
            AVG(speed) as avg_speed,
            MIN(speed) as min_speed,
            MAX(speed) as max_speed
        FROM {self.table_name}
        """
        
        df = pd.read_sql_query(query, self.conn)
        return df
    
    def vehicle_trajectories(self, vehicle_id=None):
        """Get trajectory of a specific vehicle or all vehicles"""
        if vehicle_id:
            query = f"""
            SELECT simulation_time, x, y, speed, lane, edge
            FROM {self.table_name}
            WHERE vehicle_id = '{vehicle_id}'
            ORDER BY simulation_time
            """
        else:
            query = f"""
            SELECT vehicle_id, COUNT(*) as data_points,
                   MIN(simulation_time) as first_seen,
                   MAX(simulation_time) as last_seen
            FROM {self.table_name}
            GROUP BY vehicle_id
            ORDER BY data_points DESC
            """
        
        return pd.read_sql_query(query, self.conn)
    
    def speed_analysis(self):
        """Analyze speed patterns"""
        query = f"""
        SELECT 
            edge,
            AVG(speed) as avg_speed,
            COUNT(*) as observations
        FROM {self.table_name}
        GROUP BY edge
        ORDER BY avg_speed DESC
        """
        
        return pd.read_sql_query(query, self.conn)
    
    def plot_trajectories(self, vehicle_ids=None):
        """Visualize vehicle trajectories"""
        if not vehicle_ids:
            # Get top 5 vehicles with most data points
            query = f"""
            SELECT vehicle_id
            FROM {self.table_name}
            GROUP BY vehicle_id
            ORDER BY COUNT(*) DESC
            LIMIT 5
            """
            vehicle_ids = pd.read_sql_query(query, self.conn)['vehicle_id'].tolist()
        
        plt.figure(figsize=(12, 8))
        
        for vid in vehicle_ids:
            query = f"""
            SELECT x, y, simulation_time
            FROM {self.table_name}
            WHERE vehicle_id = '{vid}'
            ORDER BY simulation_time
            """
            df = pd.read_sql_query(query, self.conn)
            
            if not df.empty:
                plt.plot(df['x'], df['y'], marker='.', linestyle='-', markersize=3, 
                        label=f'Vehicle {vid} ({len(df)} points)')
        
        plt.xlabel('X Position')
        plt.ylabel('Y Position')
        plt.title('Vehicle Trajectories - SUMO Traffic Simulation')
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('sumo_trajectories.png', dpi=150)
        plt.show()
    
    def speed_over_time(self, vehicle_id=None):
        """Plot speed over time for vehicles"""
        if vehicle_id:
            query = f"""
            SELECT simulation_time, speed
            FROM {self.table_name}
            WHERE vehicle_id = '{vehicle_id}'
            ORDER BY simulation_time
            """
            title = f'Speed over Time - Vehicle {vehicle_id}'
            filename = f'speed_over_time_vehicle_{vehicle_id}.png'
        else:
            query = f"""
            SELECT simulation_time, AVG(speed) as avg_speed
            FROM {self.table_name}
            GROUP BY simulation_time
            ORDER BY simulation_time
            """
            title = 'Average Speed over Time - All Vehicles'
            filename = 'speed_over_time_all_vehicles.png'
        
        df = pd.read_sql_query(query, self.conn)
        
        plt.figure(figsize=(12, 6))
        plt.plot(df['simulation_time'], df['speed' if vehicle_id else 'avg_speed'], 
                marker='o', markersize=3, linewidth=2)
        plt.xlabel('Simulation Time (seconds)')
        plt.ylabel('Speed (m/s)')
        plt.title(title)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig(filename, dpi=150)
        plt.show()
        
        return df
    
    def export_to_csv(self, filename='sumo_data_export.csv'):
        """Export all data to CSV for further analysis"""
        query = f"SELECT * FROM {self.table_name}"
        df = pd.read_sql_query(query, self.conn)
        df.to_csv(filename, index=False)
        print(f"Data exported to {filename}")
        return df
    
    def show_detailed_summary(self):
        """Show a detailed summary of all data"""
        print("\n" + "="*60)
        print("DETAILED DATA ANALYSIS SUMMARY")
        print("="*60)
        
        # Basic stats
        stats = self.basic_statistics()
        print(f"\n📊 BASIC STATISTICS:")
        print(f"   Total records: {stats['total_records'][0]:,}")
        print(f"   Unique vehicles: {stats['unique_vehicles'][0]}")
        print(f"   Time range: {stats['first_timestamp'][0]:.1f}s - {stats['last_timestamp'][0]:.1f}s")
        print(f"   Average speed: {stats['avg_speed'][0]:.2f} m/s")
        print(f"   Min speed: {stats['min_speed'][0]:.2f} m/s")
        print(f"   Max speed: {stats['max_speed'][0]:.2f} m/s")
        
        # Vehicle list
        vehicles = self.vehicle_trajectories()
        print(f"\n🚗 VEHICLES DETECTED ({len(vehicles)} total):")
        print("   Vehicle ID      Data Points    First Seen    Last Seen")
        print("   " + "-"*50)
        for _, row in vehicles.head(10).iterrows():
            print(f"   {row['vehicle_id']:15s} {row['data_points']:12d} {row['first_seen']:12.1f}s {row['last_seen']:10.1f}s")
        
        if len(vehicles) > 10:
            print(f"   ... and {len(vehicles) - 10} more vehicles")
        
        # Speed by edge
        speeds = self.speed_analysis()
        print(f"\n🛣️  SPEED BY ROAD SEGMENT:")
        print("   Edge           Avg Speed   Observations")
        print("   " + "-"*40)
        for _, row in speeds.iterrows():
            print(f"   {row['edge']:15s} {row['avg_speed']:10.2f} {row['observations']:13d}")
    
    def close(self):
        self.conn.close()

def run_analysis():
    print("="*60)
    print("   SUMO TRAFFIC DATA ANALYSIS - BIG DATA STORAGE")
    print("="*60)
    
    analyzer = DataAnalyzer('sumo_data.db')
    
    # 1. Show detailed summary
    analyzer.show_detailed_summary()
    
    # 2. Plot trajectories
    print("\n📈 GENERATING VISUALIZATIONS...")
    print("   Plotting vehicle trajectories...")
    analyzer.plot_trajectories()
    
    # 3. Plot speed over time
    print("   Plotting speed over time for all vehicles...")
    analyzer.speed_over_time()
    
    # Plot speed for a specific vehicle
    print("   Plotting speed over time for a sample vehicle...")
    vehicles_query = "SELECT vehicle_id FROM vehicle_telemetry GROUP BY vehicle_id LIMIT 1"
    sample_vehicle = pd.read_sql_query(vehicles_query, analyzer.conn)['vehicle_id'].iloc[0]
    analyzer.speed_over_time(sample_vehicle)
    
    # 4. Export data
    print("\n💾 EXPORTING DATA...")
    analyzer.export_to_csv()
    
    # 5. Advanced analysis
    print("\n🔍 ADVANCED ANALYSIS:")
    
    # Check vehicle types
    query = """
    SELECT 
        CASE 
            WHEN vehicle_id LIKE 'veh%' THEN 'Main Vehicle'
            WHEN vehicle_id LIKE 'vehicles1%' THEN 'Flow Type 1 (Red)'
            WHEN vehicle_id LIKE 'vehicles2%' THEN 'Flow Type 2 (Blue)'
            ELSE 'Other'
        END as vehicle_type,
        COUNT(*) as count,
        AVG(speed) as avg_speed,
        MIN(speed) as min_speed,
        MAX(speed) as max_speed
    FROM vehicle_telemetry
    GROUP BY vehicle_type
    ORDER BY count DESC
    """
    
    type_analysis = pd.read_sql_query(query, analyzer.conn)
    print("\n   Vehicle Type Analysis:")
    for _, row in type_analysis.iterrows():
        print(f"   {row['vehicle_type']:20s}: {row['count']:4d} records, "
              f"Avg speed: {row['avg_speed']:.2f} m/s")
    
    analyzer.close()
    
    print("\n" + "="*60)
    print("✅ ANALYSIS COMPLETE!")
    print("="*60)
    print("\n📁 Files created:")
    print("   - sumo_trajectories.png        : Vehicle movement paths")
    print("   - speed_over_time_all_vehicles.png : Average speed over time for all vehicles")
    print("   - speed_over_time_vehicle_*.png    : Speed over time for individual vehicle")
    print("   - sumo_data_export.csv         : Complete dataset in CSV")
    print("\n🎯 Total data points analyzed: 758 (from your Kafka stream)")

if __name__ == "__main__":
    run_analysis()