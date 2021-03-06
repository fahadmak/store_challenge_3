from flask import Blueprint, jsonify, request
from cerberus import Validator
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from passlib.hash import pbkdf2_sha256 as sha256
from datetime import timedelta
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
    if request.content_type != "application/json":
        raise InvalidUsage("Invalid content type", 400)

    db = Database(app.config['DATABASE_URI'])

    current_user_id = get_jwt_identity()
    user = db.find_user_by_id(current_user_id)
    if user.is_admin is False:
        raise InvalidUsage("you do not have admin rights", 401)

    data = request.json
    admin = data.get("is_admin")
    if not isinstance(admin, bool):
        raise InvalidUsage("Input should be set to boolean value", 400)

    attendant = db.find_user_by_id(user_id)
    if not attendant:
        raise InvalidUsage("User does not exist", 404)

    db.modify_admin_rights(user_id, admin)
    return jsonify({'message': f'{attendant.username} is now an admin {admin}'}), 200


@user.route("/api/v1/auth/signup", methods=["POST"])
@jwt_required
def create_user():
    """A method adds product instance to products list"""
    if request.content_type != "application/json":
        raise InvalidUsage("Invalid content type", 400)

    current_user_id = get_jwt_identity()

    db = Database(app.config['DATABASE_URI'])

    user = db.find_user_by_id(current_user_id)
    if user.is_admin is False:
        raise InvalidUsage("you do not have admin rights", 401)

    data = request.json
    name = data.get("name")
    username = data.get("username")
    password = data.get("password")

    validate = v.validate(data, user_schema)
    if not validate:
        raise InvalidUsage(v.errors, 400)

    found = db.find_user_by_username(username)
    if found:
        raise InvalidUsage(f"{username} already exists", 400)

    hash_password = sha256.hash(password)

    db.create_user(name, username, hash_password)

    return jsonify({'message': f'{username} has successfully been added to staff'}), 201


@user.route("/api/v1/auth/login", methods=["POST"])
def login_user():
    """Endpoint logs in user"""

    if request.content_type != "application/json":
        raise InvalidUsage("Invalid content type", 400)

    data = request.json
    username = data.get("username")
    password = data.get("password")

    validate = v.validate(data, login_schema)
    if not validate:
        return jsonify(v.errors), 400

    db = Database(app.config['DATABASE_URI'])
    found = db.find_user_by_username(username)
    if not found:
        raise InvalidUsage('Username and password did not match', 400)

    if not sha256.verify(password, found.password):
        raise InvalidUsage('Username and password did not match', 400)

    user_id = found.user_id
    status = found.is_admin

    access_token = create_access_token(identity=user_id, expires_delta=timedelta(hours=3))
    return jsonify(access_token=access_token, message="login successful", admin=status, user_id=user_id), 200


@user.route("/api/v1/auth/users", methods=["GET"])
@jwt_required
def get_users():
    """A method gets all users"""
    if request.content_type != 'application/json':
        raise InvalidUsage("Invalid content type", 400)

    current_user_id = get_jwt_identity()

    db = Database(app.config['DATABASE_URI'])

    user = db.find_user_by_id(current_user_id)

    if user.is_admin is False:
        raise InvalidUsage("you do not have admin rights", 401)

    users = db.get_all_users()
    if not users:
        raise InvalidUsage("They are currently no users")

    return jsonify({'users': users}), 200


@user.route("/api/v1/auth/users/<int:user_id>", methods=["DELETE"])
@jwt_required
def delete_user(user_id):
    """A method deletes product stored in the database"""
    if request.content_type != "application/json":
        raise InvalidUsage("Invalid content type", 400)

    db = Database(app.config['DATABASE_URI'])

    current_user_id = get_jwt_identity()
    user = db.find_user_by_id(current_user_id)
    if not user.is_admin:
        raise InvalidUsage("you do not have admin rights", 401)

    item = db.find_user_by_id(user_id)
    if not item:
        raise InvalidUsage("user does not exist", 404)

    user_name, user_id = item.username, item.user_id
    db.delete_user(user_id)
    return jsonify({'message': f'{user_name} has been deleted'}), 200


@user.route("/api/v1/users/<int:user_id>", methods=["GET"])
@jwt_required
def get_user_by_user_id(user_id):
    """A method adds product instance to products list"""

    if request.content_type != "application/json":
        raise InvalidUsage("Invalid content type", 400)

    db = Database(app.config['DATABASE_URI'])

    found_user = db.find_user_by_id(user_id)
    if not found_user:
        raise InvalidUsage("user does not exist", 400)
    return jsonify({'user': found_user.to_json()}), 200


@user.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


