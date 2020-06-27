from app.cache.cache_manager import CacheManager
from app.config import MAX_CLOSEST_BUCKET_DIFF, MEALS_PER_COMBO
from app.cache.exceptions import InvalidMealId
from app.data.models import UserCombos
from app.meals.exceptions import InvalidDay, InvalidMealCombo
from app.data.util import check_valid_day
from app.spoonacular.api import SpoonacularClient

class MealsManager(object):
    
    def __init__(self):

        self.cache_manager  = CacheManager()
        self.meals_provider = SpoonacularClient()

    def get_meals_suggestion(self, total_calories, day=None):

        if day and (check_valid_day(day) is False):
            raise InvalidDay

        calories_per_meal = total_calories // MEALS_PER_COMBO  #Distribute the calories equally
        nearest_bucket    = int(MAX_CLOSEST_BUCKET_DIFF * round(calories_per_meal/MAX_CLOSEST_BUCKET_DIFF)) # Find calorie bucket to MAX_CLOSEST_BUCKET_DIFF

        calories = nearest_bucket if nearest_bucket < calories_per_meal else nearest_bucket - MAX_CLOSEST_BUCKET_DIFF #Normalize

        if self.cache_manager.check_meals_available(calories=calories) is False:
            meals_data = self.meals_provider.get_recipies_by_nutrients(calories) # Fetch meals from provider
            self.cache_manager.add_meals_to_cache(calories, meals_data) # Cache meals

        meals = self.cache_manager.get_meals_from_cache(calories) # Get random meal combo
        return self.format_suggestion(meals)

    def get_meals_from_ids(self, meal_ids=[]):

        return self.cache_manager.get_meals_from_ids_cache(meal_ids)

    def confirm_meal_suggestion(self, user_id, day, calories, meal_ids):

        day_of_week = check_valid_day(day)
        if day_of_week is False:
            raise InvalidDay    

        meals = self.get_meals_from_ids(meal_ids)

        combo_calories = 0
        for meal in meals:
            combo_calories += meal['calories']
        if combo_calories > calories:
            raise InvalidMealCombo

        user_combo = UserCombos.save_or_update(user_id, day_of_week, meals)

        return self.format_suggestion(meals)

    def get_weekly_meal_plan(self, user_id):
            
        weekly_plan = UserCombos.get_weekly_plan(user_id)

        return weekly_plan

    def format_suggestion(self, meals):

        res = {'meals': [], 'total_calories' : 0}

        for meal in meals:
            res['meals'].append(meal)
            res['total_calories'] += meal['calories']
        
        return res
