from flask_redis import FlaskRedis
from celery import Celery
from flask import Flask
from time import sleep

reader_active = False
celery = Celery()
UPDATE_FREQ = 0.1 # seconds

def create_celery(flask_app):
  redis_store = FlaskRedis(flask_app)

  celery = Celery(flask_app.import_name, broker=flask_app.config['CELERY_BROKER_URL'])
  celery.conf.update(flask_app.config)

  UPDATE_FREQ = flask_app.config['UPDATE_FREQ']
  return celery

@celery.task
def sensor_reader(db, edison=False):
  if edison:
    from mraa import I2c      
    i2c = I2c(0)
    i2c.frequency(0)
    read = i2c_read_sensors
  else:
    read = mock_read_sensors

  reader_active = True

  while reader_active:
    read(db)
    sleep(UPDATE_FREQ)

  return x + y

@celery.task
def pause_reader(edison=False):
  reader_active = False

@celery.task
def mock_read_sensors(db):
  from models import Node, Sensor, SensorValue
  node = Node()
  #db.session.add(node)
  #db.session.commit()
  print(len(Node.query.all()))
  return 0

@celery.task
def i2c_read_sensors(db):
  print('i2c')
  return 0