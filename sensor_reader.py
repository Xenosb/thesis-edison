import app
from multiprocessing import Process
from random import randint
from time import sleep
from models import *

class SensorReader(Process):

  def __init__(self, pipe, active):
    self.name = 'SensorReader'
    self.initialized = False
    self.active = active
    self.pipe = pipe
    self.active.value = False
    super(SensorReader, self).__init__()

  '''
  Initializes the app and db if needed.
  '''
  def initialize(self):
    self.db = app.db
    self.edison = app.flask_app.config['EDISON']
    self.update_freq = app.flask_app.config['UPDATE_FREQ']
    self.read_f = self.mock_read_sensors

    if self.edison:
      from mraa import I2c      
      self.i2c = I2c(0)
      self.i2c.frequency(0)
      self.read_f = i2c_read_sensors
    else:
      #self.purge_db() # Comment if you want data to persist
      if len(SensorValue.query.all()) == 0:
        print('Database empty, adding sample data')
        self.mock_sample_db()
        print('Added {} values to database'.format(len(SensorValue.query.all())))
    
    self.initialized = True


  '''
  Starts the celery task. Initializes in case it is needed.
  '''
  def run(self, *args, **kwargs):
    if not self.initialized:
      self.initialize()

    self.active.value = True

    # Run forever
    while True:
      # Read data from the pipe
      if self.pipe.poll():
        if self.pipe.recv() == 'stop' and self.active.value == True:
          self.active.value = False
          print("stop")
        if self.pipe.recv() == 'start' and self.active.value == False:
          self.active.value = True
          print("start")

      # Read data if active
      if self.active.value:
        self.read_f()
        sleep(self.update_freq)


  '''
  Randoms values from a sensor network.
  '''
  def mock_read_sensors(self):
    for sensor in Sensor.query.all():
      reading = SensorValue(sensor.id, randint(0,65535))
      db.session.add(reading)
      db.session.commit()
    print(len(SensorValue.query.all()))


  '''
  Reads data from actual I2C network. Available only on mraa devices.
  '''
  def i2c_read_sensors(self):
    print('i2c')


  '''
  Clears the database. Useful for debug.
  '''
  def purge_db(self):
    print('Purging database')
    for value in SensorValue.query.all():
      self.db.session.delete(value)
    for sensor in Sensor.query.all():
      self.db.session.delete(sensor)
    for node in Node.query.all():
      self.db.session.delete(node)
    self.db.session.commit()


  '''
  Inserts sample data to database. Useful for debug.
  '''
  def mock_sample_db(self, n_nodes=4, n_sensors=16, n_samples=50):
    for i in range(n_nodes):
      node = Node()
      self.db.session.add(node)
      self.db.session.commit()

      for j in range(n_sensors):
        sensor = Sensor(node_id = node.id, position = j)
        self.db.session.add(sensor)
        self.db.session.commit()
      
        for k in range(n_samples):
          sample = SensorValue(sensor_id = sensor.id, value = randint(0,65535))
          self.db.session.add(sample)
        self.db.session.commit()