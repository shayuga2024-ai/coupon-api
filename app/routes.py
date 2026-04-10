from flask import Blueprint, jsonify, request
from .models import get_all, get_by_code, create

bp = Blueprint("coupon", __name__)

@bp.route("/coupons", methods=["GET"])
def list_coupons():
    return jsonify({"coupons": get_all()}), 200

@bp.route("/coupons/<code>", methods=["GET"])
def get_coupon(code):
    coupon = get_by_code(code)
    if not coupon:
        return jsonify({"error": "Coupon not found"}), 404
    if not coupon["active"]:
        return jsonify({"error": "Coupon is expired"}), 400
    return jsonify(coupon), 200

@bp.route("/coupons", methods=["POST"])
def create_coupon():
    data = request.get_json()
    if not data or "code" not in data or "discount" not in data:
        return jsonify({"error": "code and discount are required"}), 400
    if get_by_code(data["code"]):
        return jsonify({"error": "Coupon code already exists"}), 409
    coupon = create(data["code"], data["discount"])
    return jsonify({"message": "Coupon created!", "coupon": coupon}), 201

@bp.route("/apply", methods=["POST"])
def apply_coupon():
    data = request.get_json()
    if not data or "code" not in data or "price" not in data:
        return jsonify({"error": "code and price are required"}), 400
    coupon = get_by_code(data["code"])
    if not coupon:
        return jsonify({"error": "Coupon not found"}), 404
    if not coupon["active"]:
        return jsonify({"error": "Coupon is expired"}), 400
    original = data["price"]
    final = round(original - (original * coupon["discount"] / 100), 2)
    return jsonify({
        "original_price": original,
        "discount_percent": coupon["discount"],
        "final_price": final,
        "you_save": round(original - final, 2)
    }), 200