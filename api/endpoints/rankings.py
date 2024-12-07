from flask import Blueprint, jsonify
import pandas as pd
from api.utils.db_utils import get_room_scores

rankings_bp = Blueprint('rankings', __name__)

@rankings_bp.route('/room-rankings', methods=['GET'])
def get_room_rankings():
    # Fetch room scores from precomputed method/function
    scores = get_room_scores()
    return jsonify(scores)