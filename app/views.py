from flask import render_template, jsonify, request, abort, Response
from app import flask_app
from models import *
from datetime import timedelta
from math import floor

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

  nodes = Node.query.all()

  return render_template('index.html', \
    nodes=nodes, active_nodes=active_nodes, \
    active_sensors=active_sensors, edison=edison)

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
  return render_template('sleep_monitor.html', nodes=Node.query.all())

@flask_app.route('/settings')
def settings():
  return render_template('settings.html', nodes=Node.query.all())

@flask_app.route('/about')
def about():
  return render_template('about.html', nodes=Node.query.all())


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
  return jsonify({ 'result': reader.active.value == 1 })

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
  if reader.active.value == 0:
    parent_pipe.send('start')
    return jsonify({'result': 'success'})
  return jsonify({'result': 'failed'})

@flask_app.route('/api/node')
def api_node():
  args = request.args
  if 'id' in args:
    r_node_id = args.get('id', 0, type=int)

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

    if Sensor.query.filter_by(id=r_sensor_id).count() == 0:
      return jsonify(result='unknown sensor id')

    result = Sensor.query.filter_by(id=int(r_sensor_id)).first().serialize()
    return jsonify(result=result)

  else:
    return jsonify(result='sensor id not provided')

@flask_app.route('/api/sensor_value')
def api_sensor_value():
  args = request.args
  if 'id' in args:
    r_sensor_id = args.get('id', 0, type=int)

    if Sensor.query.filter_by(id=r_sensor_id).count() == 0:
      return jsonify(result='unknown sensor id')

    values = {}
    result = SensorValue.query.filter(SensorValue.sensor_id == r_sensor_id)

    if 'start' in args:
      r_start_readings = args.get('start', 0, type=str)
      print r_start_readings
      result = result.filter(SensorValue.timestamp >= r_start_readings)
    
    if 'end' in args:
      r_end_readings = args.get('end', 0, type=str)
      result = result.filter(SensorValue.timestamp <= r_end_readings)
    
    result = result.all()

    if 'readings' in args:
      r_sensor_readings = args.get('readings', 0, type=int)
      result = result[-r_sensor_readings:]

    for reading in result:
      values[reading.timestamp.strftime('%Y-%m-%d-%H-%M-%S')] = reading.value
  
  return jsonify(result = values)


# API routes for charts
@flask_app.route('/api/chart/histogram')
def api_chart_histogram():
  result = {}
  nodes = Node.query.all()
  for node in nodes:
    for sensor in node.sensors:
      result[sensor.id] = sensor.last_value
  return jsonify(result=result)

@flask_app.route('/api/chart/heatmap')
def api_chart_heatmap():
  # result = [[1409,  2309,   5102,   373,    1268,   2954,   6042,  1008], \
  #           [1120,  14120,  12420,  8120,   9520,   11820,  8120,  1420], \
  #           [18285, 42567,  44567,  32567,  40567,  44567,  19567, 16567], \
  #           [25567, 45567,  47567,  38567,  41567,  43567,  21567, 19567], \
  #           [21849, 32849,  33849,  28849,  35849,  35849,  16849, 12849], \
  #           [1317,  2217,   2017,   1997,   1417,   1397,   2017,  1837], \
  #           [794,   1294,   8794,   1794,   1294,   2594,   1294,  1194], \
  #           [863,   1363,    763,    893,   1963,   663,    2063,   583], \
  # ]
  # return jsonify(result=result)
  nodes = Node.query.all()
  result = []
  for node in nodes:
    tmp0 = []
    tmp1 = []
    sensors = node.sensors.all()
    for i in range(len(sensors)/2):
      tmp0.append(sensors[i].last_value)
      tmp1.append(sensors[8+i].last_value)
    result.append(tmp0)
    result.append(tmp1)
  return jsonify(result=result)

@flask_app.route('/api/chart/node')
def api_chart_sensors():
  if not 'id' in request.args:
    return jsonify(result='node id not provided')

  if 'len' in request.args:
    length = request.args.get('len', 0, type=int)
  else:
    length = 20

  r_node_id = request.args.get('id', 0, type=int)
  if Node.query.filter_by(id=r_node_id).count() == 0:
    return jsonify(result='unknown node id')

  result = {}
  for sensor in Sensor.query.filter(Sensor.node_id == r_node_id).all():
    values = SensorValue.query.filter(SensorValue.sensor_id == sensor.id).order_by(-SensorValue.timestamp).limit(length).all()
    result[sensor.position] = []
    for i in range(length):
      result[sensor.position] += [values[i].value]

  return jsonify(result)