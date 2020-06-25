from app.data import data_bp
from app.spoonacular.api import Spoonacular
from app.cache.cache_manager import CacheManager
from flask import Response, request, abort
import json

spoonacular_client = Spoonacular()
cache_manager = CacheManager()

@data_bp.route("/")
def ping():
        
    return Response(json.dumps({
        "v" : "0.1"
    }), 
        status=200, mimetype='application/json'
    )

@data_bp.route("/get_meals_suggestion", methods=['POST'])
def get_meals_suggestion():
        
    response = {}
    data = json.loads(request.data)

    calories = data.get('calories', None)

    if calories is None:
        abort(400, 'Calories data not provided')

    if cache_manager.check_meals_available(calories=calories) is False:
        
        meals_data = spoonacular_client.get_recipies_by_nutrients(calories)
        cache_manager.add_meals_to_cache(calories, meals_data)
    
    meals = cache_manager.get_meals_from_cache(calories)

    return Response(json.dumps(meals), 
        status=200, mimetype='application/json'
        )
