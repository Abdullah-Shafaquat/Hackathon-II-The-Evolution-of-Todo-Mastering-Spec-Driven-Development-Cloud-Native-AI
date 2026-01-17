"""
Quick Chat Diagnostic Script
Run this to test if everything is configured correctly
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("=" * 60)
print("CHAT DIAGNOSTICS - Checking Configuration")
print("=" * 60)

# 1. Check Python version
print("\n1. Python Version:")
print(f"   ✓ {sys.version}")

# 2. Check Database URL
print("\n2. Database URL:")
db_url = os.getenv("DATABASE_URL")
if db_url:
    # Hide password for security
    safe_url = db_url.split("@")[1] if "@" in db_url else "configured"
    print(f"   ✓ Database configured: ...@{safe_url}")
else:
    print("   ❌ DATABASE_URL not found in .env")
    print("   → Add: DATABASE_URL=postgresql://...")

# 3. Check OpenAI API Key
print("\n3. OpenAI API Key:")
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    print(f"   ✓ API Key configured: {api_key[:7]}...{api_key[-4:]}")
else:
    print("   ❌ OPENAI_API_KEY not found in .env")
    print("   → Add: OPENAI_API_KEY=sk-...")
    print("   → Get key from: https://platform.openai.com/api-keys")

# 4. Check OpenAI Model
print("\n4. OpenAI Model:")
model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
print(f"   ✓ Model: {model}")

# 5. Test OpenAI Connection
print("\n5. Testing OpenAI Connection:")
if api_key:
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)

        # Try a simple completion
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": "Say 'test successful'"}],
            max_tokens=10
        )
        print(f"   ✓ OpenAI API working: {response.choices[0].message.content}")
    except Exception as e:
        print(f"   ❌ OpenAI API error: {str(e)}")
        if "authentication" in str(e).lower() or "api_key" in str(e).lower():
            print("   → Check your API key is valid")
            print("   → Verify at: https://platform.openai.com/api-keys")
        elif "quota" in str(e).lower() or "billing" in str(e).lower():
            print("   → Check your OpenAI billing/credits")
            print("   → Visit: https://platform.openai.com/account/billing")
        elif "rate" in str(e).lower():
            print("   → Rate limit exceeded, wait a moment")
else:
    print("   ⚠ Skipped (no API key)")

# 6. Check Database Connection
print("\n6. Testing Database Connection:")
if db_url:
    try:
        import psycopg2
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        cursor.close()
        conn.close()
        print(f"   ✓ Database connected successfully")
    except Exception as e:
        print(f"   ❌ Database error: {str(e)}")
        print("   → Check your DATABASE_URL is correct")
        print("   → Verify database is running on Neon")
else:
    print("   ⚠ Skipped (no DATABASE_URL)")

# 7. Check Database Tables
print("\n7. Checking Database Tables:")
if db_url:
    try:
        import psycopg2
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()

        # Check for required tables
        cursor.execute("""
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        tables = [row[0] for row in cursor.fetchall()]

        required_tables = ['users', 'tasks', 'conversations', 'messages']
        for table in required_tables:
            if table in tables:
                print(f"   ✓ Table '{table}' exists")
            else:
                print(f"   ❌ Table '{table}' missing")
                print(f"   → Run migration: migrations/00X_*.sql")

        cursor.close()
        conn.close()
    except Exception as e:
        print(f"   ❌ Error checking tables: {str(e)}")
else:
    print("   ⚠ Skipped (no DATABASE_URL)")

# 8. Check Required Python Packages
print("\n8. Checking Python Packages:")
required_packages = [
    "fastapi",
    "uvicorn",
    "sqlmodel",
    "openai",
    "python-jose",
    "passlib",
    "python-dotenv"
]

for package in required_packages:
    try:
        __import__(package)
        print(f"   ✓ {package}")
    except ImportError:
        print(f"   ❌ {package} not installed")
        print(f"   → Run: pip install {package}")

print("\n" + "=" * 60)
print("DIAGNOSTICS COMPLETE")
print("=" * 60)

# Final recommendation
print("\nNext Steps:")
if not api_key:
    print("1. Add OPENAI_API_KEY to backend/.env")
    print("   Get from: https://platform.openai.com/api-keys")
if not db_url:
    print("2. Add DATABASE_URL to backend/.env")
    print("   Get from: https://console.neon.tech")
print("\n3. Restart backend server:")
print("   uvicorn app.main:app --reload")
print("\n4. Try chat again at: http://localhost:3000/chat")
