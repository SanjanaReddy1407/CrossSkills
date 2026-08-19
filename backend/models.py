import uuid
from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID, JSONB

from extensions import db


class User(db.Model):
    __tablename__ = "users"

    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    avg_rating = db.Column(db.Numeric(3, 2), default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    skills = db.relationship("Skill", backref="user", cascade="all, delete-orphan")
    schedules = db.relationship("Schedule", backref="user", cascade="all, delete-orphan")

    connections_initiated = db.relationship(
        "Connection", foreign_keys="Connection.user_id",
        backref="initiator", cascade="all, delete-orphan",
    )
    connections_received = db.relationship(
        "Connection", foreign_keys="Connection.connection_user_id",
        backref="recipient", cascade="all, delete-orphan",
    )

    feedback_received = db.relationship(
        "Feedback", foreign_keys="Feedback.user_id",
        backref="target_user", cascade="all, delete-orphan",
    )
    feedback_given = db.relationship(
        "Feedback", foreign_keys="Feedback.reviewer_user_id",
        backref="reviewer", cascade="all, delete-orphan",
    )

    def to_public_dict(self):
        """Safe representation — never include password_hash."""
        return {
            "user_id": str(self.user_id),
            "name": self.name,
            "email": self.email,
            "avg_rating": float(self.avg_rating) if self.avg_rating is not None else 0.0,
        }


class Category(db.Model):
    __tablename__ = "category"

    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    category_name = db.Column(db.String(255), unique=True, nullable=False)

    skills = db.relationship("Skill", backref="category", cascade="all, delete-orphan")

    def to_dict(self):
        return {"category_id": self.category_id, "category_name": self.category_name}


class Skill(db.Model):
    __tablename__ = "skills"

    skill_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.user_id"), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey("category.category_id"), nullable=False)

    skill = db.Column(db.String(255))            # offered skill
    skill_level = db.Column(db.String(50))         # offered skill proficiency
    desired_skill = db.Column(db.String(255))     # target skill
    desired_level = db.Column(db.String(50))        # target proficiency

    def to_dict(self):
        return {
            "skill_id": str(self.skill_id),
            "user_id": str(self.user_id),
            "category_id": self.category_id,
            "skill": self.skill,
            "skill_level": self.skill_level,
            "desired_skill": self.desired_skill,
            "desired_level": self.desired_level,
        }


class Connection(db.Model):
    __tablename__ = "connection"

    connection_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.user_id"), nullable=False)
    connection_user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.user_id"), nullable=False)

    chat_locked = db.Column(db.Boolean, default=True)
    chat_data = db.Column(JSONB, default=list)
    status = db.Column(db.String(20), default="PENDING")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.CheckConstraint(
            "status IN ('PENDING', 'ACTIVE', 'REJECTED', 'COMPLETED')",
            name="chk_connection_status",
        ),
        db.CheckConstraint("user_id != connection_user_id", name="chk_no_self_connection"),
    )

    def to_dict(self):
        return {
            "connection_id": str(self.connection_id),
            "user_id": str(self.user_id),
            "connection_user_id": str(self.connection_user_id),
            "chat_locked": self.chat_locked,
            "status": self.status,
        }


class Schedule(db.Model):
    __tablename__ = "schedule"

    schedule_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.user_id"), nullable=False)

    number_of_slot = db.Column(db.Integer)
    start = db.Column(db.DateTime, nullable=False)
    end = db.Column(db.DateTime, nullable=False)
    agenda = db.Column(db.Text)

    __table_args__ = (
        db.CheckConstraint("\"end\" > start", name="chk_schedule_end_after_start"),
    )

    def to_dict(self):
        return {
            "schedule_id": str(self.schedule_id),
            "user_id": str(self.user_id),
            "number_of_slot": self.number_of_slot,
            "start": self.start.isoformat(),
            "end": self.end.isoformat(),
            "agenda": self.agenda,
        }


class Feedback(db.Model):
    __tablename__ = "feedback"

    feedback_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.user_id"), nullable=False)
    reviewer_user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.user_id"), nullable=False)

    no_of_star = db.Column(db.Integer, nullable=False)
    feedback_text = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.CheckConstraint("no_of_star >= 1 AND no_of_star <= 5", name="chk_star_range"),
        db.CheckConstraint("user_id != reviewer_user_id", name="chk_no_self_feedback"),
    )

    def to_dict(self):
        return {
            "feedback_id": str(self.feedback_id),
            "user_id": str(self.user_id),
            "reviewer_user_id": str(self.reviewer_user_id),
            "no_of_star": self.no_of_star,
            "feedback_text": self.feedback_text,
        }