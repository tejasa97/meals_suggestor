from app.config import REDIS_CONF
from app.cache.exceptions import RedisKeyError
import pickle
import redis

class Redis(object):
    
    def __init__(self):
    
        self.redis = redis.Redis(host=REDIS_CONF['host'], port=REDIS_CONF['port'])

    def check_key_exists(self, key):

        if not isinstance(key, str):
            key = str(key)

        return bool(self.redis.exists(key))

    def get_key(self, key):
    
        if not isinstance(key, str):
            key = str(key)
           
        return self.redis.get(key)

    def set_key(self, key, value):

        if not isinstance(key, str):
            key = str(key)

        return self.redis.set(key, value)

    def set_keys(self, objects):
    
        pipe = self.redis.pipeline()

        for key, value in objects.items():
            pipe.execute_command('set', key, pickle.dumps(value))

        pipe.execute()

    def save_list(self, key, list_):

        if not isinstance(key, str):
            key = str(key)

        self.redis.rpush(key, *list_)
    
    def get_from_list(self, key, indices=[]):

        if not isinstance(key, str):
            key = str(key)

        pipe = self.redis.pipeline()
        for idx in indices:
            pipe.execute_command('lindex', key, idx)

        res = pipe.execute()

        return res

    def get_multiple_keys(self, keys=[]):

        res = []
        for key in keys:
            redis_value = self.redis.get(key)

            if redis_value is None:
                raise RedisKeyError

            obj = pickle.loads(redis_value)
            obj.update({'meal_id' : int(key)})
            res.append(obj)
            
        return res
