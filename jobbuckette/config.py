import os

class DevelopmentConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://thinkful:thinkful@localhost:5432/jobbuckette"
    DEBUG = True

class TestingConfig(object):
    SQLALCHEMY_DATABASE_URI = "postgresql://thinkful:thinkful@localhost:5432/jobbuckette-test"
    DEBUG = False
    SECRET_KEY = "Not secret"
