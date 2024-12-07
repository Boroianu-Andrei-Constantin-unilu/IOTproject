import sqlite3

conn = sqlite3.connect('confort_room.db')
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

# Commit the creation of tables and close
conn.commit()
conn.close()