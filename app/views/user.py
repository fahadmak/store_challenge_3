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
    if request.content_type != "application/json":
        raise InvalidUsage("Invalid content type", 400)
    data = request.json
    name = data.get("name")
    username = data.get("username")
    password = data.get("password")
    check = empty(name, username, password)
    if check:
        raise InvalidUsage(check, 400)
    invalid = validate_user(name, username, password)
    if invalid:
        raise InvalidUsage(invalid, 400)
    found = db.find('users', 'username', username)
    if found:
        raise InvalidUsage(f"{username} already exists", 400)
    db.create_user(name, username, password)
    return jsonify({'message': f'{username} has successfully been added to staff'}), 200


@user.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response