import os

class Config(object):

    SECRET_KEY                     = os.urandom(30)
    SQLALCHEMY_DATABASE_URI        = 'postgres://postgres:postgres@localhost:5432/dev'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
