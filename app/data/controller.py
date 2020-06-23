from app.data import data_bp
from flask import Response
import json

@data_bp.route("/")
def ping():

    return Response(json.dumps({
        "v" : "0.1"
    }), 
        status=200, mimetype='application/json'
    )
