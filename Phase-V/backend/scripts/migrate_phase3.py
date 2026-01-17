#!/usr/bin/env python3
"""
Phase III Database Migration Runner
Applies Phase III migrations (conversations and messages tables)
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.config import settings
import psycopg2


def run_migration():
    """Run Phase III migration to add conversations and messages tables."""

    print("=" * 80)
    print("Phase III Database Migration")
    print("=" * 80)

    # Read migration SQL
    migration_file = Path(__file__).parent.parent / "migrations" / "003_add_conversations_messages.sql"

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

        # Verify tables exist
        print("\n[INFO] Verifying tables...")
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
              AND table_name IN ('conversations', 'messages')
            ORDER BY table_name
        """)

        tables = cursor.fetchall()

        if len(tables) == 2:
            print("[SUCCESS] Both tables created successfully:")
            for table in tables:
                print(f"   - {table[0]}")
        else:
            print(f"[WARNING] Expected 2 tables, found {len(tables)}")

        # Show table structures
        print("\n[INFO] Table structures:")

        for table_name in ['conversations', 'messages']:
            cursor.execute(f"""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns
                WHERE table_name = '{table_name}'
                ORDER BY ordinal_position
            """)

            columns = cursor.fetchall()
            print(f"\n   {table_name}:")
            for col in columns:
                nullable = "NULL" if col[2] == "YES" else "NOT NULL"
                print(f"     - {col[0]}: {col[1]} ({nullable})")

        # Close connection
        cursor.close()
        conn.close()

        print("\n" + "=" * 80)
        print("[SUCCESS] Phase III migration completed successfully!")
        print("=" * 80)

        return True

    except Exception as e:
        print(f"\n[ERROR] Migration failed: {e}")
        return False


def rollback_migration():
    """Rollback Phase III migration (remove tables)."""

    print("=" * 80)
    print("Phase III Database Rollback")
    print("=" * 80)

    # Confirm rollback
    response = input("\n[WARNING] This will delete all conversation data. Continue? (yes/no): ")

    if response.lower() != 'yes':
        print("[INFO] Rollback cancelled")
        return False

    # Read rollback SQL
    rollback_file = Path(__file__).parent.parent / "migrations" / "003_rollback_conversations_messages.sql"

    if not rollback_file.exists():
        print(f"[ERROR] Rollback file not found: {rollback_file}")
        return False

    print(f"\n[INFO] Reading rollback file: {rollback_file.name}")

    with open(rollback_file, 'r') as f:
        rollback_sql = f.read()

    # Connect to database
    print(f"\n[INFO] Connecting to database...")

    try:
        conn = psycopg2.connect(settings.DATABASE_URL)
        conn.autocommit = True
        cursor = conn.cursor()

        print("[SUCCESS] Connected successfully")

        # Execute rollback
        print("\n[INFO] Executing rollback...")
        cursor.execute(rollback_sql)

        print("[SUCCESS] Rollback executed successfully")

        # Close connection
        cursor.close()
        conn.close()

        print("\n" + "=" * 80)
        print("[SUCCESS] Phase III rollback completed successfully!")
        print("=" * 80)

        return True

    except Exception as e:
        print(f"\n[ERROR] Rollback failed: {e}")
        return False


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "rollback":
        success = rollback_migration()
    else:
        success = run_migration()

    sys.exit(0 if success else 1)
