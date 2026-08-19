"""
models.py
SQLAlchemy ORM models matching the PRD ER Diagram (Sections 32-39).

These are now the SOURCE OF TRUTH for your schema - app.py calls
db.create_all() on startup, which creates any tables that don't exist
yet based on these classes. You do NOT need to run schema.sql manually
UNLESS you prefer managing the schema by hand / via migrations - in
that case keep schema.sql in sync with this file instead.

One-time requirement in Neon (for gen_random_uuid() to work):
    CREATE EXTENSION IF NOT EXISTS "pgcrypto";
Run that once in the Neon SQL editor. db.create_all() does not create
extensions, only tables.
"""

import uuid
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func

from backend.extensions import db


class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(
        UUID(as_uuid=True), primary_key=True, server_default=db.text("gen_random_uuid()")
    )
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    avg_rating = db.Column(db.Numeric(3, 2), default=0)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    skills = db.relationship("Skill", backref="user", lazy=True, cascade="all, delete-orphan")


class Category(db.Model):
    __tablename__ = "category"

    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), unique=True, nullable=False)


class Skill(db.Model):
    __tablename__ = "skills"

    skill_id = db.Column(
        UUID(as_uuid=True), primary_key=True, server_default=db.text("gen_random_uuid()")
    )
    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False
    )
    category_id = db.Column(db.Integer, db.ForeignKey("category.category_id"))
    skill = db.Column(db.String(100), nullable=False)          # offered skill
    skill_level = db.Column(db.String(20), nullable=False)      # offered proficiency
    desired_skill = db.Column(db.String(100))                   # target skill
    desired_level = db.Column(db.String(20))                    # target proficiency

    category = db.relationship("Category", lazy=True)


class Connection(db.Model):
    __tablename__ = "connection"

    connection_id = db.Column(
        UUID(as_uuid=True), primary_key=True, server_default=db.text("gen_random_uuid()")
    )
    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False
    )
    connection_user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False
    )
    chat_locked = db.Column(db.Boolean, default=True)
    chat_data = db.Column(JSONB, default=list)   # messages array
    status = db.Column(db.String(20), default="PENDING")  # PENDING / ACTIVE / COMPLETED
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        db.CheckConstraint("user_id <> connection_user_id", name="no_self_connection"),
    )


class Schedule(db.Model):
    __tablename__ = "schedule"

    schedule_id = db.Column(
        UUID(as_uuid=True), primary_key=True, server_default=db.text("gen_random_uuid()")
    )
    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False
    )
    number_of_slot = db.Column(db.Integer, default=1)
    start_time = db.Column(db.DateTime(timezone=True), nullable=False)
    end_time = db.Column(db.DateTime(timezone=True), nullable=False)
    agenda = db.Column(db.Text)

    __table_args__ = (
        db.CheckConstraint("end_time > start_time", name="end_after_start"),
    )


class Feedback(db.Model):
    __tablename__ = "feedback"

    feedback_id = db.Column(
        UUID(as_uuid=True), primary_key=True, server_default=db.text("gen_random_uuid()")
    )
    user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False
    )  # target user
    reviewer_user_id = db.Column(
        UUID(as_uuid=True), db.ForeignKey("users.user_id", ondelete="CASCADE"), nullable=False
    )
    no_of_star = db.Column(db.Integer, nullable=False)
    feedback_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    __table_args__ = (
        db.CheckConstraint("no_of_star BETWEEN 1 AND 5", name="star_range"),
    )