from flask import Blueprint, jsonify, request

from app.error_handler import InvalidUsage
from app.validate import validate_user, empty
from app.models.database import Database
from flask import current_app as app


user = Blueprint("user", __name__)


@user.route("/api/v1/auth/signup", methods=["POST"])
def create_user():
    """A method adds product instance to products list"""
    db = Database(app.config['DATABASE_URI'])
    data = request.json
    name = data.get("name")
    username = data.get("username")
    password = data.get("password")
    db.create_user(name, username, password)
    return jsonify({'message': f'{username} has successfully been added to staff'}), 200

