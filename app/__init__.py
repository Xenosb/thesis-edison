import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

flask_app = Flask(__name__, instance_relative_config=True)

# Set environment
flask_app.config.from_object('config.config_s')

# Configure db and models
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(flask_app)

# Make sure this is executed only once
if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
  from sensor_reader import SensorReader
  sr = SensorReader()
  sr.start()

# Load views
from app import views