from flask_redis import FlaskRedis
from celery import Celery
from flask import Flask
from time import sleep

celery = Celery()

def create_celery(flask_app):
  # Configure Redis
  redis_store = FlaskRedis(flask_app)

  # Configure Celery
  celery = Celery(flask_app.import_name, broker=flask_app.config['CELERY_BROKER_URL'])
  celery.conf.update(flask_app.config)
  
  return celery

@celery.task
def sensor_reader(edison=False):
  if edison:
    from mraa import I2c      
    i2c = I2c(0)
    i2c.frequency(0)
    read = i2c_read_sensors
  else:
    read = mock_read_sensors

  while True:
    read()
    sleep(0.1)
  return x + y

@celery.task
def mock_read_sensors():
  print('mock')
  return 0

@celery.task
def i2c_read_sensors():
  print('i2c')
  return 0