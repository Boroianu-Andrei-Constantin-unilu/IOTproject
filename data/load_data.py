import sqlite3
import json

# Database connection
DATABASE_PATH = '../database/confort_room.db'

def load_data():
    conn = sqlite3.connect(DATABASE_PATH)
    cursor = conn.cursor()

    # Load room facilities data
    with open('room_facilities_data.json', 'r') as f:
        facilities_data = json.load(f)
        for room in facilities_data['rooms']:
            cursor.execute("""INSERT OR REPLACE INTO room_facilities (room_name, videoprojector, seating_capacity, computers, robots_for_training) VALUES (?, ?, ?, ?, ?);""",
                (room['name'], room['facilities'].get('videoprojector', False), room['facilities'].get('seating_capacity', None), room['facilities'].get('computers', None), room['facilities'].get('robots_for_training', None)))
            
    # Load other sensor data (similar approach for each sensor JSON file)
    # Example given: CO2 Data
    with open('co2_sensor_data.json', 'r') as f:
        co2_data = json.load(f)
        for room in co2_data['rooms']:
            for entry in room['co2_values']:
                cursor.execute("""INSERT INTO co2_levels (room_name, timestamp, co2_level) VALUES (?, ?, ?)""", (room['name'], entry['timestamp'], entry['co2_level']))

    # Commit changes and close connection
    conn.commit()
    conn.close()

if __name__ == '__main__':
    load_data()