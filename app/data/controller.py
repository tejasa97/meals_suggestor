from app.data import data_bp
from app.meals.exceptions import InvalidDay
from app.meals.meals_manager import MealsManager
from app.spoonacular.exceptions import InvalidApiKey, ServerError
from flask import Response, request, abort
import json

meals_manager = MealsManager()

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
    data     = json.loads(request.data)

    calories = data.get('calories', None)
    day      = data.get('day', None)

    if calories is None:
        abort(400, 'Calories data not provided')

    try:
        meals_suggestion = meals_manager.get_meals_suggestion(calories, day)
        
    except InvalidDay:
        abort(400, 'Invalid day provided')
    except InvalidApiKey:
        abort(400, 'Invalid Spoonacular API-KEY provided')
    except Exception as e:
        print("Exception occured")
        abort(500, str(e))

    return Response(json.dumps(meals_suggestion), 
        status=200, mimetype='application/json'
        )
