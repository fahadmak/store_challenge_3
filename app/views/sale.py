from flask import Blueprint, jsonify, request, current_app as app
from flask_jwt_extended import jwt_required, get_jwt_identity
from cerberus import Validator

from app.error_handler import InvalidUsage
from app.models.database import Database
from app.validation_schema import sale_schema

v = Validator()


sale = Blueprint("sale", __name__)


@sale.route("/api/v1/sales", methods=["POST"])
@jwt_required
def create_sale():
    """A method that creates a products"""

    if request.content_type != "application/json":
        raise InvalidUsage("Invalid content type", 400)

    db = Database(app.config['DATABASE_URI'])
    current_user_id = get_jwt_identity()
    user = db.find_user_by_id(current_user_id)
    if user.is_admin is False:
        raise InvalidUsage("you do not have admin rights", 401)
    data = request.json
    cart = data.get("cart")
    total = 0
    sales_by_id = db.get_max_sale_id()
    sale_id = max([sold for sold in sales_by_id]) + 1 if sales_by_id else 1
    for item in cart:
        validate = v.validate(item, sale_schema)
        if not validate:
            raise InvalidUsage({'error': v.errors}, 400)
        product = db.find_product_by_product_id(item['product_id'])
        if not product:
            raise InvalidUsage("product does not exist", 400)
        if item['quantity'] > product.quantity:
            raise InvalidUsage(f"This quantity of {product.product_name} ordered should less than "
                               f"{item['quantity']}", 400)
        total += product.price * item['quantity']
        new_stock = product.quantity - item['quantity']
        db.update_stock(new_stock, item['product_id'])
        db.add_sold_item(item['quantity'], item['product_id'], sale_id)
    db.add_sale(total, current_user_id, sale_id)
    return jsonify({'message': 'Sale record has been created successfully'}), 200


@sale.route("/api/v1/sales/<int:sale_id>", methods=["GET"])
@jwt_required
def get_sale(sale_id):
    """A method that gets a sale"""

    if request.content_type != "application/json":
        raise InvalidUsage("Invalid content type", 400)

    current_user_id = get_jwt_identity()

    db = Database(app.config['DATABASE_URI'])
    user = db.find_user_by_id(current_user_id)
    if user.is_admin is True:
        raise InvalidUsage("You can't access this sale record", 401)

    item = db.find_sale_by_sale_id(sale_id)
    if item.user_id != current_user_id:
        raise InvalidUsage("sale record does not exist")

    return jsonify({'sale': item.to_json()}), 200


@sale.route("/api/v1/sales", methods=["GET"])
@jwt_required
def get_all_sale():
    """A method that gets all sales"""

    if request.content_type != "application/json":
        raise InvalidUsage("Invalid content type", 400)

    current_user_id = get_jwt_identity()

    db = Database(app.config['DATABASE_URI'])
    user = db.find_user_by_id(current_user_id)
    if user.is_admin is False:
        raise InvalidUsage("you do not have admin rights", 401)

    item = db.get_all_sales()
    if not item:
        raise InvalidUsage("No sale records")

    return jsonify({'sale': item}), 200


@sale.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
