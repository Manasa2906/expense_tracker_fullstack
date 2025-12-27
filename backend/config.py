import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = "change-this-secret-key"
    JWT_SECRET_KEY = "change-this-jwt-secret"

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" + os.path.join(BASE_DIR, "expense_tracker.db")
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
