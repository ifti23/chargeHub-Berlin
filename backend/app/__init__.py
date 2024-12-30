from flask import Flask

# from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


# db = SQLAlchemy()


def create_app():
    """Creates the flask application"""
    app = Flask(__name__)
    app.config.from_object("config.Config")
    CORS(app)

    # db.init_app(app) # maybe we add a database in the backend

    # import Blueprints
    from app.routes.search_for_charging_station import search_station_plz
    from app.routes.users import get_users
    from app.routes.home import home_message

    # Register Blueprints
    app.register_blueprint(search_station_plz, url_prefix="/api/search")
    app.register_blueprint(get_users, url_prefix="/api/users")
    app.register_blueprint(home_message, url_prefix="/")

    return app
