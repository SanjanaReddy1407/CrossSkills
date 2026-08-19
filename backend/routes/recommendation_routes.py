"""
recommendation_routes.py
GET /api/recommendations?user_id=...&limit=10

Same auth note as search_routes.py: user_id will move into an auth
token once the authentication mechanism is finalized.
"""

from flask import Blueprint, request, jsonify
from backend.services import recommendation_service

recommendation_bp = Blueprint(
    "recommendations", __name__, url_prefix="/api/recommendations"
)


@recommendation_bp.route("", methods=["GET"])
def get_recommendations():
    user_id = request.args.get("user_id")
    limit = request.args.get("limit", default=10, type=int)

    if not user_id:
        return jsonify({"error": "Query parameter 'user_id' is required."}), 400

    results = recommendation_service.get_recommendations(user_id, limit=limit)

    if not results:
        return jsonify(
            {
                "message": "No suitable skill-swap partners found at the moment.",
                "results": [],
            }
        ), 200

    return jsonify({"results": results}), 200