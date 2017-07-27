from flask import render_template, jsonify, request, abort, Response
from app import flask_app
from models import *

# Error handlers
@flask_app.errorhandler(404)
def page_not_found(e):
  return flask_app.send_static_file('404.html')


# Frontend routes
@flask_app.route('/')
@flask_app.route('/index')
def index():
  return render_template('index.html')

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
  if 'id'
  r_node_id = request.args.get('id', 0, type=int)
  return jsonify(result=Node.query.filter_by(id=int(r_node_id)).first().serialize())

@flask_app.route('/api/sensor')
def api_sensor():
  r_sensor_id = request.args.get('id', 0, type=int)
  try:
    return jsonify(result=Sensor.query.filter_by(id=int(r_sensor_id)).first().serialize())
  except:
    return 'Sensor not available'
