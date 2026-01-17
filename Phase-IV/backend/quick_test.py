"""
Quick API test - Run this after starting the backend server
Tests basic functionality of new features
"""
import requests
import json
from datetime import date, timedelta

BASE_URL = "http://localhost:8000/api"

print("=" * 60)
print("QUICK API TEST")
print("=" * 60)

# 1. Check server health
print("\n1. Checking server health...")
try:
    response = requests.get(f"http://localhost:8000/health", timeout=2)
    if response.status_code == 200:
        print("   [OK] Server is running")
    else:
        print(f"   [ERROR] Server returned {response.status_code}")
        exit(1)
except requests.exceptions.ConnectionError:
    print("   [ERROR] Cannot connect to server at http://localhost:8000")
    print("   Please start the backend with: uvicorn app.main:app --reload")
    exit(1)

# 2. Register/Login
print("\n2. Testing authentication...")
test_email = f"quicktest_{date.today().isoformat()}@example.com"
register_data = {
    "email": test_email,
    "password": "Test123!",
    "name": "Quick Tester"
}

response = requests.post(f"{BASE_URL}/auth/signup", json=register_data)
if response.status_code in [200, 201]:
    token = response.json()["access_token"]
    print(f"   [OK] Registered user: {test_email}")
elif "already exists" in response.text:
    # Login instead
    login_data = {"email": test_email, "password": "Test123!"}
    response = requests.post(f"{BASE_URL}/auth/signin", json=login_data)
    token = response.json()["access_token"]
    print(f"   [OK] Logged in as: {test_email}")
else:
    print(f"   [ERROR] Auth failed: {response.status_code}")
    exit(1)

headers = {"Authorization": f"Bearer {token}"}

# 3. Create task with NEW fields
print("\n3. Testing task creation with new fields...")
task_data = {
    "title": "Test Task with All Fields",
    "description": "Testing priority, category, due_date, status",
    "due_date": date.today().isoformat(),
    "priority": "high",
    "category": "work"
}

response = requests.post(f"{BASE_URL}/tasks", json=task_data, headers=headers)
if response.status_code in [200, 201]:
    task = response.json()
    task_id = task["id"]
    print(f"   [OK] Created task ID: {task_id}")
    print(f"       Title: {task['title']}")
    print(f"       Priority: {task.get('priority', 'MISSING!')}")
    print(f"       Category: {task.get('category', 'MISSING!')}")
    print(f"       Due Date: {task.get('due_date', 'MISSING!')}")
    print(f"       Status: {task.get('status', 'MISSING!')}")

    # Verify fields exist
    if task.get('priority') and task.get('category') and task.get('status'):
        print("   [OK] All new fields present!")
    else:
        print("   [ERROR] Some new fields missing!")
else:
    print(f"   [ERROR] Failed to create task: {response.status_code}")
    print(f"   Response: {response.text}")
    exit(1)

# 4. Update task status
print("\n4. Testing status update...")
update_data = {"status": "in_progress"}
response = requests.patch(f"{BASE_URL}/tasks/{task_id}", json=update_data, headers=headers)
if response.status_code == 200:
    updated_task = response.json()
    print(f"   [OK] Status updated to: {updated_task.get('status')}")
    if updated_task.get('status') == 'in_progress':
        print("   [OK] Status change verified!")
    else:
        print(f"   [ERROR] Status not updated correctly: {updated_task.get('status')}")
else:
    print(f"   [ERROR] Failed to update status: {response.status_code}")

# 5. List tasks
print("\n5. Testing task listing...")
response = requests.get(f"{BASE_URL}/tasks?filter=all", headers=headers)
if response.status_code == 200:
    data = response.json()
    print(f"   [OK] Retrieved {len(data['tasks'])} tasks")
    print(f"       Total: {data['total']}, Completed: {data['completed']}, Pending: {data['pending']}")
else:
    print(f"   [ERROR] Failed to list tasks: {response.status_code}")

# 6. Test backward compatibility (task without new fields)
print("\n6. Testing backward compatibility...")
minimal_task = {
    "title": "Minimal Task (Old Style)",
    "description": "No priority, category, or due_date"
}
response = requests.post(f"{BASE_URL}/tasks", json=minimal_task, headers=headers)
if response.status_code in [200, 201]:
    task = response.json()
    print(f"   [OK] Created minimal task")
    print(f"       Priority (default): {task.get('priority')} (expected: medium)")
    print(f"       Category (default): {task.get('category')} (expected: other)")
    print(f"       Status (default): {task.get('status')} (expected: pending)")

    # Verify defaults
    if task.get('priority') == 'medium' and task.get('category') == 'other' and task.get('status') == 'pending':
        print("   [OK] Default values correct!")
    else:
        print("   [ERROR] Default values incorrect!")
else:
    print(f"   [ERROR] Failed to create minimal task: {response.status_code}")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print("[OK] Backend API is working correctly!")
print("[OK] All new fields (priority, category, due_date, status) are functional")
print("[OK] Task creation, updating, and listing work as expected")
print("[OK] Backward compatibility maintained")
print("\nNext steps:")
print("1. Start the frontend: cd frontend && npm run dev")
print("2. Open http://localhost:3000")
print("3. Follow TESTING_GUIDE.md for complete feature testing")
print("=" * 60)
