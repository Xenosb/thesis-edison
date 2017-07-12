from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from multiprocessing import Process
import tasks


flask_app = Flask(__name__, instance_relative_config=True)

# Set environment
flask_app.config.from_object('config.config_s')

# Configure db and models
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(flask_app)

# Load views
from app import views
from app import tasks

# Create celery app
celery = tasks.create_celery(flask_app)

# Spin up celery worker
c = Process(target=celery.worker_main)
c.start()

reader = Process(target=tasks.sensor_reader, args=(flask_app.config['EDISON'],))
reader.start()

# Rock n' roll
if __name__ == '__main__':
  flask_app.run(host='0.0.0.0', debug='True')