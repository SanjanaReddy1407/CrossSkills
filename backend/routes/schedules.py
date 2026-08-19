from datetime import datetime

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models import Schedule

schedules_bp = Blueprint("schedules", __name__, url_prefix="/api/schedules")


def _parse_dt(value):
    try:
        return datetime.fromisoformat(value)
    except (TypeError, ValueError):
        return None


@schedules_bp.route("", methods=["POST"])
@jwt_required()
def create_schedule():
    user_id = get_jwt_identity()
    data = request.get_json(silent=True) or {}

    start = _parse_dt(data.get("start"))
    end = _parse_dt(data.get("end"))

    if not start or not end:
        return jsonify({"error": "start and end must be valid ISO 8601 timestamps"}), 400
    if end <= start:
        return jsonify({"error": "end time must be after start time"}), 400

    schedule = Schedule(
        user_id=user_id,
        number_of_slot=data.get("number_of_slot"),
        start=start,
        end=end,
        agenda=(data.get("agenda") or "").strip() or None,
    )
    db.session.add(schedule)
    db.session.commit()
    return jsonify(schedule.to_dict()), 201


@schedules_bp.route("/<uuid:schedule_id>", methods=["PUT"])
@jwt_required()
def update_schedule(schedule_id):
    user_id = get_jwt_identity()
    schedule = Schedule.query.get(str(schedule_id))
    if not schedule:
        return jsonify({"error": "Schedule not found"}), 404
    if str(schedule.user_id) != str(user_id):
        return jsonify({"error": "Not authorized to modify this schedule"}), 403

    data = request.get_json(silent=True) or {}
    new_start = _parse_dt(data.get("start")) if "start" in data else schedule.start
    new_end = _parse_dt(data.get("end")) if "end" in data else schedule.end

    if "start" in data and not new_start:
        return jsonify({"error": "Invalid start timestamp"}), 400
    if "end" in data and not new_end:
        return jsonify({"error": "Invalid end timestamp"}), 400
    if new_end <= new_start:
        return jsonify({"error": "end time must be after start time"}), 400

    schedule.start = new_start
    schedule.end = new_end
    if "number_of_slot" in data:
        schedule.number_of_slot = data["number_of_slot"]
    if "agenda" in data:
        schedule.agenda = (data["agenda"] or "").strip() or None

    db.session.commit()
    return jsonify(schedule.to_dict()), 200


@schedules_bp.route("/<uuid:user_id>", methods=["GET"])
@jwt_required()
def list_user_schedules(user_id):
    schedules = Schedule.query.filter_by(user_id=str(user_id)).order_by(Schedule.start).all()
    return jsonify([s.to_dict() for s in schedules]), 200


@schedules_bp.route("/<uuid:schedule_id>", methods=["DELETE"])
@jwt_required()
def delete_schedule(schedule_id):
    user_id = get_jwt_identity()
    schedule = Schedule.query.get(str(schedule_id))
    if not schedule:
        return jsonify({"error": "Schedule not found"}), 404
    if str(schedule.user_id) != str(user_id):
        return jsonify({"error": "Not authorized to delete this schedule"}), 403

    db.session.delete(schedule)
    db.session.commit()
    return jsonify({"message": "Schedule deleted"}), 200