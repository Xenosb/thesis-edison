from flask import Flask
from flask_sqlalchemy import SQLAlchemy

flask_app = Flask(__name__, instance_relative_config=True)

# Set environment
flask_app.config.from_object('config.ClientTestConfig')

# Configure db and models
flask_app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(flask_app)
#from models import Node, Sensor, SensorValue

# Load views
from app import views


# Rock n' roll
if __name__ == '__main__':
  flask_app.run(host='0.0.0.0', debug='True')