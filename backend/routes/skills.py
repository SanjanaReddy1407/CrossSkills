from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models import Skill, Category

skills_bp = Blueprint("skills", __name__, url_prefix="/api/skills")


@skills_bp.route("", methods=["GET"])
@jwt_required()
def list_my_skills():
    user_id = get_jwt_identity()
    skills = Skill.query.filter_by(user_id=user_id).all()
    return jsonify([s.to_dict() for s in skills]), 200


@skills_bp.route("", methods=["POST"])
@jwt_required()
def add_skill():
    user_id = get_jwt_identity()
    data = request.get_json(silent=True) or {}

    category_id = data.get("category_id")
    skill = (data.get("skill") or "").strip()
    skill_level = (data.get("skill_level") or "").strip()
    desired_skill = (data.get("desired_skill") or "").strip()
    desired_level = (data.get("desired_level") or "").strip()

    if not category_id or not (skill or desired_skill):
        return jsonify({
            "error": "category_id is required, and at least one of skill/desired_skill must be provided"
        }), 400

    if not Category.query.get(category_id):
        return jsonify({"error": "Invalid category_id"}), 400

    record = Skill(
        user_id=user_id,
        category_id=category_id,
        skill=skill or None,
        skill_level=skill_level or None,
        desired_skill=desired_skill or None,
        desired_level=desired_level or None,
    )
    db.session.add(record)
    db.session.commit()
    return jsonify(record.to_dict()), 201


@skills_bp.route("/<uuid:skill_id>", methods=["PUT"])
@jwt_required()
def update_skill(skill_id):
    user_id = get_jwt_identity()
    record = Skill.query.get(str(skill_id))
    if not record:
        return jsonify({"error": "Skill not found"}), 404
    if str(record.user_id) != str(user_id):
        return jsonify({"error": "Not authorized to modify this skill"}), 403

    data = request.get_json(silent=True) or {}
    for field in ("skill", "skill_level", "desired_skill", "desired_level"):
        if field in data:
            setattr(record, field, data[field].strip() or None)

    if "category_id" in data:
        if not Category.query.get(data["category_id"]):
            return jsonify({"error": "Invalid category_id"}), 400
        record.category_id = data["category_id"]

    db.session.commit()
    return jsonify(record.to_dict()), 200


@skills_bp.route("/<uuid:skill_id>", methods=["DELETE"])
@jwt_required()
def delete_skill(skill_id):
    user_id = get_jwt_identity()
    record = Skill.query.get(str(skill_id))
    if not record:
        return jsonify({"error": "Skill not found"}), 404
    if str(record.user_id) != str(user_id):
        return jsonify({"error": "Not authorized to delete this skill"}), 403

    db.session.delete(record)
    db.session.commit()
    return jsonify({"message": "Skill deleted"}), 200
