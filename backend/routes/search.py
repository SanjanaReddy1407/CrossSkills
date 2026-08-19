from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

from models import User, Skill

search_bp = Blueprint("search", __name__, url_prefix="/api/search")


@search_bp.route("/name", methods=["GET"])
@jwt_required()
def search_by_name():
    query = (request.args.get("q") or "").strip()
    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400

    users = User.query.filter(User.name.ilike(f"%{query}%")).limit(50).all()
    return jsonify([u.to_public_dict() for u in users]), 200


@search_bp.route("/skill", methods=["GET"])
@jwt_required()
def search_by_skill():
    query = (request.args.get("q") or "").strip()
    if not query:
        return jsonify({"error": "Query parameter 'q' is required"}), 400

    # Normalize: case-insensitive match against offered skill (PRD section 53)
    matches = (
        Skill.query.filter(Skill.skill.ilike(f"%{query}%"))
        .join(User, Skill.user_id == User.user_id)
        .add_columns(User.user_id, User.name, User.avg_rating)
        .limit(50)
        .all()
    )

    results = []
    seen = set()
    for skill_row, user_id, name, avg_rating in matches:
        if str(user_id) in seen:
            continue
        seen.add(str(user_id))
        results.append({
            "user_id": str(user_id),
            "name": name,
            "avg_rating": float(avg_rating) if avg_rating is not None else 0.0,
            "matched_skill": skill_row.skill,
            "skill_level": skill_row.skill_level,
        })

    if not results:
        return jsonify({"message": "No users found with this skill", "results": []}), 200

    return jsonify({"results": results}), 200