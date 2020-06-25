from dotenv import load_dotenv
import os

load_dotenv()  # Load all env variables for the app

MEALS_PER_COMBO    = 3
MAX_RESULTS        = 50

class Config(object):

    SECRET_KEY                     = os.urandom(30)
    SQLALCHEMY_DATABASE_URI        = 'postgres://postgres:postgres@localhost:5432/dev'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

REDIS_CONF = {
    'host' : os.getenv('REDIS_HOST'),
    'port' : int(os.getenv('REDIS_PORT'))
}
