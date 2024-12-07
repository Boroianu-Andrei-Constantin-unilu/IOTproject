from flask import Flask
from flask_jwt_extended import JWTManager
from config.config import config

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = config.JWT_SECRET_KEY
jwt = JWTManager(app)

# Import and register blueprints for endpoints
from api.endpoints.rooms import rooms_bp
from api.endpoints.sensor_data import sensor_data_bp
from api.endpoints.rankings import rankings_bp

app.register_blueprint(rooms_bp, url_prefix='/api')
app.register_blueprint(sensor_data_bp, url_prefix='/api')
app.register_blueprint(rankings_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)