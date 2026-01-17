"""
Run database migration for task status field
"""
import os
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    print("ERROR: DATABASE_URL not found in environment variables")
    exit(1)

# Read migration file
migration_file = "migrations/006_add_task_status.sql"

try:
    with open(migration_file, 'r') as f:
        migration_sql = f.read()

    print(f"Running migration: {migration_file}")
    print("=" * 60)

    # Create engine and run migration
    engine = create_engine(DATABASE_URL)

    with engine.connect() as conn:
        # Split by semicolons and execute each statement
        # Remove comment-only lines first
        lines = migration_sql.split('\n')
        sql_lines = []
        for line in lines:
            stripped = line.strip()
            if stripped and not stripped.startswith('--'):
                sql_lines.append(line)

        clean_sql = '\n'.join(sql_lines)
        statements = [s.strip() for s in clean_sql.split(';') if s.strip()]

        for i, statement in enumerate(statements, 1):
            if statement:
                print(f"\nExecuting statement {i}...")
                print(f"  {statement[:80]}...")
                try:
                    conn.execute(text(statement))
                    conn.commit()
                    print("  [OK] Success")
                except Exception as e:
                    # If constraint already exists, that's okay
                    if "already exists" in str(e) or "duplicate" in str(e).lower():
                        print(f"  [SKIP] Already applied: {e}")
                    else:
                        print(f"  [ERROR] {e}")
                        raise

    print("\n" + "=" * 60)
    print("[SUCCESS] Migration completed successfully!")
    print("\nThe 'status' column has been added to the tasks table.")
    print("Existing tasks have been migrated:")
    print("  - Completed tasks -> status = 'completed'")
    print("  - Pending tasks -> status = 'pending'")

except FileNotFoundError:
    print(f"ERROR: Migration file not found: {migration_file}")
    exit(1)
except Exception as e:
    print(f"\nERROR: Migration failed: {e}")
    exit(1)
