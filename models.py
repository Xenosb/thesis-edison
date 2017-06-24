from app import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import JSON

'''
id          - Integer
sensors     - ForeignKey(Sensor)
'''
class Node(db.Model):
  __tablename__ = 'node'

  id = Column(Integer, primary_key=True)
  sensors = db.relationship('Sensor', backref='node', lazy="dynamic")

  def __init__(self):
    pass

  def __repr__(self):
    return 'Node<id {}>'.format(self.id)


'''
id          - Integer
node_id     - ForeignKey(Node)
position    - Integer
last_value  - Integer
'''
class Sensor(db.Model):
  __tablename__ = 'sensor'

  id = Column(Integer, primary_key=True)
  node_id = Column(Integer, ForeignKey('node.id'))
  position = Column(Integer())
  last_value = Column(Integer())
  values = db.relationship('SensorValue', backref='Sensor', lazy='dynamic')

  def __init__(self, node_id, position, last_value):
    self.node_id = node_id
    self.position = position
    self.last_value = 0
  
  def __repr__(self):
    return 'Sensor<id {} node{} position{}>'.format(self.id, self.node, self.position)



'''
id          - Integer
sensor_id   - ForeignKey(Node)
value       - Integer
timestamp   - DateTime
'''
class SenosrValue(db.Model):
  __tablename__ = 'sensorValue'

  id = Column(Integer, primary_key=True)
  sensor_id = db.Column(Integer, db.ForeignKey('sensor.id'))
  value = Column(Integer())
  timestamp = Column(DateTime(), default=datetime.utcnow)

  def __init__(self, sensor_id, value):
    self.sensor_id = sensor_id
    self.value = value
  
  def __repr__(self):
    return 'Reading<node{} position{} value{}>'.format(self.id, self.sensor.node, self.position, self.value)