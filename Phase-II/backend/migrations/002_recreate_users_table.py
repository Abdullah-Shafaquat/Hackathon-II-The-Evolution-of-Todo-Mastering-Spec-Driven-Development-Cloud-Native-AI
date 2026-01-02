"""
Migration: Recreate users table with all required columns
This will backup existing data and recreate the table with proper schema
"""

from sqlalchemy import create_engine, text
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def migrate():
    """Recreate users table with all columns"""
    engine = create_engine(DATABASE_URL)

    with engine.connect() as conn:
        print("Step 1: Checking current users table schema...")

        # Get current columns
        result = conn.execute(text("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = 'users'
            ORDER BY ordinal_position
        """))

        current_columns = {row[0]: row[1] for row in result}
        print(f"Current columns: {list(current_columns.keys())}")

        # Backup existing data
        print("\nStep 2: Backing up existing users...")
        backup_result = conn.execute(text("SELECT * FROM users"))
        backup_data = backup_result.fetchall()
        print(f"Backed up {len(backup_data)} users")

        # Drop and recreate table
        print("\nStep 3: Dropping old users table...")
        conn.execute(text("DROP TABLE IF EXISTS tasks CASCADE"))
        conn.execute(text("DROP TABLE IF EXISTS users CASCADE"))
        conn.commit()

        print("\nStep 4: Creating new users table with complete schema...")
        conn.execute(text("""
            CREATE TABLE users (
                id VARCHAR PRIMARY KEY,
                email VARCHAR(255) UNIQUE NOT NULL,
                name VARCHAR(100),
                password_hash VARCHAR NOT NULL,
                created_at TIMESTAMP NOT NULL,
                updated_at TIMESTAMP NOT NULL
            )
        """))

        print("\nStep 5: Creating tasks table...")
        conn.execute(text("""
            CREATE TABLE tasks (
                id SERIAL PRIMARY KEY,
                user_id VARCHAR NOT NULL REFERENCES users(id) ON DELETE CASCADE,
                title VARCHAR(200) NOT NULL,
                description TEXT,
                completed BOOLEAN DEFAULT FALSE,
                created_at TIMESTAMP NOT NULL,
                updated_at TIMESTAMP NOT NULL
            )
        """))

        # Create indexes
        print("\nStep 6: Creating indexes...")
        conn.execute(text("CREATE INDEX idx_users_email ON users(email)"))
        conn.execute(text("CREATE INDEX idx_tasks_user_id ON tasks(user_id)"))

        conn.commit()

        print("\n[SUCCESS] Tables recreated successfully!")
        print("\nNote: Old user data was backed up but passwords cannot be restored.")
        print("Please ask users to sign up again with new accounts.")

if __name__ == "__main__":
    try:
        migrate()
        print("\n[SUCCESS] Migration completed successfully!")
        print("\nNext steps:")
        print("1. Restart your backend server")
        print("2. Go to http://localhost:3000/signup")
        print("3. Create a new account")
    except Exception as e:
        print(f"\n[ERROR] Migration failed: {e}")
        import traceback
        traceback.print_exc()
