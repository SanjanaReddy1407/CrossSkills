"""
search_service.py
User-driven search: by name, or by skill (PRD Sections 11, 54).
Uses Flask-SQLAlchemy ORM (matches your existing app.py setup).

Search is intentionally "dumb" compared to the recommendation engine -
it returns direct matches, not ranked/scored suggestions.
Never returns password_hash or other private fields.
"""

from sqlalchemy import func

from backend.extensions import db
from backend.models import User, Skill, Category
from backend.utils.normalization import normalize_skill


def search_by_name(name: str, exclude_user_id: str = None, limit: int = 20):
    """Returns users whose name matches (case-insensitive, partial)."""
    query = User.query.filter(func.lower(User.name).like(f"%{name.strip().lower()}%"))
    if exclude_user_id:
        query = query.filter(User.user_id != exclude_user_id)

    users = query.order_by(User.name).limit(limit).all()

    return [
        {
            "user_id": str(u.user_id),
            "name": u.name,
            "avg_rating": float(u.avg_rating or 0),
        }
        for u in users
    ]


def search_by_skill(skill: str, exclude_user_id: str = None, limit: int = 20):
    """
    Returns users who OFFER the given skill (normalized match),
    along with their skill_level and category.
    """
    normalized = normalize_skill(skill)

    query = (
        db.session.query(Skill, User, Category)
        .join(User, User.user_id == Skill.user_id)
        .outerjoin(Category, Category.category_id == Skill.category_id)
        .filter(func.lower(Skill.skill) == normalized)
    )
    if exclude_user_id:
        query = query.filter(User.user_id != exclude_user_id)

    rows = query.order_by(User.avg_rating.desc().nullslast()).limit(limit).all()

    return [
        {
            "user_id": str(u.user_id),
            "name": u.name,
            "avg_rating": float(u.avg_rating or 0),
            "skill": s.skill,
            "skill_level": s.skill_level,
            "category_name": c.category_name if c else None,
        }
        for s, u, c in rows
    ]