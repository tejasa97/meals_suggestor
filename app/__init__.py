from app.config import Config
from dotenv import load_dotenv
from app.extensions import db, migrate
from flask import Flask, jsonify, make_response

def register_errorhandlers(app):
    """Register error handlers."""

    def render_error(error):
        """Render error template."""

        # If a HTTPException, pull the `code` attribute; default to 500
        error_code        = getattr(error, 'code', 500)
        error_description = getattr(error, 'name', '')
        error_message     = getattr(error, 'description', '')
        return make_response(jsonify(
            {
                'error'   : error_code,
                'message' : error_message
            }), error_code
        )

    for errcode in [400, 401, 403, 404, 405, 500]:
        app.errorhandler(errcode)(render_error)

def create_app(config_class=Config):
    
    load_dotenv() # Load all env variables for the app
    app = Flask(__name__)

    app.secret_key = "lsgab7sfgd"
    app.config.from_object(config_class)

    db.init_app(app)

    # Uncomment when creating the tables
    """
    with app.app_context():
        print("Creating all tables")
        db.create_all()
    """
    # Uncomment whenever migration is to be done
    """ 
    migrate.init_app(app, db) 
    """
    
    from app.data import data_bp
    app.register_blueprint(data_bp, cli_group=None)

    register_errorhandlers(app)

    return app
