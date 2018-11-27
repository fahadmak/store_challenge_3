from flask import Blueprint, jsonify, request, current_app as app
from flask_jwt_extended import jwt_required, get_jwt_identity
from cerberus import Validator

from app.error_handler import InvalidUsage

from app.models.database import Database
from app.validation_schema import category_schema


category = Blueprint("category", __name__)

v = Validator()


@category.route("/api/v1/categories", methods=["POST"])
@jwt_required
def create_category():
    """A method adds product instance to products list"""
    if request.content_type != "application/json":
        raise InvalidUsage("Invalid content type", 400)

    db = Database(app.config['DATABASE_URI'])
    current_user_id = get_jwt_identity()
    user = db.find_user_by_id(current_user_id)
    if user.is_admin is False:
        raise InvalidUsage("you do not have admin rights", 401)

    data = request.json
    name = data.get("category_name")
    validate = v.validate(data, category_schema)
    if not validate:
        raise InvalidUsage({'error': v.errors}, 400)

    found = db.find_category_by_category_name(name)
    if found:
        raise InvalidUsage(f"{found.category_name} already exists", 400)
    db.add_category(name, current_user_id)
    return jsonify({'message': f'{name} has successfully been added to categories'}), 201


@category.route("/api/v1/categories/<int:category_id>", methods=["PUT"])
@jwt_required
def modify_category(category_id):
    """A method adds product instance to products list"""

    if request.content_type != "application/json":
        raise InvalidUsage("Invalid content type", 400)

    db = Database(app.config['DATABASE_URI'])

    current_user_id = get_jwt_identity()
    user = db.find_user_by_id(current_user_id)
    if user.is_admin is False:
        raise InvalidUsage("you do not have admin rights", 401)

    data = request.json
    name = data.get("category_name")

    validate = v.validate(data, category_schema)
    if not validate:
        raise InvalidUsage({'error': v.errors}, 400)

    found = db.find_category_by_category_id(category_id)
    if not found:
        raise InvalidUsage(f"category does not exist", 404)

    found_name = db.find_category_by_category_name(name)
    if found_name:
        raise InvalidUsage(f"{found_name.category_name} name already exists", 400)

    db.modify_category(name, category_id)

    return jsonify({'message': f'{name} has successfully been modified'}), 200


@category.route("/api/v1/categories/<int:category_id>", methods=["DELETE"])
@jwt_required
def delete_category(category_id):
    """A method adds product instance to products list"""

    if request.content_type != "application/json":
        raise InvalidUsage("Invalid content type", 400)

    db = Database(app.config['DATABASE_URI'])

    current_user_id = get_jwt_identity()
    user = db.find_user_by_id(current_user_id)
    if user.is_admin is False:
        raise InvalidUsage("you do not have admin rights", 401)

    found = db.find_category_by_category_id(category_id)
    if not found:
        raise InvalidUsage("Category does not exist", 404)

    db.delete_category(category_id)

    return jsonify({'message': f'{found.category_name} has been deleted'}), 200


@category.route("/api/v1/categories/<int:category_id>", methods=["GET"])
@jwt_required
def get_category(category_id):
    """A method adds product instance to products list"""

    if request.content_type != "application/json":
        raise InvalidUsage("Invalid content type", 400)

    db = Database(app.config['DATABASE_URI'])

    found = db.find_category_by_category_id(category_id)
    if not found:
        raise InvalidUsage("Category does not exist", 404)

    return jsonify(found.to_json()), 200


@category.route("/api/v1/categories", methods=["GET"])
@jwt_required
def get_all_category():
    """A method adds product instance to products list"""

    if request.content_type != "application/json":
        raise InvalidUsage("Invalid content type", 400)

    db = Database(app.config['DATABASE_URI'])

    found = db.get_all_categories()
    if not found:
        raise InvalidUsage("No categories does not exist", 404)

    return jsonify({"categories": found}), 200


@category.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

