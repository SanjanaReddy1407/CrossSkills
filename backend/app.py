import os

from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

from extensions import db, jwt

load_dotenv()


def create_app():
    app = Flask(__name__)

    database_uri = os.getenv("DATABASE_URL")
    if database_uri and database_uri.startswith("postgres://"):
        database_uri = database_uri.replace("postgres://", "postgresql://", 1)

    app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "dev-secret-change-me")

    db.init_app(app)
    jwt.init_app(app)
    CORS(app)  # allow the React frontend (different origin) to call this API

    # Register blueprints — one per PRD section 49 module
    from routes.auth import auth_bp
    from routes.users import users_bp
    from routes.categories import categories_bp
    from routes.skills import skills_bp
    from routes.search import search_bp
    from routes.recommendations import recommendations_bp
    from routes.connections import connections_bp
    from routes.chat import chat_bp
    from routes.schedules import schedules_bp
    from routes.feedback import feedback_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(categories_bp)
    app.register_blueprint(skills_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(recommendations_bp)
    app.register_blueprint(connections_bp)
    app.register_blueprint(chat_bp)
    app.register_blueprint(schedules_bp)
    app.register_blueprint(feedback_bp)

    @app.route("/")
    def health_check():
        try:
            db.create_all()
            return "Connected to Neon database successfully! All tables created."
        except Exception as e:
            return f"Database connection failed: {str(e)}"

    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Not found"}), 404

    @app.errorhandler(500)
    def server_error(e):
        return jsonify({"error": "Internal server error"}), 500

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)