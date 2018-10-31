from flask import Blueprint, jsonify, request, current_app as app
from flask_jwt_extended import jwt_required, get_jwt_identity
from cerberus import Validator

from app.error_handler import InvalidUsage
from app.models.database import Database
from app.validation_schema import product_schema

product = Blueprint("product", __name__)

v = Validator()


@product.route("/api/v1/categories/<int:category_id>/products", methods=["POST"])
@jwt_required
def create_product(category_id):
    """A method adds product instance to products list"""
    db = Database(app.config['DATABASE_URI'])
    if request.content_type != "application/json":
        raise InvalidUsage("Invalid content type", 400)
    data = request.json
    name = data.get("product_name")
    price = data.get("product_price")
    quantity = data.get("quantity")
    current_user_id = get_jwt_identity()
    user = db.find_user_by_id(current_user_id)
    if user.is_admin is False:
        raise InvalidUsage("you do not have admin rights", 403)
    validate = v.validate(data, product_schema)
    if not validate:
        raise InvalidUsage({'error': v.errors}, 400)
    category = db.find_category_by_category_id(category_id)
    if not category:
        raise InvalidUsage("category does not exist", 404)
    found = db.find_product_by_product_name(name)
    if found:
        raise InvalidUsage(f"{found.product_name} already exists", 400)
    db.add_product(name, quantity, price, current_user_id, category_id)
    return jsonify({'message': f'{name}'
                               f' has successfully been added to inventories'}), 201


@product.route("/api/v1/categories/<int:category_id>/products/<int:product_id>", methods=["PUT"])
@jwt_required
def modify_product(category_id, product_id):
    """A method adds product instance to products list"""
    db = Database(app.config['DATABASE_URI'])
    if request.content_type != "application/json":
        raise InvalidUsage("Invalid content type", 400)
    current_user_id = get_jwt_identity()
    user = db.find_user_by_id(current_user_id)
    if user.is_admin is False:
        raise InvalidUsage("you do not have admin rights", 403)
    data = request.json
    name = data.get("product_name")
    price = data.get("product_price")
    quantity = data.get("quantity")
    category = db.find_category_by_category_id(category_id)
    if not category:
        raise InvalidUsage("category does not exist")
    validate = v.validate(data, product_schema)
    if not validate:
        raise InvalidUsage({'error': v.errors}, 400)
    found = db.find_product_by_product_name(name)
    if found:
        raise InvalidUsage(f"{found.product_name} name already exists", 400)
    db.modify_product(name, quantity, price, product_id)
    return jsonify({'message': f'{name} has successfully been modified'}), 200


@product.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

