from app import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSON

class System(): # Note that his is not a db table but just a helper class
  def __init__(self):
    self.nodes = []

  def add_node(self, node):
    self.nodes.append([node])

  def serialize(self):
    from app import reader
    result = {
      'state': reader.active.value
      }
    for node in self.nodes:
      result[node[0].id] = node[0].serialize()
    
    return result


'''
========NODE=========
id          - Integer
name        - Integer
sensors     - ForeignKey(Sensor)
last_update - DateTime
=====================
'''
class Node(db.Model):
  __tablename__ = 'node'

  id = Column(Integer, primary_key=True)
  name = Column(Integer, default=-1)
  last_update = Column(DateTime(), default=datetime.utcnow)
  sensors = db.relationship('Sensor', backref='node', lazy="dynamic")

  def __init__(self, name):
    self.name = name

  def __repr__(self):
    return 'Node<id {}>'.format(self.id)
  
  def serialize(self):
    return {
      'id': self.id,
      'name': self.name,
      'last_update': self.last_update,
      'sensors': [s.id for s in self.sensors]
    }


'''
=======SENSOR========
id          - Integer
node_id     - ForeignKey(Node)
position    - Integer
last_value  - Integer
last_update - DateTime
=====================
'''
class Sensor(db.Model):
  __tablename__ = 'sensor'

  id = Column(Integer, primary_key=True)
  node_id = Column(Integer, ForeignKey('node.id'))
  position = Column(Integer(), default=-1)
  last_value = Column(Integer(), default=0)
  last_update = Column(DateTime(), default=datetime.now)
  values = db.relationship('SensorValue')

  def __init__(self, node_id, position):
    self.node_id = node_id
    self.position = position
    self.last_value = 0
  
  def __repr__(self):
    return 'Sensor<id {} node {} position {}>'.format(self.id, self.node.id, self.position)

  def serialize(self):
    return {
      'id': self.id,
      'node_id': self.node.id,
      'position': self.position,
      'last_value': self.last_value,
      'last_update': self.last_update
    }

'''
====SENSOR VALUE=====
id          - Integer
sensor_id   - ForeignKey(Node)
value       - Integer
timestamp   - DateTime
=====================
'''
class SensorValue(db.Model):
  __tablename__ = 'sensorValue'

  id = Column(Integer, primary_key=True)
  sensor_id = Column(Integer, ForeignKey('sensor.id'))
  value = Column(Integer())
  timestamp = Column(DateTime(), default=datetime.utcnow)

  def __init__(self, sensor_id, value):
    self.sensor_id = sensor_id
    self.value = value
  
  def __repr__(self):
    return 'Reading<id {} node {} position {} value {} time {}>'.format(self.id, self.sensor.node.id, self.sensor.position, self.value, self.timestamp)
  
  def serialize(self):
    return {
      'id': self.id,
      'sensor_id': self.sensor_id,
      'value': self.value,
      'timestamp': self.timestamp
    }