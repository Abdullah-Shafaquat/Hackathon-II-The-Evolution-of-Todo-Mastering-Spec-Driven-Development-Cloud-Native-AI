#!/usr/bin/env python3
"""
Add priority and category Columns Migration Runner
Adds priority and category columns to tasks table
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import settings
import psycopg2


def run_migration():
    """Run migration to add priority and category columns to tasks table."""

    print("=" * 80)
    print("Add Priority and Category Columns Migration")
    print("=" * 80)

    # Read migration SQL
    migration_file = Path(__file__).parent.parent / "migrations" / "005_add_priority_category.sql"

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

        # Verify columns exist
        print("\n[INFO] Verifying columns...")
        cursor.execute("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = 'tasks'
              AND column_name IN ('priority', 'category')
            ORDER BY column_name
        """)

        columns = cursor.fetchall()

        if len(columns) == 2:
            print("[SUCCESS] Columns created successfully:")
            for col in columns:
                nullable = "NULL" if col[2] == "YES" else "NOT NULL"
                default = f", default={col[3]}" if col[3] else ""
                print(f"   - {col[0]}: {col[1]} ({nullable}{default})")
        else:
            print(f"[ERROR] Expected 2 columns, found {len(columns)}")
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
