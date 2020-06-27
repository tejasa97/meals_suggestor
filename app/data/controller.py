from app.data import data_bp
from app.cache.exceptions import InvalidMealId
from app.meals.exceptions import InvalidDay, InvalidMealCombo
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

@data_bp.route("/get_meals_suggestion", methods=['GET'])
def get_meals_suggestion():
        
    calories = request.args.get('calories', None)
    day      = request.args.get('day', None)

    if calories is None:
        abort(400, 'Calories data not provided')

    try:
        meals_suggestion = meals_manager.get_meals_suggestion(int(calories), day)
        
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

@data_bp.route("/meals/confirm_suggestion", methods=['POST'])
def confirm_meals_suggestion():
        
    response = {}
    data     = json.loads(request.data)

    calories = data.get('calories', None)
    day      = data.get('day', None)
    meal_ids = data.get('meal_ids', None)

    try:
        combo_data = meals_manager.confirm_meal_suggestion(1, day, calories, meal_ids)
    except InvalidMealCombo:
        abort(400, 'Invalid Meal Combo provided')
    except InvalidMealId:
        abort(400, 'Invalid Meal ID(s) provided')

    response = {'status' : 'success'}

    return Response(json.dumps(combo_data), 
        status=201, mimetype='application/json'
        )

@data_bp.route("/meals/weekly_plan", methods=['GET'])
def get_weekly_plan():
        
    weekly_plan = meals_manager.get_weekly_meal_plan(user_id=1)

    return Response(json.dumps(weekly_plan), 
        status=200, mimetype='application/json'
        )
    