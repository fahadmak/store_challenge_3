from flask import Flask
from flask_jwt_extended import JWTManager
from config import app_config


def create_app(config_name):
    """create flask application and set dev environment"""
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    jwt = JWTManager(app)
    from app.views.user import user as user_blueprint

    app.register_blueprint(user_blueprint)

    return app


app = create_app("development")
