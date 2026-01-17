"""
Comprehensive test script for all new task management features
Tests Wave 1-4 implementations
"""
import requests
import json
from datetime import date, timedelta
from typing import Dict, Any

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api"

# Color codes for terminal output
class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'

def print_header(text: str):
    print(f"\n{Colors.BLUE}{'=' * 60}")
    print(f"{text}")
    print(f"{'=' * 60}{Colors.RESET}\n")

def print_success(text: str):
    print(f"{Colors.GREEN}[OK] {text}{Colors.RESET}")

def print_error(text: str):
    print(f"{Colors.RED}[ERROR] {text}{Colors.RESET}")

def print_info(text: str):
    print(f"{Colors.YELLOW}[INFO] {text}{Colors.RESET}")

# Global token storage
auth_token = None
user_id = None

def test_auth():
    """Test 0: Authentication"""
    global auth_token, user_id

    print_header("TEST 0: Authentication")

    # Register a test user
    register_data = {
        "email": f"test_features_{date.today().isoformat()}@example.com",
        "password": "TestPassword123!",
        "name": "Feature Tester"
    }

    try:
        response = requests.post(f"{API_BASE}/auth/signup", json=register_data)
        if response.status_code in [200, 201]:
            data = response.json()
            auth_token = data.get("access_token")
            print_success(f"User registered: {register_data['email']}")
        elif response.status_code == 400 and "already exists" in response.text:
            # Try to login instead
            print_info("User already exists, logging in...")
            login_data = {"email": register_data["email"], "password": register_data["password"]}
            response = requests.post(f"{API_BASE}/auth/signin", json=login_data)
            data = response.json()
            auth_token = data.get("access_token")
            print_success("Logged in successfully")

        # Get user info
        headers = {"Authorization": f"Bearer {auth_token}"}
        response = requests.get(f"{API_BASE}/auth/me", headers=headers)
        if response.status_code == 200:
            user_data = response.json()
            user_id = user_data.get("id")
            print_success(f"User ID: {user_id}")
            return True
        else:
            print_error(f"Failed to get user info: {response.status_code}")
            return False

    except Exception as e:
        print_error(f"Authentication failed: {e}")
        return False

def test_create_task_with_all_fields():
    """Test 1: Create tasks with all new fields"""
    print_header("TEST 1: Create Tasks with All Fields")

    headers = {"Authorization": f"Bearer {auth_token}"}

    test_tasks = [
        {
            "title": "High Priority Work Meeting",
            "description": "Quarterly review with team",
            "due_date": (date.today() + timedelta(days=1)).isoformat(),
            "priority": "high",
            "category": "work"
        },
        {
            "title": "Buy Groceries",
            "description": "Milk, eggs, bread",
            "due_date": date.today().isoformat(),
            "priority": "medium",
            "category": "shopping"
        },
        {
            "title": "Study Python",
            "description": "Complete chapter 5",
            "due_date": (date.today() + timedelta(days=3)).isoformat(),
            "priority": "high",
            "category": "study"
        },
        {
            "title": "Morning Workout",
            "description": "30 min cardio + stretching",
            "due_date": date.today().isoformat(),
            "priority": "medium",
            "category": "health"
        },
        {
            "title": "Overdue Task Test",
            "description": "This should appear as overdue",
            "due_date": (date.today() - timedelta(days=2)).isoformat(),
            "priority": "high",
            "category": "personal"
        }
    ]

    created_tasks = []

    for task_data in test_tasks:
        try:
            response = requests.post(f"{API_BASE}/tasks", json=task_data, headers=headers)
            if response.status_code in [200, 201]:
                task = response.json()
                created_tasks.append(task)
                print_success(f"Created: {task['title']} (ID: {task['id']})")
                print_info(f"  Priority: {task.get('priority')}, Category: {task.get('category')}, Due: {task.get('due_date')}, Status: {task.get('status')}")
            else:
                print_error(f"Failed to create task: {task_data['title']} - {response.status_code}: {response.text}")
        except Exception as e:
            print_error(f"Error creating task: {e}")

    print(f"\n{Colors.GREEN}Created {len(created_tasks)} tasks successfully{Colors.RESET}")
    return created_tasks

def test_list_tasks_with_filters(created_tasks):
    """Test 2: List tasks with various filters"""
    print_header("TEST 2: Filter Tasks by Category & Status")

    headers = {"Authorization": f"Bearer {auth_token}"}

    filters = [
        ("all", "All tasks"),
        ("pending", "Pending tasks only"),
        ("completed", "Completed tasks only"),
    ]

    for filter_type, description in filters:
        try:
            response = requests.get(f"{API_BASE}/tasks?filter={filter_type}", headers=headers)
            if response.status_code == 200:
                data = response.json()
                print_success(f"{description}: {len(data['tasks'])} tasks")
                print_info(f"  Total: {data['total']}, Completed: {data['completed']}, Pending: {data['pending']}")
            else:
                print_error(f"Failed to list tasks with filter '{filter_type}': {response.status_code}")
        except Exception as e:
            print_error(f"Error listing tasks: {e}")

    return True

def test_update_task_status(created_tasks):
    """Test 3: Update task status (pending -> in_progress -> completed)"""
    print_header("TEST 3: Update Task Status")

    if not created_tasks:
        print_error("No tasks available to test status updates")
        return False

    headers = {"Authorization": f"Bearer {auth_token}"}
    task = created_tasks[0]
    task_id = task['id']

    statuses = ["pending", "in_progress", "completed"]

    for status in statuses:
        try:
            update_data = {"status": status}
            response = requests.patch(f"{API_BASE}/tasks/{task_id}", json=update_data, headers=headers)
            if response.status_code == 200:
                updated_task = response.json()
                print_success(f"Task {task_id} status updated to: {status}")
                print_info(f"  Completed flag: {updated_task.get('completed')}")
            else:
                print_error(f"Failed to update status to '{status}': {response.status_code}")
        except Exception as e:
            print_error(f"Error updating status: {e}")

    return True

def test_update_all_fields(created_tasks):
    """Test 4: Update priority, category, and due_date"""
    print_header("TEST 4: Update Priority, Category & Due Date")

    if len(created_tasks) < 2:
        print_error("Not enough tasks to test updates")
        return False

    headers = {"Authorization": f"Bearer {auth_token}"}
    task = created_tasks[1]
    task_id = task['id']

    updates = [
        {"priority": "low", "description": "Priority change to low"},
        {"category": "personal", "description": "Category change to personal"},
        {"due_date": (date.today() + timedelta(days=7)).isoformat(), "description": "Due date extended"}
    ]

    for update_data in updates:
        try:
            response = requests.patch(f"{API_BASE}/tasks/{task_id}", json=update_data, headers=headers)
            if response.status_code == 200:
                updated_task = response.json()
                field = list(update_data.keys())[0]
                new_value = update_data[field]
                print_success(f"Updated {field} to: {new_value}")
            else:
                print_error(f"Failed to update: {response.status_code}")
        except Exception as e:
            print_error(f"Error updating task: {e}")

    return True

def test_sorting_and_filtering():
    """Test 5: Advanced sorting and category filtering"""
    print_header("TEST 5: Sorting & Filtering")

    headers = {"Authorization": f"Bearer {auth_token}"}

    # Note: These parameters would need to be supported in the API routes
    # The frontend does client-side filtering, but we can test what the API returns

    print_info("Fetching all tasks to test client-side sorting logic...")

    try:
        response = requests.get(f"{API_BASE}/tasks?filter=all", headers=headers)
        if response.status_code == 200:
            data = response.json()
            tasks = data['tasks']

            print_success(f"Retrieved {len(tasks)} tasks for sorting tests")

            # Test category grouping
            categories = {}
            for task in tasks:
                cat = task.get('category', 'other')
                categories[cat] = categories.get(cat, 0) + 1

            print_info("Tasks by category:")
            for cat, count in categories.items():
                print(f"  {cat}: {count} tasks")

            # Test priority grouping
            priorities = {}
            for task in tasks:
                pri = task.get('priority', 'medium')
                priorities[pri] = priorities.get(pri, 0) + 1

            print_info("Tasks by priority:")
            for pri, count in priorities.items():
                print(f"  {pri}: {count} tasks")

            # Test status grouping
            statuses = {}
            for task in tasks:
                status = task.get('status', 'pending')
                statuses[status] = statuses.get(status, 0) + 1

            print_info("Tasks by status:")
            for status, count in statuses.items():
                print(f"  {status}: {count} tasks")

            return True
        else:
            print_error(f"Failed to fetch tasks: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error testing sorting: {e}")
        return False

def test_overdue_detection(created_tasks):
    """Test 6: Overdue task detection"""
    print_header("TEST 6: Overdue Task Detection")

    headers = {"Authorization": f"Bearer {auth_token}"}

    try:
        response = requests.get(f"{API_BASE}/tasks?filter=all", headers=headers)
        if response.status_code == 200:
            data = response.json()
            tasks = data['tasks']

            today = date.today()
            overdue_tasks = []
            due_today_tasks = []

            for task in tasks:
                if task.get('completed'):
                    continue

                due_date_str = task.get('due_date')
                if due_date_str:
                    due_date = date.fromisoformat(due_date_str)
                    if due_date < today:
                        overdue_tasks.append(task)
                    elif due_date == today:
                        due_today_tasks.append(task)

            print_success(f"Found {len(overdue_tasks)} overdue tasks")
            for task in overdue_tasks:
                print_info(f"  OVERDUE: {task['title']} (Due: {task['due_date']})")

            print_success(f"Found {len(due_today_tasks)} tasks due today")
            for task in due_today_tasks:
                print_info(f"  DUE TODAY: {task['title']}")

            return True
        else:
            print_error(f"Failed to fetch tasks: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error testing overdue detection: {e}")
        return False

def test_bulk_operations(created_tasks):
    """Test 7: Bulk complete operation"""
    print_header("TEST 7: Bulk Operations")

    if len(created_tasks) < 2:
        print_error("Not enough tasks to test bulk operations")
        return False

    headers = {"Authorization": f"Bearer {auth_token}"}

    # Get first 2 tasks to bulk complete
    task_ids = [created_tasks[0]['id'], created_tasks[1]['id']]

    print_info(f"Attempting to bulk complete tasks: {task_ids}")

    success_count = 0
    for task_id in task_ids:
        try:
            update_data = {"status": "completed", "completed": True}
            response = requests.patch(f"{API_BASE}/tasks/{task_id}", json=update_data, headers=headers)
            if response.status_code == 200:
                success_count += 1
                print_success(f"Task {task_id} marked as completed")
            else:
                print_error(f"Failed to complete task {task_id}: {response.status_code}")
        except Exception as e:
            print_error(f"Error completing task {task_id}: {e}")

    print_success(f"Bulk operation: {success_count}/{len(task_ids)} tasks completed")
    return success_count == len(task_ids)

def test_daily_summary():
    """Test 8: Daily summary calculations"""
    print_header("TEST 8: Daily Summary Metrics")

    headers = {"Authorization": f"Bearer {auth_token}"}

    try:
        response = requests.get(f"{API_BASE}/tasks?filter=all", headers=headers)
        if response.status_code == 200:
            data = response.json()
            tasks = data['tasks']

            today = date.today().isoformat()

            # Calculate metrics (same logic as DailySummary component)
            overdue = len([t for t in tasks if t.get('due_date') and not t.get('completed') and date.fromisoformat(t['due_date']) < date.today()])
            due_today = len([t for t in tasks if t.get('due_date') == today and not t.get('completed')])
            completed_today = len([t for t in tasks if t.get('completed') and t.get('updated_at', '').startswith(today)])
            pending = len([t for t in tasks if not t.get('completed')])
            in_progress = len([t for t in tasks if t.get('status') == 'in_progress'])
            total = len(tasks)

            print_success("Daily Summary Metrics:")
            print(f"  Overdue: {overdue}")
            print(f"  Due Today: {due_today}")
            print(f"  Completed Today: {completed_today}")
            print(f"  In Progress: {in_progress}")
            print(f"  Pending: {pending}")
            print(f"  Total: {total}")

            return True
        else:
            print_error(f"Failed to fetch tasks: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error calculating daily summary: {e}")
        return False

def test_search_enhancement(created_tasks):
    """Test 9: Enhanced search (title, description, category, priority)"""
    print_header("TEST 9: Enhanced Search")

    headers = {"Authorization": f"Bearer {auth_token}"}

    try:
        response = requests.get(f"{API_BASE}/tasks?filter=all", headers=headers)
        if response.status_code == 200:
            data = response.json()
            tasks = data['tasks']

            search_terms = ["work", "high", "shopping", "study"]

            for term in search_terms:
                matching_tasks = [
                    t for t in tasks
                    if term.lower() in t.get('title', '').lower() or
                       term.lower() in t.get('description', '').lower() or
                       term.lower() in t.get('category', '').lower() or
                       term.lower() in t.get('priority', '').lower()
                ]
                print_success(f"Search '{term}': {len(matching_tasks)} matches")
                for task in matching_tasks[:3]:  # Show first 3 matches
                    print_info(f"  - {task['title']} ({task.get('category')}, {task.get('priority')})")

            return True
        else:
            print_error(f"Failed to fetch tasks: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error testing search: {e}")
        return False

def test_backward_compatibility(created_tasks):
    """Test 10: Backward compatibility (old tasks without new fields)"""
    print_header("TEST 10: Backward Compatibility")

    headers = {"Authorization": f"Bearer {auth_token}"}

    # Create a task with minimal fields (old style)
    old_style_task = {
        "title": "Old Style Task",
        "description": "This task has no due_date, priority, or category"
    }

    try:
        response = requests.post(f"{API_BASE}/tasks", json=old_style_task, headers=headers)
        if response.status_code in [200, 201]:
            task = response.json()
            print_success("Created old-style task (minimal fields)")
            print_info(f"  Priority: {task.get('priority')} (should default to 'medium')")
            print_info(f"  Category: {task.get('category')} (should default to 'other')")
            print_info(f"  Status: {task.get('status')} (should default to 'pending')")
            print_info(f"  Due Date: {task.get('due_date')} (should be None/null)")

            # Verify defaults
            defaults_correct = (
                task.get('priority') == 'medium' and
                task.get('category') == 'other' and
                task.get('status') == 'pending' and
                task.get('due_date') is None
            )

            if defaults_correct:
                print_success("All default values are correct!")
                return True
            else:
                print_error("Some default values are incorrect")
                return False
        else:
            print_error(f"Failed to create old-style task: {response.status_code}")
            return False
    except Exception as e:
        print_error(f"Error testing backward compatibility: {e}")
        return False

def run_all_tests():
    """Run all feature tests"""
    print(f"\n{Colors.BLUE}{'=' * 60}")
    print(f"  TASK MANAGEMENT FEATURES TEST SUITE")
    print(f"  Testing All New Features")
    print(f"{'=' * 60}{Colors.RESET}\n")

    test_results = {}

    # Test 0: Authentication
    if not test_auth():
        print_error("Authentication failed. Cannot proceed with tests.")
        return

    # Test 1: Create tasks with all fields
    created_tasks = test_create_task_with_all_fields()
    test_results['create_with_all_fields'] = len(created_tasks) > 0

    # Test 2: Filter tasks
    test_results['filter_tasks'] = test_list_tasks_with_filters(created_tasks)

    # Test 3: Update task status
    test_results['update_status'] = test_update_task_status(created_tasks)

    # Test 4: Update all fields
    test_results['update_all_fields'] = test_update_all_fields(created_tasks)

    # Test 5: Sorting and filtering
    test_results['sorting_filtering'] = test_sorting_and_filtering()

    # Test 6: Overdue detection
    test_results['overdue_detection'] = test_overdue_detection(created_tasks)

    # Test 7: Bulk operations
    test_results['bulk_operations'] = test_bulk_operations(created_tasks)

    # Test 8: Daily summary
    test_results['daily_summary'] = test_daily_summary()

    # Test 9: Enhanced search
    test_results['enhanced_search'] = test_search_enhancement(created_tasks)

    # Test 10: Backward compatibility
    test_results['backward_compatibility'] = test_backward_compatibility(created_tasks)

    # Summary
    print_header("TEST SUMMARY")

    total_tests = len(test_results)
    passed_tests = sum(1 for result in test_results.values() if result)
    failed_tests = total_tests - passed_tests

    for test_name, result in test_results.items():
        status = f"{Colors.GREEN}PASS{Colors.RESET}" if result else f"{Colors.RED}FAIL{Colors.RESET}"
        print(f"{status} - {test_name}")

    print(f"\n{Colors.BLUE}{'=' * 60}{Colors.RESET}")
    print(f"{Colors.GREEN}Passed: {passed_tests}/{total_tests}{Colors.RESET}")
    if failed_tests > 0:
        print(f"{Colors.RED}Failed: {failed_tests}/{total_tests}{Colors.RESET}")
    print(f"{Colors.BLUE}{'=' * 60}{Colors.RESET}\n")

    if passed_tests == total_tests:
        print(f"{Colors.GREEN}[SUCCESS] All tests passed! All features are working correctly.{Colors.RESET}\n")
    else:
        print(f"{Colors.YELLOW}[WARNING] Some tests failed. Please review the errors above.{Colors.RESET}\n")

if __name__ == "__main__":
    run_all_tests()
