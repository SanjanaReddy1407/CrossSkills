"""
search_routes.py
GET /api/search/by-name?q=...&user_id=...
GET /api/search/by-skill?q=...&user_id=...

NOTE: user_id is passed as a query param for now since the authentication
mechanism is still an open decision (PRD Section 83, item 3). Once you add
JWT/session auth, replace `request.args.get("user_id")` with the value
pulled from the verified token instead.
"""

from flask import Blueprint, request, jsonify
from backend.services import search_service

search_bp = Blueprint("search", __name__, url_prefix="/api/search")


@search_bp.route("/by-name", methods=["GET"])
def by_name():
    name = request.args.get("q", "").strip()
    user_id = request.args.get("user_id")

    if not name:
        return jsonify({"error": "Query parameter 'q' is required."}), 400

    results = search_service.search_by_name(name, exclude_user_id=user_id)
    if not results:
        return jsonify({"message": "User not found.", "results": []}), 200

    return jsonify({"results": results}), 200


@search_bp.route("/by-skill", methods=["GET"])
def by_skill():
    skill = request.args.get("q", "").strip()
    user_id = request.args.get("user_id")

    if not skill:
        return jsonify({"error": "Query parameter 'q' is required."}), 400

    results = search_service.search_by_skill(skill, exclude_user_id=user_id)
    if not results:
        return jsonify(
            {"message": "No users found with this skill.", "results": []}
        ), 200

    return jsonify({"results": results}), 200