from flask import Blueprint, jsonify, request
from cerberus import Validator
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity

from app.error_handler import InvalidUsage
from app.models.database import Database
from flask import current_app as app
from app.validation_schema import user_schema, login_schema

user = Blueprint("user", __name__)

v = Validator()


@user.route("/api/v1/auth/promote/<user_id>", methods=["PUT"])
@jwt_required
def give_admin_rights(user_id):
    """A method adds product instance to products list"""
    db = Database(app.config['DATABASE_URI'])
    if request.content_type != "application/json":
        raise InvalidUsage("Invalid content type", 400)
    current_user_id = get_jwt_identity()
    user = db.find_user_by_id(current_user_id)
    if user.is_admin is False:
        raise InvalidUsage("you do not have admin rights", 403)
    attendant = db.find_user_by_id(user_id)
    if not attendant:
        raise InvalidUsage("User does not exist", 404)
    if attendant.is_admin is True:
        raise InvalidUsage("you already have admin rights", 400)
    db.modify_admin_rights(user_id)
    return jsonify({'message': f'{attendant.username} is now an admin'}), 200


@user.route("/api/v1/auth/signup", methods=["POST"])
@jwt_required
def create_user():
    """A method adds product instance to products list"""
    db = Database(app.config['DATABASE_URI'])
    if request.content_type != "application/json":
        raise InvalidUsage("Invalid content type", 400)
    data = request.json
    name = data.get("name")
    username = data.get("username")
    password = data.get("password")
    validate = v.validate(data, user_schema)
    if not validate:
        raise InvalidUsage({'error': v.errors}, 400)
    current_user_id = get_jwt_identity()
    user = db.find_user_by_id(current_user_id)
    if user.is_admin is False:
        raise InvalidUsage("you do not have admin rights", 403)
    found = db.find_user_by_username(username)
    if found:
        raise InvalidUsage(f"{username} already exists", 400)
    db.create_user(name, username, password)
    return jsonify({'message': f'{username} has successfully been added to staff'}), 201


@user.route("/api/v1/auth/login", methods=["POST"])
def login_user():
    """A method adds product instance to products list"""
    db = Database(app.config['DATABASE_URI'])
    if request.content_type != "application/json":
        raise InvalidUsage("Invalid content type", 400)
    data = request.json
    username = data.get("username")
    password = data.get("password")
    validate = v.validate(data, login_schema)
    if not validate:
        raise InvalidUsage({'error': v.errors}, 400)
    found = db.find_user_by_username(username)
    if not found:
        raise InvalidUsage(f"{username} doesn't exist", 400)
    user_id = found.user_id
    if password == found.password:
        access_token = create_access_token(identity=user_id)
        return jsonify(access_token=access_token, message="login successful"), 200
    return jsonify({'error': 'Username and password did not match'}), 400


@user.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response