from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_redis import FlaskRedis
from celery import Celery
from multiprocessing import Process


flask_app = Flask(__name__, instance_relative_config=True)

# Set environment
flask_app.config.from_object('config.ClientTestConfig')

# Configure db and models
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(flask_app)

# Configure Redis
redis_store = FlaskRedis(flask_app)

# Configure Celary
celery = Celery(flask_app.import_name, broker=flask_app.config['CELERY_BROKER_URL'])
celery.conf.update(flask_app.config)

# Load views
from app import views
from app import tasks

# Spin up celery worker
c = Process(target=celery.worker_main)
c.start()

# Rock n' roll
if __name__ == '__main__':
  flask_app.run(host='0.0.0.0', debug='True')