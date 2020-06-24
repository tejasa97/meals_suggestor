from app.data import data_bp
from app.spoonacular.api import Spoonacular
from flask import Response
import json

spoonacular_client = Spoonacular()

@data_bp.route("/")
def ping():
        
    return Response(json.dumps({
        "v" : "0.1"
    }), 
        status=200, mimetype='application/json'
    )
