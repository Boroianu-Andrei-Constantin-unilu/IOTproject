import sqlite3
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from config.config import config

# Define weights for each criterion
weights = {'air_quality': 0.25, 'co2_level': 0.20, 'humidity': 0.15, 'temperature': 0.20, 'sound_level': 0.10, 'light_intensity': 0.10}

def get_db_connection():
    conn = sqlite3.connect(config.DATABASE_URI)
    conn.row_factory = sqlite3.Row
    return conn

def get_room_scores():
    # Fetch average values for each sensor and room
    averages_query = """SELECT room_name, 
                            (SELECT AVG(pm25 + pm10) / 2 FROM air_quality WHERE room_name = r.room_name) AS air_quality,
                            (SELECT AVG(co2_level) FROM co2_levels WHERE room_name = r.room_name) AS co2_level,
                            (SELECT AVG(humidity) FROM humidity WHERE room_name = r.room_name) AS humidity,
                            (SELECT AVG(temperature) FROM temperature WHERE room_name = r.room_name) AS temperature,
                            (SELECT AVG(sound_level) FROM sound_levels WHERE room_name = r.room_name) AS sound_level,
                            (SELECT AVG(light_intensity) FROM light_intensity WHERE room_name = r.room_name) AS light_intensity
                        FROM room_facilities r"""
    
    # Execute query and convert result to DataFrame
    rooms_data = cursor.execute(averages_query).fetchall()
    df = pd.DataFrame(rooms_data)

    # Normalize the data
    scaler = MinMaxScaler()
    normalized_data = scaler.fit_transform(df.iloc[:, 1:])
    df.iloc[:, 1:] = normalized_data

    # Calculate weighted scores
    df['score'] = (df['air_quality'] * weights['air_quality'] + df['co2_level'] * weights['co2_level'] + df['humidity'] * weights['humidity'] + df['temperature'] * weights['temperature'] + df['sound_level'] * weights['sound_level'] + df['light_intensity'] * weights['light_intensity'])

    # Sort by score in descending order, and convert to a list of dictionaries
    df = df.sort_values(by='score', ascending=False)
    print(df[['room_name', 'score']].to_dict(orient='records'))
    pass