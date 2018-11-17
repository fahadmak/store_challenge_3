from flask import Blueprint, jsonify, request, current_app as app
from flask_jwt_extended import jwt_required, get_jwt_identity
from cerberus import Validator

from app.error_handler import InvalidUsage
from app.models.database import Database
from app.validation_schema import product_schema, add_product_schema

product = Blueprint("product", __name__)

v = Validator()


@product.route("/api/v1/products", methods=["POST"])
@jwt_required
def create_product():
    """A method adds product to database"""

    if request.content_type != "application/json":
        raise InvalidUsage("Invalid content type", 400)

    db = Database(app.config['DATABASE_URI'])
    current_user_id = get_jwt_identity()
    user = db.find_user_by_id(current_user_id)
    if user.is_admin is False:
        raise InvalidUsage("you do not have admin rights", 401)

    data = request.json
    name = data.get("name")
    price = data.get("price")
    quantity = data.get("quantity")
    category_id = data.get("category_id")

    validate = v.validate(data, add_product_schema)
    if not validate:
        raise InvalidUsage(v.errors, 400)

    category = db.find_category_by_category_id(category_id)
    if not category:
        raise InvalidUsage("category does not exist", 404)

    found = db.find_product_by_product_name(name)
    if found:
        raise InvalidUsage(f"{found.product_name} already exists", 400)
    db.add_product(name, quantity, price, current_user_id, category_id)
    return jsonify({'message': f'{name}'
                               f' has successfully been added to inventories'}), 201


@product.route("/api/v1/products/<int:product_id>", methods=["PUT"])
@jwt_required
def modify_product(product_id):
    """A method adds product instance to products list"""
    if request.content_type != "application/json":
        raise InvalidUsage("Invalid content type", 400)

    data = request.json
    name = data.get("name")
    price = data.get("price")
    quantity = data.get("quantity")

    validate = v.validate(data, product_schema)
    if not validate:
        raise InvalidUsage({'error': v.errors}, 400)

    db = Database(app.config['DATABASE_URI'])

    current_user_id = get_jwt_identity()
    user = db.find_user_by_id(current_user_id)
    if user.is_admin is False:
        raise InvalidUsage("you do not have admin rights", 401)

    found = db.find_product_by_product_name(name)
    if found:
        raise InvalidUsage(f"{found.product_name} name already exists", 400)

    db.modify_product(name, quantity, price, product_id)

    return jsonify({'message': f'Product is now called {name} '}), 200


@product.route("/api/v1/products/<int:product_id>", methods=["DELETE"])
@jwt_required
def delete_product(product_id):
    """A method deletes product stored in the database"""
    if request.content_type != "application/json":
        raise InvalidUsage("Invalid content type", 400)

    db = Database(app.config['DATABASE_URI'])

    current_user_id = get_jwt_identity()
    user = db.find_user_by_id(current_user_id)
    if not user.is_admin:
        raise InvalidUsage("you do not have admin rights", 401)

    item = db.find_product_by_product_id(product_id)
    if not item:
        raise InvalidUsage("product does not exist", 404)
    item_name, item_id = item.product_name, item.product_id
    db.delete_product(product_id)
    return jsonify({'message': f'{item_name} has been deleted'}), 200


@product.route("/api/v1/products/<int:product_id>", methods=["GET"])
@jwt_required
def get_product(product_id):
    """A method adds product instance to products list"""

    if request.content_type != "application/json":
        raise InvalidUsage("Invalid content type", 400)

    db = Database(app.config['DATABASE_URI'])

    item = db.find_product_by_product_id(product_id)
    if not item:
        raise InvalidUsage("product does not exist", 400)
    return jsonify({'product': item.to_json()}), 200


@product.route("/api/v1/products", methods=["GET"])
@jwt_required
def get_all_products():
    """A method gets all products"""
    if request.content_type != 'application/json':
        raise InvalidUsage("Invalid content type", 400)

    db = Database(app.config['DATABASE_URI'])

    products = db.get_all_products()
    if not products:
        raise InvalidUsage("They are currently no products")

    return jsonify({'products': products}), 200


@product.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

