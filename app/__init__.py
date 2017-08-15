import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from multiprocessing import Value, Pipe

flask_app = Flask(__name__, instance_relative_config=True)

# Set environment
flask_app.config.from_object('config.config_s')

# Configure db and models
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(flask_app)

# Make sure this is executed only once
if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
  # Prepare pipe and shared status variable
  parent_pipe, reader_pipe = Pipe()
  reader_active = Value('d', 0) # Change to 1 to autostart

  # Create a reader process
  from sensor_reader import SensorReader
  reader = SensorReader(reader_pipe, reader_active)
  reader.start()

# Load views
from app import views