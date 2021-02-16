import os

SECRET_KEY = os.environ.get("SECRET_KEY")

# ????
# SQLALCHEMY_DATABASE_URI = 'postgres://....'
# # os.environ['DATABASE_URL']
# SQLALCHEMY_TRACK_MODIFICATIONS = False 

class Config(object):
    DEBUG = False
    TESTING = False
    DATABASE_URI = 'postgres://ndkkehfxwfrhwx:8e9dcf6bf7d646cfed08f429670580fd545233e6df9ea58ac35783963aaceb30@ec2-34-230-167-186.compute-1.amazonaws.com:5432/d620dgs57jjv59'


class ProductionConfig(Config):
    DATABASE_URI = 'mysql://user@localhost/foo'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True

