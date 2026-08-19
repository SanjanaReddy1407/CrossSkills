from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models import Connection, User

connections_bp = Blueprint("connections", __name__, url_prefix="/api/connections")

VALID_STATUSES = {"PENDING", "ACTIVE", "REJECTED", "COMPLETED"}


@connections_bp.route("", methods=["POST"])
@jwt_required()
def send_request():
    user_id = get_jwt_identity()
    data = request.get_json(silent=True) or {}
    target_id = data.get("connection_user_id")

    if not target_id:
        return jsonify({"error": "connection_user_id is required"}), 400

    if str(target_id) == str(user_id):
        return jsonify({"error": "Cannot send a request to yourself"}), 400

    if not User.query.get(target_id):
        return jsonify({"error": "Target user not found"}), 404

    existing = Connection.query.filter(
        db.or_(
            db.and_(Connection.user_id == user_id, Connection.connection_user_id == target_id),
            db.and_(Connection.user_id == target_id, Connection.connection_user_id == user_id),
        ),
        Connection.status.in_(["PENDING", "ACTIVE"]),
    ).first()
    if existing:
        return jsonify({"error": "A pending or active connection already exists with this user"}), 409

    connection = Connection(user_id=user_id, connection_user_id=target_id, status="PENDING")
    db.session.add(connection)
    db.session.commit()
    return jsonify(connection.to_dict()), 201


@connections_bp.route("/<uuid:connection_id>", methods=["PATCH"])
@jwt_required()
def respond_to_request(connection_id):
    user_id = get_jwt_identity()
    connection = Connection.query.get(str(connection_id))
    if not connection:
        return jsonify({"error": "Connection not found"}), 404

    # Only the recipient can accept/reject
    if str(connection.connection_user_id) != str(user_id):
        return jsonify({"error": "Not authorized to respond to this request"}), 403

    data = request.get_json(silent=True) or {}
    new_status = (data.get("status") or "").upper()

    if new_status not in VALID_STATUSES:
        return jsonify({"error": f"status must be one of {sorted(VALID_STATUSES)}"}), 400

    if connection.status != "PENDING":
        return jsonify({"error": f"Connection is already {connection.status}, cannot change"}), 409

    connection.status = new_status
    if new_status == "ACTIVE":
        connection.chat_locked = False  # unlock chat once accepted

    db.session.commit()
    return jsonify(connection.to_dict()), 200


@connections_bp.route("", methods=["GET"])
@jwt_required()
def list_my_connections():
    user_id = get_jwt_identity()
    connections = Connection.query.filter(
        db.or_(Connection.user_id == user_id, Connection.connection_user_id == user_id)
    ).all()
    return jsonify([c.to_dict() for c in connections]), 200