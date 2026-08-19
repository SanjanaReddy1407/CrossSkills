from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import func

from extensions import db
from models import Feedback, User

feedback_bp = Blueprint("feedback", __name__, url_prefix="/api/feedback")


def _recalculate_avg_rating(target_user_id):
    avg = db.session.query(func.avg(Feedback.no_of_star)).filter(
        Feedback.user_id == target_user_id
    ).scalar()
    user = User.query.get(target_user_id)
    if user:
        user.avg_rating = round(float(avg), 2) if avg is not None else 0.0
        db.session.commit()


@feedback_bp.route("", methods=["POST"])
@jwt_required()
def submit_feedback():
    reviewer_id = get_jwt_identity()
    data = request.get_json(silent=True) or {}

    target_id = data.get("user_id")
    stars = data.get("no_of_star")
    text = (data.get("feedback_text") or "").strip() or None

    if not target_id:
        return jsonify({"error": "user_id (target) is required"}), 400
    if str(target_id) == str(reviewer_id):
        return jsonify({"error": "Cannot leave feedback for yourself"}), 400
    if not isinstance(stars, int) or not (1 <= stars <= 5):
        return jsonify({"error": "no_of_star must be an integer between 1 and 5"}), 400
    if not User.query.get(target_id):
        return jsonify({"error": "Target user not found"}), 404

    entry = Feedback(
        user_id=target_id,
        reviewer_user_id=reviewer_id,
        no_of_star=stars,
        feedback_text=text,
    )
    db.session.add(entry)
    db.session.commit()

    _recalculate_avg_rating(target_id)

    return jsonify(entry.to_dict()), 201


@feedback_bp.route("/<uuid:user_id>", methods=["GET"])
@jwt_required()
def get_feedback_for_user(user_id):
    entries = Feedback.query.filter_by(user_id=str(user_id)).order_by(Feedback.created_at.desc()).all()
    if not entries:
        return jsonify({"message": "No feedback received yet.", "results": []}), 200
    return jsonify({"results": [e.to_dict() for e in entries]}), 200