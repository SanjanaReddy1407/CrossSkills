from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models import User

users_bp = Blueprint("users", __name__, url_prefix="/api/users")


@users_bp.route("/me", methods=["GET"])
@jwt_required()
def get_my_profile():
    user = User.query.get(get_jwt_identity())
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_public_dict()), 200


@users_bp.route("/me", methods=["PUT"])
@jwt_required()
def update_my_profile():
    user = User.query.get(get_jwt_identity())
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json(silent=True) or {}
    if "name" in data and data["name"].strip():
        user.name = data["name"].strip()

    db.session.commit()
    return jsonify(user.to_public_dict()), 200


@users_bp.route("/<uuid:user_id>", methods=["GET"])
@jwt_required()
def get_user(user_id):
    user = User.query.get(str(user_id))
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.to_public_dict()), 200