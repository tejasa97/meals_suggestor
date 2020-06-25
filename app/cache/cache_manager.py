from app.cache.redis_cache import Redis
from app.config import MEALS_PER_COMBO, MAX_CACHED_RESULTS
from six.moves import range as xrange
import random

class CacheManager(object):

    def __init__(self):

        self.cache = Redis()

    def add_meals_to_cache(self, calories, meals):

        meal_ids     = []
        meal_objects = {}

        for meal in meals:
            meal_ids.append(meal['id'])
            meal_objects[meal['id']] = {
                'name'     : meal['title'],
                'calories' : meal['calories']
            }

        self.cache.save_list(f'calories_{calories}', meal_ids)
        self.cache.set_keys(meal_objects)

    def get_meals_from_cache(self, calories, number_of_meals=MEALS_PER_COMBO):
    
        meal_ids = self.get_meal_ids_from_cache(calories, number_of_meals)

        return self.get_meals_from_ids_cache(meal_ids)

    def get_meal_ids_from_cache(self, calories, number_of_meals):

        random_meal_idxs = random.sample(xrange(1, MAX_CACHED_RESULTS), number_of_meals)

        return self.cache.get_from_list(f'calories_{calories}', random_meal_idxs)

    def get_meals_from_ids_cache(self, meal_ids=[]):

        return self.cache.get_multiple_keys(meal_ids)

    def check_meals_available(self, calories):
    
        return self.cache.check_key_exists(f'calories_{calories}')
