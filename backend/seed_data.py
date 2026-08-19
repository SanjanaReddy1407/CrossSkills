"""
seed_data.py
Quick script to insert 2 test users with complementary skills, so you
can immediately test /api/search and /api/recommendations without
building the full auth/profile UI first.

Run from the project root (same place you run `python -m backend.app`):
    python -m backend.seed_data

Delete this file once you have real signup/profile flows.
"""

from werkzeug.security import generate_password_hash

from backend.app import app
from backend.extensions import db
from backend.models import User, Category, Skill


def run():
    with app.app_context():
        db.create_all()

        # Category
        web_dev = Category.query.filter_by(category_name="Web Development").first()
        if not web_dev:
            web_dev = Category(category_name="Web Development")
            db.session.add(web_dev)
            db.session.commit()

        # User A: knows Python, wants React
        user_a = User(
            name="Student A",
            email="studenta@example.com",
            password_hash=generate_password_hash("password123"),
            avg_rating=4.5,
        )
        # User B: knows React, wants Python
        user_b = User(
            name="Student B",
            email="studentb@example.com",
            password_hash=generate_password_hash("password123"),
            avg_rating=4.7,
        )
        db.session.add_all([user_a, user_b])
        db.session.commit()

        skill_a = Skill(
            user_id=user_a.user_id,
            category_id=web_dev.category_id,
            skill="Python",
            skill_level="Advanced",
            desired_skill="React",
            desired_level="Intermediate",
        )
        skill_b = Skill(
            user_id=user_b.user_id,
            category_id=web_dev.category_id,
            skill="React",
            skill_level="Advanced",
            desired_skill="Python",
            desired_level="Intermediate",
        )
        db.session.add_all([skill_a, skill_b])
        db.session.commit()

        print("Seeded successfully!")
        print(f"Student A user_id: {user_a.user_id}")
        print(f"Student B user_id: {user_b.user_id}")
        print()
        print("Try these:")
        print(f"  http://127.0.0.1:5000/api/search/by-skill?q=react")
        print(f"  http://127.0.0.1:5000/api/recommendations?user_id={user_a.user_id}")


if __name__ == "__main__":
    run()