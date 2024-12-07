from flask import Blueprint, jsonify
from api.utils.db_utils import get_db_connection

rooms_bp = Blueprint('rooms', __name__)

@rooms_bp.route('/rooms', methods=['GET'])
def get_rooms():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """SELECT * FROM room_facilities"""
    rooms = cursor.execute(query).fetchall()
    conn.close()
    return jsonify([dict(room) for room in rooms])