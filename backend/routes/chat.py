from datetime import datetime

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.orm.attributes import flag_modified

from extensions import db
from models import Connection

chat_bp = Blueprint("chat", __name__, url_prefix="/api/connections")


def _get_authorized_connection(connection_id, user_id):
    connection = Connection.query.get(str(connection_id))
    if not connection:
        return None, ("Connection not found", 404)
    if str(connection.user_id) != str(user_id) and str(connection.connection_user_id) != str(user_id):
        return None, ("Not authorized to access this chat", 403)
    return connection, None


@chat_bp.route("/<uuid:connection_id>/messages", methods=["GET"])
@jwt_required()
def get_messages(connection_id):
    user_id = get_jwt_identity()
    connection, error = _get_authorized_connection(connection_id, user_id)
    if error:
        return jsonify({"error": error[0]}), error[1]

    return jsonify({"messages": connection.chat_data or []}), 200


@chat_bp.route("/<uuid:connection_id>/messages", methods=["POST"])
@jwt_required()
def send_message(connection_id):
    user_id = get_jwt_identity()
    connection, error = _get_authorized_connection(connection_id, user_id)
    if error:
        return jsonify({"error": error[0]}), error[1]

    if connection.chat_locked or connection.status != "ACTIVE":
        return jsonify({"error": "Chat is locked until the connection is active"}), 403

    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    if not text:
        return jsonify({"error": "Message text is required"}), 400

    message = {
        "sender_id": str(user_id),
        "text": text,
        "sent_at": datetime.utcnow().isoformat(),
    }

    messages = list(connection.chat_data or [])
    messages.append(message)
    connection.chat_data = messages
    flag_modified(connection, "chat_data")  # required so SQLAlchemy detects the JSONB mutation

    db.session.commit()
    return jsonify(message), 201