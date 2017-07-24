from flask import render_template, jsonify, request, abort
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


# API
@flask_app.route('/api/node')
def api_node():
  #r_node_id = request.args.get('id', 0, type=int)
  #r_node_id = request.args.get('id', 0)
  #return jsonify(result=Node.query.filter_by(id=int(r_node_id)).first().serialize())
  #return "%i" % t_add.AsyncResult(r_node_id).get()
  return 'a'

@flask_app.route('/api/sensor')
def api_sensor():
  r_sensor_id = request.args.get('id', 0, type=int)
  try:
    return jsonify(result=Sensor.query.filter_by(id=int(r_sensor_id)).first().serialize())
  except:
    return 'Sensor not available'