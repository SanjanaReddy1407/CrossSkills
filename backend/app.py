import os
from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv

from backend.extensions import db
from backend.routes.search_routes import search_bp
from backend.routes.recommendation_routes import recommendation_bp

# Load variables from the .env file
load_dotenv()

app = Flask(__name__)
CORS(app)  # tighten allowed origins before production deployment

# Fetch the connection string from environment variables
database_uri = os.getenv("DATABASE_URL")

# Quick fix: SQLAlchemy requires 'postgresql://', NOT 'postgres://'
if database_uri and database_uri.startswith("postgres://"):
    database_uri = database_uri.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database extension (this is the same `db` object models.py
# and the services use, via backend.extensions)
db.init_app(app)

# Import models so SQLAlchemy knows about them before create_all(),
# then register the search + recommendation blueprints.
with app.app_context():
    from backend import models  # noqa: F401  (import needed for side effect)

app.register_blueprint(search_bp)
app.register_blueprint(recommendation_bp)


@app.route("/")
def home():
    try:
        # Create any tables that don't exist yet, to confirm connectivity
        # (see models.py - remember to run
        #  CREATE EXTENSION IF NOT EXISTS "pgcrypto";
        #  once in Neon so gen_random_uuid() works)
        with app.app_context():
            db.create_all()
        return "Connected to Neon database successfully!"
    except Exception as e:
        return f"Database connection failed: {str(e)}"


if __name__ == "__main__":
    app.run(debug=True)