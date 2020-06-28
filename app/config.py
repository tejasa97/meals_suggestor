import os

MEALS_PER_COMBO         = 3
MAX_RESULTS             = 50
MAX_CLOSEST_BUCKET_DIFF = 25

POSTGRES_CONF = {
    'host'     : os.getenv('POSTGRES_HOST', 'localhost'),
    'port'     : int(os.getenv('POSTGRES_PORT', 6379)),
    'db'       : os.getenv('POSTGRES_DB', 'dev'),
    'user'     : os.getenv('POSTGRES_USER', 'postgres'),
    'password' : os.getenv('POSTGRES_PASSWORD', 'postgres')
}

REDIS_CONF = {
    'host' : os.getenv('REDIS_HOST'),
    'port' : int(os.getenv('REDIS_PORT'))
}

class Config(object):
    
    SECRET_KEY                     = os.urandom(30)
    SQLALCHEMY_DATABASE_URI        = f"postgres://{POSTGRES_CONF['user']}:{POSTGRES_CONF['password']}@{POSTGRES_CONF['host']}:{POSTGRES_CONF['port']}/{POSTGRES_CONF['db']}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

