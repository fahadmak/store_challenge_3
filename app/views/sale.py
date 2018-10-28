from flask import Blueprint, jsonify, request

from app.models.model import Sale, sales
from app.error_handler import InvalidUsage
from app.utils import find_product


sale = Blueprint('sale', __name__)


@sale.route("/api/v1/sales", methods=["POST"])
def add_sale():
    if request.content_type != "application/json":
        raise InvalidUsage("Invalid content type", 400)
    data = request.json
    cart = data.get('cart')
    if not cart:
        raise InvalidUsage("please fill missing fields", 400)
    if not isinstance(cart, dict):
        raise InvalidUsage("please input correct format like {'corn': 6000, 'fish': 12300}", 400)
    unavailable = [item for item in cart if not find_product(item)]
    if not unavailable:
        shopping = [item for item in cart]
        for item in cart:
            if find_product(item).quantity >= cart[item]:
                find_product(item).quantity -= cart[item]
                shopping.remove(item)
            else:
                few_instock = ', '.join(str(item) for item in shopping)
                raise InvalidUsage(f"{few_instock} these quantity are unavailable", 400)
        sold_id = max([sold.saleId for sold in sales]) + 1 if sales else 1
        sold = Sale(sold_id, cart)
        sales.append(sold)
        return jsonify({"message": str(sold)}), 201
    raise InvalidUsage(f"{', '.join(str(item) for item in unavailable)} can not be found", 400)


@sale.route("/api/v1/sales", methods=["GET"])
def get_all_sales():
    if not sales:
        raise InvalidUsage("They are currently no sales", 404)
    json_sales = []
    for sold in sales:
        json_sales.append(sold.to_json())
    return jsonify({"sales": json_sales}), 200


@sale.route("/api/v1/sales/<int:sale_id>", methods=["GET"])
def get_sale_by_id(sale_id):
    for sold in sales:
        if sold.saleId == sale_id:
            return jsonify({"sale": sold.to_json()}), 200
    else:
        return jsonify({"error": f"Sale Record of ID {sale_id} does not exist"}), 404


@sale.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


