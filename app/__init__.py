from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, instance_relative_config=True)
from app import views

# Set environment
app.config.from_object('config.ClientTestConfig')


# Configure db and models
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
from models import *


# Rock n' roll
if __name__ == '__main__':
  app.run(host='0.0.0.0', debug='True')