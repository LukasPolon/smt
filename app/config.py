import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = "test"
    SQLALCHEMY_DATABASE_URI = "postgresql://test:test@localhost/test"
