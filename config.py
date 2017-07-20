class Config(object):
  DEBUG = True
  EDISON = False
  SECRET_KEY = 'this-really-needs-to-be-changed'
  SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/smartbed'
  REDIS_URL = "redis://localhost:6379/0"
  CELERY_BROKER_URL = 'redis://localhost:6379/0'
  CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
  UPDATE_FREQ = 0.1

class EdisonProductionConfig(Config):
  DEBUG = False
  EDISON = True

class EdisonTestConfig(Config):
  DEBUG = True
  EDISON = True

class ClientProductionConfig(Config):
  DEBUG = False
  EDISON = False
  SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/smartbed-prod'

class ClientTestConfig(Config):
  DEBUG = True
  EDISON = False
  SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/smartbed-test'

config_s = ClientTestConfig