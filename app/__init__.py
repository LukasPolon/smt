from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from app.config import Config
from flask_migrate import Migrate



APP = Flask(__name__)
APP.config.from_object(Config)
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
DB = SQLAlchemy(APP)
MIGRATE = Migrate(APP, DB)
