import os

class Config:
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your_jwt_secret_key")

    DATABASE_URI = "sqlite:///../database/confort_room.db"

config = Config()