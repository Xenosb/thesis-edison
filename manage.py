from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import flask_app, db

flask_app.config.from_object('config.config_s')

migrate = Migrate(flask_app, db)
manager = Manager(flask_app)

manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()