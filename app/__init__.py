from flask import Flask
from flask_jwt_extended import JWTManager
from config import app_config


def create_app(config_name):
    """create flask application and set dev environment"""
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    jwt = JWTManager(app)

    from app.views.user import user as user_blueprint
    from app.views.category import category as category_blueprint
    from app.views.product import product as product_blueprint
    from app.views.sale import sale as sale_blueprint

    app.register_blueprint(user_blueprint)
    app.register_blueprint(category_blueprint)
    app.register_blueprint(product_blueprint)
    app.register_blueprint(sale_blueprint)

    return app


app = create_app("development")
