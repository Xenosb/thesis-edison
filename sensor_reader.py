import app
from multiprocessing import Process
from random import randint
from struct import unpack
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
      from mraa import I2c, Gpio, DIR_OUT
      self.i2c = I2c(0)
      self.i2c.frequency(0)
      self.i2c.address(0x10)
      self.read_f = self.i2c_read_sensors
      #self.sense_out = Gpio(14)
      #self.sense_out.dir(DIR_OUT)
    else:
      #self.purge_db() # Comment if you want data to persist, bear in mind that auto_id is not reset
      if len(SensorValue.query.all()) == 0:
        print('Database empty, adding sample data')
        self.mock_sample_db()
        print('Added {} values to database'.format(len(SensorValue.query.all())))
    
    self.initialized = True
    self.active.value = True


  '''
  Main runner method
  '''
  def run(self, *args, **kwargs):
    if not self.initialized:
      self.initialize()

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
  Reads data from actual I2C network. Available only on mraa devices.
  '''
  def i2c_read_sensors(self):
    # for regular use
    for node_pos in range(1,3):
      try:
        self.i2c_read_all_sensors(node_pos)
      except IOError:
        print 'Unable to read from node {}'.format(node_pos)

    # to be used if device has a problem receiving packages
    '''
    for node_pos in range(1,3):
      for sensor_pos in range(1):
        self.i2c_read_sensor(node_pos, sensor_pos)
    '''

    # for high precision, not implemented yet
    '''
    for node_pos in range(1,3):
      self.i2c_read_all_sensors_buffered(node_pos)
    '''
    

  def i2c_read_all_sensors(self, node_pos):
    self.i2c.address(0x10 + node_pos)
    self.i2c.writeReg(0xaa, 2)
    values = self.i2c.readBytesReg(0xa0, 32)
    for sensor_pos in range(16):
      res = 65535 - unpack('H', values[sensor_pos*2:sensor_pos*2+2])[0]
      sensor = Sensor.query.filter_by(position=sensor_pos).filter_by(node_id=node_pos).first()
      reading = SensorValue(sensor.id, res)
      sensor.last_value = reading.value
      sensor.last_update = datetime.now()
      db.session.add(reading)
      db.session.add(sensor)
    db.session.commit()


  # Not implemented YET
  def i2c_read_all_sensors_buffered(self, node_pos):
    self.i2c.address(0x10 + node_pos)
    self.i2c.writeReg(0xaa, 2)
    self.i2c.readBytesReg(0xa1, 640)


  def i2c_read_sensor(self, node_pos, sensor_pos):
    self.i2c.address(0x10 + node_pos)
    success = False

    for i in range(5):
      # We need this because bad i2c implementation on mraa
      # Problem is that mraa device is not setting the stop bit after it receives the data from the node
      self.i2c.writeReg(0xaa, 2)

      try:
        value = self.i2c.readBytesReg(sensor_pos, 2)
        res = 65535 - unpack('H',value)[0]
        if res > 150:
          success = True
          break
      except IOError:
        pass

    if not success:
      res = 0

    sensor = Sensor.query.filter_by(position=sensor_pos).filter_by(node_id=node_pos).first()
    reading = SensorValue(sensor.id, res)
    sensor.last_value = reading.value
    sensor.last_update = datetime.now()
    db.session.add(reading)
    db.session.add(sensor)
    db.session.commit()


  '''
  Distributes the I2C addresses to the nodes based on their position
  '''
  def distribute_i2c_addresses(self):
    if not self.edison:
      print('This is supported only on mraa devices')
      return

    self.i2c.address(0x00) # Switch to general call address
    self.i2c.write(0xcd) # Send release i2c address (0xcd)
    self.sense_out.write(1) # Set position sensing pin to high so that first node can be identified
    self.i2c.write(0xcd) # Send release i2c address (0xcd)

    i = 1
    while (set_i2c_address):
      i += 1
  

  '''
  Tries to set the I2C address of the node which has sense_in high
  In case that this works, it yields true and in case it doesn't it yields false
  '''
  def set_i2c_address(self):
    pass


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
      node = Node(i)
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


  '''
  Randoms values from a sensor network.
  '''
  def mock_read_sensors(self):
    for sensor in Sensor.query.all():
      reading = SensorValue(sensor.id, randint(0,65535))
      sensor.last_value = reading.value
      sensor.last_update = datetime.now()
      db.session.add(reading)
      db.session.add(sensor)
      db.session.commit()
    print(len(SensorValue.query.all()))
