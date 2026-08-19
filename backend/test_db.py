import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load environment variables from .env
load_dotenv()

database_url = os.getenv("DATABASE_URL")

if not database_url:
    print("❌ Error: DATABASE_URL not found in your .env file.")
    exit(1)

# Ensure the URI starts with postgresql:// instead of postgres://
if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

print("Connecting to Neon...")

try:
    # Initialize connection engine
    engine = create_engine(database_url)
    
    # Execute a simple raw SQL query to test connectivity
    with engine.connect() as connection:
        result = connection.execute(text("SELECT NOW();"))
        db_time = result.scalar()
        print("✅ Connection successful!")
        print(f"🕒 Current Neon Server Time: {db_time}")

except Exception as e:
    print("❌ Connection failed!")
    print(f"Error Details: {e}")
