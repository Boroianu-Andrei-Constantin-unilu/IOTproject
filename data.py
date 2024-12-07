import sqlite3
import json
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from flask import Flask, jsonify, request
from flask_cors import CORS

# Creating connection to database
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

# Creating tables for room facilities and sensors with timestamps for time-series data

# Room facilities
cursor.execute("""CREATE TABLE IF NOT EXISTS room_facilities (room_name TEXT PRIMARY KEY, videoprojector BOOLEAN, seating_capacity INTEGER, computers INTEGER, robots_for_training INTEGER);""")

# Air quality sensors (PM2.5 and PM10)
cursor.execute("""CREATE TABLE IF NOT EXISTS air_quality (room_name TEXT, timestamp TEXT, pm25 REAL, pm10 REAL, FOREIGN KEY(room_name) REFERENCES room_facilities(room_name));""")

# CO2 levels
cursor.execute("""CREATE TABLE IF NOT EXISTS co2_levels (room_name TEXT, timestamp TEXT, co2_level REAL, FOREIGN KEY(room_name) REFERENCES room_facilities(room_name));""")

# Humidity levels
cursor.execute("""CREATE TABLE IF NOT EXISTS humidity (room_name TEXT, timestamp TEXT, humidity REAL, FOREIGN KEY(room_name) REFERENCES room_facilities(room_name));""")

# Sound levels
cursor.execute("""CREATE TABLE IF NOT EXISTS sound_levels (room_name TEXT, timestamp TEXT, sound_level REAL, FOREIGN KEY(room_name) REFERENCES room_facilities(room_name));""")

# Temperature levels
cursor.execute("""CREATE TABLE IF NOT EXISTS temperature (room_name TEXT, timestamp TEXT, temperature REAL, FOREIGN KEY(room_name) REFERENCES room_facilities(room_name));""")

# VOC Levels
cursor.execute("""CREATE TABLE IF NOT EXISTS voc_levels (room_name TEXT, timestamp TEXT, voc_level REAL, FOREIGN KEY(room_name) REFERENCES room_facilities(room_name));""")

# Light intensity levels
cursor.execute("""CREATE TABLE IF NOT EXISTS light_intensity (room_name TEXT, timestamp TEXT, light_intensity REAL, FOREIGN KEY(room_name) REFERENCES room_facilities(room_name));""")

# Commit the creation of tables
conn.commit()

# Check successful table creation
tables = cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()

print(tables)

# Paths to JSON files
files = {'room_facilities': 'room_facilities_data.json', 'air_quality': 'air_quality_sensor_data.json', 'co2_levels': 'co2_sensor_data.json', 'humidity': 'humidity_sensor_data.json', 'sound_levels': 'sound_sensor_data.json', 'temperature': 'temperature_sensor_data.json', 'voc_levels': 'voc_sensor_data.json', 'light_intensity': 'LightIntensity_sensor_data.json'}

# Load and insert room facilities data
with open(files['room_facilities'], 'r') as f:
    facilities_data = json.load(f)
    for room in facilities_data['rooms']:
        room_name = room['name']
        facilities = room['facilities']
        cursor.execute("""INSERT OR REPLACE INTO room_facilities (room_name, videoprojector, seating_capacity, computers, robots_for_training) VALUES (?, ?, ?, ?, ?);""", (room_name, facilities.get('videoprojector', False), facilities.get('seating_capacity', None), facilities.get('computers', None), facilities.get('robots_for_training', None)))
        
# Commit successful population of room facilities
conn.commit()

# Query the room facilities table, to ensure that data was inserted
room_facilities_entries = cursor.execute("SELECT * FROM room_facilities;").fetchall()

print(room_facilities_entries)

# Helper function to insert time-series sensor data
def insert_sensor_data(data, table_name, columns):
    for room in data['rooms']:
        room_name = room['name']
        for entry in room[columns[1]]:
            timestamp = entry['timestamp']
            value = entry.get(columns[2], None)
            cursor.execute(f"""INSERT OR REPLACE INTO {table_name} (room_name, timestamp, {columns[2]}) VALUES (?, ?, ?)""", (room_name, timestamp, value))
            
    conn.commit()
    
# Load and insert sensor data from each file

# Air Quality Data
with open(files['air_quality'], 'r') as f:
    air_quality_data = json.load(f)
    insert_sensor_data(air_quality_data, 'air_quality', ('room_name', 'air_quality_values', 'pm25'))
    insert_sensor_data(air_quality_data, 'air_quality', ('room_name', 'air_quality_values', 'pm10'))

# CO2 Levels Data
with open(files['co2_levels'], 'r') as f:
    co2_data = json.load(f)
    insert_sensor_data(co2_data, 'co2_levels', ('room_name', 'co2_values', 'co2_level'))

# Humidity Data
with open(files['humidity'], 'r') as f:
    humidity_data = json.load(f)
    insert_sensor_data(humidity_data, 'humidity', ('room_name', 'humidity_values', 'humidity'))

# Sound Level Data
with open(files['sound_levels'], 'r') as f:
    sound_data = json.load(f)
    insert_sensor_data(sound_data, 'sound_levels', ('room_name', 'sound_values', 'sound_level'))

# Temperature Data
with open(files['temperature'], 'r') as f:
    temperature_data = json.load(f)
    insert_sensor_data(temperature_data, 'temperature', ('room_name', 'temperature_values', 'temperature'))

# VOC Levels Data
with open(files['voc_levels'], 'r') as f:
    voc_data = json.load(f)
    insert_sensor_data(voc_data, 'voc_levels', ('room_name', 'voc_values', 'voc_level'))

# Light Intensity Data
with open(files['light_intensity'], 'r') as f:
    light_data = json.load(f)
    insert_sensor_data(light_data, 'light_intensity', ('room_name', 'light_intensity_values', 'light_intensity'))
    
# Verify one of the tables for data insertion
co2_entries = cursor.execute("SELECT * FROM co2_levels LIMIT 5").fetchall()

print("Checking CO2 tables for data insertion: ", co2_entries)

# Function adjusted to handle different value keys in sensor data
def insert_sensor_data_custom(data, table_name, room_key, values_key, value_column):
    for room in data['rooms']:
        room_name = room[room_key]
        for entry in room[values_key]:
            timestamp = entry['timestamp']
            value = entry[value_column]
            cursor.execute(f"""INSERT OR REPLACE INTO {table_name} (room_name, timestamp, {value_column}) VALUES (?, ?, ?)""", (room_name, timestamp, value))
            
    conn.commit()
    
# Load and insert remaining sensor data

# CO2 Levels Data
with open(files['co2_levels'], 'r') as f:
    co2_data = json.load(f)
    insert_sensor_data_custom(co2_data, 'co2_levels', 'name', 'co2_values', 'co2_level')

# Humidity Data
with open(files['humidity'], 'r') as f:
    humidity_data = json.load(f)
    insert_sensor_data_custom(humidity_data, 'humidity', 'name', 'humidity_values', 'humidity')

# Sound Level Data
with open(files['sound_levels'], 'r') as f:
    sound_data = json.load(f)
    insert_sensor_data_custom(sound_data, 'sound_levels', 'name', 'sound_values', 'sound_level')

# Temperature Data
with open(files['temperature'], 'r') as f:
    temperature_data = json.load(f)
    insert_sensor_data_custom(temperature_data, 'temperature', 'name', 'temperature_values', 'temperature')

# VOC Levels Data
with open(files['voc_levels'], 'r') as f:
    voc_data = json.load(f)
    insert_sensor_data_custom(voc_data, 'voc_levels', 'name', 'voc_values', 'VOC_level')

# Light Intensity Data
with open(files['light_intensity'], 'r') as f:
    light_data = json.load(f)
    insert_sensor_data_custom(light_data, 'light_intensity', 'name', 'light_intensity_values', 'light_intensity')
    
# Verify one of the tables for data insertion
temperature_entries = cursor.execute("SELECT * FROM temperature LIMIT 5").fetchall()

print("Checking temperature tables for data insertion: ", temperature_entries)

# Define weights for each criterion
weights = {'air_quality': 0.25, 'co2_level': 0.20, 'humidity': 0.15, 'temperature': 0.20, 'sound_level': 0.10, 'light_intensity': 0.10}

# Fetch data for each criterion and calculate averages per room
def fetch_and_calculate_averages(table_name, value_column):
    query = f"""SELECT room_name, AVG({value_column}) AS avg_value FROM {table_name} GROUP BY room_name"""
    return pd.read_sql_query(query, conn)

# Air Quality (combined PM2.5 and PM10)
air_quality_pm25 = fetch_and_calculate_averages('air_quality', 'pm25')
air_quality_pm10 = fetch_and_calculate_averages('air_quality', 'pm10')
air_quality = air_quality_pm25.copy()
air_quality['avg_value'] = (air_quality_pm25['avg_value'] + air_quality_pm10['avg_value']) / 2

# Fetching other sensor averages
co2 = fetch_and_calculate_averages('co2_levels', 'co2_level')
humidity = fetch_and_calculate_averages('humidity', 'humidity')
temperature = fetch_and_calculate_averages('temperature', 'temperature')
sound_level = fetch_and_calculate_averages('sound_levels', 'sound_level')
light_intensity = fetch_and_calculate_averages('light_intensity', 'light_intensity')

# Combine data into a single DataFrame
room_data = air_quality[['room_name']].copy()
room_data['air_quality'] = air_quality['avg_value']
room_data = room_data.merge(co2[['room_name', 'avg_value']], on='room_name', how='left').rename(columns={'avg_value': 'co2_level'})
room_data = room_data.merge(humidity[['room_name', 'avg_value']], on='room_name', how='left').rename(columns={'avg_value': 'humidity'})
room_data = room_data.merge(temperature[['room_name', 'avg_value']], on='room_name', how='left').rename(columns={'avg_value': 'temperature'})
room_data = room_data.merge(sound_level[['room_name', 'avg_value']], on='room_name', how='left').rename(columns={'avg_value': 'sound_level'})
room_data = room_data.merge(light_intensity[['room_name', 'avg_value']], on='room_name', how='left').rename(columns={'avg_value': 'light_intensity'})

# Normalize the data
scaler = MinMaxScaler()
normalized_values = scaler.fit_transform(room_data.iloc[:, 1:])
room_data.iloc[:, 1:] = normalized_values

# Calculate the weighted score for each room
room_data['score'] = (room_data['air_quality'] * weights['air_quality'] + room_data['co2_level'] * weights['co2_level'] + room_data['humidity'] * weights['humidity'] + room_data['temperature'] * weights['temperature'] + room_data['sound_level'] * weights['sound_level'] + room_data['light_intensity'] * weights['light_intensity'])

# Rank the rooms by score (the higher, the better)
room_data = room_data.sort_values(by='score', ascending=False).reset_index(drop=True)
print(room_data[['room_name', 'score']]).to_dict(orient='records')

# Initialize Flask App
app = Flask(__name__)

# Database connection function
def get_db_connection():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row # Dictionary-like access to rows
    return conn

# Endpoint to retrieve all rooms with facilities and average sensor values
@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Query room facilities
    facilities_query = """SELECT * FROM room_facilities"""
    facilities = cursor.execute(facilities_query).fetchall()
    
    # Query average sensor values per room
    averages_query = """SELECT room_name, 
                            (SELECT AVG(pm25 + pm10) / 2 FROM air_quality WHERE room_name = r.room_name) AS air_quality,
                            (SELECT AVG(co2_level) FROM co2_levels WHERE room_name = r.room_name) AS co2_level,
                            (SELECT AVG(humidity) FROM humidity WHERE room_name = r.room_name) AS humidity,
                            (SELECT AVG(temperature) FROM temperature WHERE room_name = r.room_name) AS temperature,
                            (SELECT AVG(sound_level) FROM sound_levels WHERE room_name = r.room_name) AS sound_level,
                            (SELECT AVG(light_intensity) FROM light_intensity WHERE room_name = r.room_name) AS light_intensity
                        FROM room_facilities r"""
    averages = cursor.execute(averages_query).fetchall()
    conn.close()

    # Format response
    response = []
    for room, avg_values in zip(facilities, averages):
        room_data = dict(room)
        room_data.update({key: avg_values[key] for key in avg_values.keys() if key != 'room_name'})
        response.append(room_data)

    return jsonify(response)

# Endpoint to retrieve room rankings, based on suitability score
@app.route('/api/room-rankings', methods=['GET'])
def get_room_rankings():
    # Ranked room data prepared previously
    ranked_rooms = room_data[['room name', 'score']].to_dict(orient='records')
    return jsonify(ranked_rooms)

app.run(debug=True)
CORS(app)