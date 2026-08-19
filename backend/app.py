import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()

app = Flask(__name__)

# Fetch the connection string from environment variables
database_uri = os.getenv("DATABASE_URL")

# Quick fix: SQLAlchemy requires 'postgresql://', NOT 'postgres://' 
if database_uri and database_uri.startswith("postgres://"):
    database_uri = database_uri.replace("postgres://", "postgresql://", 1)

app.config["SQLALCHEMY_DATABASE_URI"] = database_uri
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize database extension
db = SQLAlchemy(app)

@app.route("/")
def home():
    try:
        # Create database tables to test connection connectivity
        db.create_all()
        return "Connected to Neon database successfully!"
    except Exception as e:
        return f"Database connection failed: {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
