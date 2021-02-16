import os

SECRET_KEY = os.environ.get("SECRET_KEY")

# SQLALCHEMY_DATABASE_URI = 'postgres://....'
# # os.environ['DATABASE_URL']
# SQLALCHEMY_TRACK_MODIFICATIONS = False 

class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'sqlite:///:memory:'


class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

