from flask import render_template, jsonify, request, abort, Response
from app import flask_app
from models import *
from datetime import timedelta

# Error handlers
@flask_app.errorhandler(404)
def page_not_found(e):
  return flask_app.send_static_file('404.html')


# Frontend routes
@flask_app.route('/')
@flask_app.route('/index')
def index():
  active_nodes = 0
  active_sensors = 0

  for node in Node.query.all():
    inactivity = datetime.now() - timedelta(minutes=2)

    if node.last_update > inactivity:
      active_nodes+=1
    for sensor in node.sensors:
      if sensor.last_update > inactivity:
        active_sensors+=1

  edison = flask_app.config['EDISON']

  return render_template('index.html', \
    active_nodes=active_nodes, active_sensors=active_sensors, edison=edison)

@flask_app.route('/all_nodes')
def all_nodes():
  return render_template('all_nodes.html', nodes=Node.query.all())

@flask_app.route('/node')
def node():
  if 'id' in request.args:
    nodes = Node.query.all()
    node = Node.query.filter_by(id = request.args['id']).first()
    return render_template('node.html', nodes=nodes, node=node)

@flask_app.route('/sleep_monitor')
def sleep_monitor():
  return render_template('sleep_monitor.html')

@flask_app.route('/settings')
def settings():
  return render_template('settings.html')

@flask_app.route('/about')
def about():
  return render_template('about.html')


# API routes
@flask_app.route('/api/system')
def api_system():
  all_nodes = Node.query.all()
  sys = System()
  for node in all_nodes:
    sys.add_node(node)
  return jsonify(sys.serialize())

@flask_app.route('/api/service')
def api_service():
  from app import reader
  return jsonify({'result': reader.active.value})

@flask_app.route('/api/service/stop')
def api_service_stop():
  from app import reader, parent_pipe
  if reader.active.value:
    parent_pipe.send('stop')
    return jsonify({'result': 'success'})
  return jsonify({'result': 'failed'})

@flask_app.route('/api/service/start')
def api_service_start():
  from app import reader, parent_pipe
  if not reader.active.value:
    parent_pipe.send('start')
    return jsonify({'result': 'success'})
  return jsonify({'result': 'failed'})

@flask_app.route('/api/node')
def api_node():
  args = request.args
  if 'id' in args:
    r_node_id = args.get('id', 0, type=int)

    if 'readings' in args:
      r_node_readings = args.get('readings', 0, type=int)
      return jsonify(result=r_node_readings)

    else:
      try:
        return jsonify(result=Node.query.filter_by(id=int(r_node_id)).first().serialize())
      except AttributeError:
        return jsonify(result='unknown node id')
    
  return jsonify({})

@flask_app.route('/api/sensor')
def api_sensor():
  args = request.args
  if 'id' in args:
    r_sensor_id = args.get('id', 0, type=int)

    try:
      result = Sensor.query.filter_by(id=int(r_sensor_id)).first().serialize()
      return jsonify(result=result)
    except:
      return jsonify(result='unknown sensor id')


@flask_app.route('/api/sensor_value')
def api_sensor_value():
  args = request.args
  if 'id' in args:
    r_sensor_id = args.get('id', 0, type=int)

    try:
      result = SensorValue.query.filter(SensorValue.sensor_id == r_sensor_id)
      result.first().serialize()
    except:
      return jsonify(result='unknown sensor id')

    values = {}

    if 'start' in args:
      r_start_readings = args.get('start', 0, type=int)
      result = result.filter(SensorValue.timestamp >= r_start_readings)
    
    if 'end' in args:
      r_end_readings = args.get('end', 0, type=int)
      result = result.filter(SensorValue.timestamp <= r_end_readings)
    
    result = result.all()

    if 'readings' in args:
      r_sensor_readings = args.get('readings', 0, type=int)
      result = result[-r_sensor_readings:]

    for reading in result:
      values[reading.timestamp.strftime('%Y-%m-%d-%H-%M-%S')] = reading.value
  
  return jsonify(result = values)

@flask_app.route('/api/chart/histogram')
def api_charts_histogram():
  result = {}
  nodes = Node.query.filter(Node.last_update > datetime.utcnow() - timedelta(minutes=2)).all()
  for node in nodes:
    for sensor in node.sensors:
      result[sensor.id] = sensor.last_value
  return jsonify(result=result)