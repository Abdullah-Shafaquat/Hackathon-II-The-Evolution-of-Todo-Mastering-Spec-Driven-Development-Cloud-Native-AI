#!/usr/bin/env python3
"""
Add due_date Column Migration Runner
Adds due_date column to tasks table
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import settings
import psycopg2


def run_migration():
    """Run migration to add due_date column to tasks table."""

    print("=" * 80)
    print("Add due_date Column Migration")
    print("=" * 80)

    # Read migration SQL
    migration_file = Path(__file__).parent.parent / "migrations" / "004_add_task_due_date.sql"

    if not migration_file.exists():
        print(f"[ERROR] Migration file not found: {migration_file}")
        return False

    print(f"\n[INFO] Reading migration file: {migration_file.name}")

    with open(migration_file, 'r') as f:
        migration_sql = f.read()

    # Connect to database
    print(f"\n[INFO] Connecting to database...")
    print(f"   Database URL: {settings.DATABASE_URL[:50]}...")

    try:
        conn = psycopg2.connect(settings.DATABASE_URL)
        conn.autocommit = True
        cursor = conn.cursor()

        print("[SUCCESS] Connected successfully")

        # Execute migration
        print("\n[INFO] Executing migration...")
        cursor.execute(migration_sql)

        print("[SUCCESS] Migration executed successfully")

        # Verify column exists
        print("\n[INFO] Verifying column...")
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'tasks'
              AND column_name = 'due_date'
        """)

        column = cursor.fetchone()

        if column:
            print("[SUCCESS] due_date column created successfully:")
            nullable = "NULL" if column[2] == "YES" else "NOT NULL"
            print(f"   - {column[0]}: {column[1]} ({nullable})")
        else:
            print("[ERROR] Column not found after migration")
            return False

        # Show full tasks table structure
        print("\n[INFO] Updated tasks table structure:")
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'tasks'
            ORDER BY ordinal_position
        """)

        columns = cursor.fetchall()
        for col in columns:
            nullable = "NULL" if col[2] == "YES" else "NOT NULL"
            print(f"   - {col[0]}: {col[1]} ({nullable})")

        # Close connection
        cursor.close()
        conn.close()

        print("\n" + "=" * 80)
        print("[SUCCESS] Migration completed successfully!")
        print("=" * 80)

        return True

    except Exception as e:
        print(f"\n[ERROR] Migration failed: {e}")
        print(f"   Details: {type(e).__name__}")
        return False


if __name__ == "__main__":
    success = run_migration()
    sys.exit(0 if success else 1)
