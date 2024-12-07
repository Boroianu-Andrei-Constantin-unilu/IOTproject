from flask import Blueprint, jsonify, request
from api.utils.db_utils import get_db_connection

sensor_data_bp = Blueprint('sensor_data', __name__)

@sensor_data_bp.route('/room/<string:room_name>/data', methods=['GET'])
def get_room_data(room_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    data = {
        'air_quality': cursor.execute("SELECT * FROM air_quality WHERE room_name = ?", (room_name,)).fetchall(),
        'temperature': cursor.execute("SELECT * FROM temperature WHERE room_name = ?", (room_name,)).fetchall(),
        'humidity': cursor.execute("SELECT * FROM humidity WHERE room_name = ?", (room_name,)).fetchall(),
        'co2_levels': cursor.execute("SELECT * FROM co2_levels WHERE room_name = ?", (room_name,)).fetchall(),
        'voc_levels': cursor.execute("SELECT * FROM voc_levels WHERE room_name = ?", (room_name,)).fetchall(),
        'sound_levels': cursor.execute("SELECT * FROM sound_levels WHERE room_name = ?", (room_name,)).fetchall(),
        'light_intensity': cursor.execute("SELECT * FROM light_intensity WHERE room_name = ?", (room_name,)).fetchall()}
    conn.close()
    return jsonify({sensor: [dict(entry) for entry in entries] for sensor, entries in data.items()})