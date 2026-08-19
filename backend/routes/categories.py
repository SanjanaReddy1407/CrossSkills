from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from extensions import db
from models import Category

categories_bp = Blueprint("categories", __name__, url_prefix="/api/categories")


@categories_bp.route("", methods=["GET"])
def list_categories():
    categories = Category.query.order_by(Category.category_name).all()
    return jsonify([c.to_dict() for c in categories]), 200


@categories_bp.route("", methods=["POST"])
@jwt_required()
def create_category():
    data = request.get_json(silent=True) or {}
    name = data.get("category_name", "").strip()
    if not name:
        return jsonify({"error": "category_name is required"}), 400

    if Category.query.filter_by(category_name=name).first():
        return jsonify({"error": "Category already exists"}), 409

    category = Category(category_name=name)
    db.session.add(category)
    db.session.commit()
    return jsonify(category.to_dict()), 201