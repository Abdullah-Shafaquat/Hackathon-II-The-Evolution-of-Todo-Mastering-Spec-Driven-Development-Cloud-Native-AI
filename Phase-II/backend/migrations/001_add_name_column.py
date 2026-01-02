"""
Migration: Add name column to users table
Run this script to add the missing 'name' column to existing PostgreSQL database
"""

from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def migrate():
    """Add name column to users table if it doesn't exist"""
    engine = create_engine(DATABASE_URL)

    with engine.connect() as conn:
        # Check if column exists
        result = conn.execute(text("""
            SELECT column_name
            FROM information_schema.columns
            WHERE table_name='users' AND column_name='name'
        """))

        if result.fetchone() is None:
            print("Adding 'name' column to users table...")
            conn.execute(text("""
                ALTER TABLE users
                ADD COLUMN name VARCHAR(100)
            """))
            conn.commit()
            print("[SUCCESS] Successfully added 'name' column")
        else:
            print("[INFO] Column 'name' already exists")

if __name__ == "__main__":
    try:
        migrate()
        print("\n[SUCCESS] Migration completed successfully!")
    except Exception as e:
        print(f"\n[ERROR] Migration failed: {e}")
        import traceback
        traceback.print_exc()
