class Config(object):
  DEBUG = True
  EDISON = False
  SECRET_KEY = 'this-really-needs-to-be-changed'
  SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/smartbed-test'
  UPDATE_FREQ = 0.1

class EdisonProductionConfig(Config):
  DEBUG = True
  EDISON = True
  SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/smartbed-prod'

class EdisonTestConfig(Config):
  DEBUG = True
  EDISON = True

class ClientTestConfig(Config):
  DEBUG = True
  EDISON = False

config_s = EdisonTestConfig
#config_s = ClientTestConfig
