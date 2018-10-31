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
    """A method adds product instance to products list"""
    db = Database(app.config['DATABASE_URI'])
    if request.content_type != "application/json":
        raise InvalidUsage("Invalid content type", 400)
    data = request.json
    product_id = data.get("product_id")
    quantity = data.get("quantity")
    print("yes")
    current_user_id = get_jwt_identity()
    user = db.find_user_by_id(current_user_id)
    if user.is_admin is False:
        raise InvalidUsage("you do not have admin rights", 403)
    validate = v.validate(data, sale_schema)
    if not validate:
        raise InvalidUsage({'error': v.errors}, 400)
    product = db.find_product_by_product_id(product_id)
    if not product:
        raise InvalidUsage("product does not exist", 400)
    if quantity < product.quantity:
        total = product.price * quantity
        new_stock = product.quantity - quantity
        db.update_stock(new_stock, product_id)
        db.add_sale(total, current_user_id)
        return jsonify({'message': 'Sale record has been created successfully'}), 200
    raise InvalidUsage("This quantity is unavailable, try lesser quantity", 400)


@sale.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
