class Config(object):
  DEBUG = True
  EDISON = False
  SECRET_KEY = 'this-really-needs-to-be-changed'
  SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/smartbed'

class EdisonProductionConfig(Config):
  DEBUG = False
  EDISON = True

class EdisonTestConfig(Config):
  DEBUG = True
  EDISON = True

class ClientProductionConfig(Config):
  DEBUG = False

class ClientTestConfig(Config):
  DEBUG = True