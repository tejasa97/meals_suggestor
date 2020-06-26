from app.cache.cache_manager import CacheManager
from app.config import MAX_CLOSEST_BUCKET_DIFF
from app.meals.exceptions import InvalidDay
from app.meals.util import DAYS_OF_WEEK
from app.spoonacular.api import Spoonacular

class MealsManager(object):
    
    def __init__(self):

        self.cache_manager  = CacheManager()
        self.meals_provider = Spoonacular()

    def get_meals_suggestion(self, total_calories, day=None):

        if day is not None and day not in DAYS_OF_WEEK:
            raise InvalidDay(f"Invalid day '{day}' provided")

        calories_per_meal = total_calories // 3  #Distribute the calories equally
        nearest_bucket    = int(MAX_CLOSEST_BUCKET_DIFF * round(calories_per_meal/MAX_CLOSEST_BUCKET_DIFF)) # Find calorie bucket to MAX_CLOSEST_BUCKET_DIFF

        calories = nearest_bucket if nearest_bucket < calories_per_meal else nearest_bucket - MAX_CLOSEST_BUCKET_DIFF #Normalize

        if self.cache_manager.check_meals_available(calories=calories) is False:
            print(f"Adding meals with calories {calories} to cache..")
            meals_data = self.meals_provider.get_recipies_by_nutrients(calories) # Fetch meals from provider
            self.cache_manager.add_meals_to_cache(calories, meals_data) # Cache meals

        print(f"Fetching from `{calories}` calories bucket")
        meals            = self.cache_manager.get_meals_from_cache(calories) # Get random meal combo
        meals_suggestion = self.format_suggestion(meals)

        return meals_suggestion

    def confirm_meal_suggestion(self, day, meal_ids):

        raise NotImplementedError

    def get_weekly_meal_plan(self):
            
        raise NotImplementedError

    def format_suggestion(self, meals):

        res = {
            'meals'          : [],
            'total_calories' : 0
        }

        for meal in meals:
            res['meals'].append(meal)
            res['total_calories'] += meal['calories']
        
        return res
