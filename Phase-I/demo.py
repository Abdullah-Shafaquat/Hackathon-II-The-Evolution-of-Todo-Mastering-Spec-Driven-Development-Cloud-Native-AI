"""Quick demo of the Todo Console App functionality"""

import sys
import io

# Fix Windows console encoding for Unicode symbols
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

from src import todo_manager
from src.console_ui import format_task_display

print("=" * 50)
print("TODO CONSOLE APP - QUICK DEMO")
print("=" * 50)

# Add some tasks
print("\n1. Adding tasks...")
task1 = todo_manager.add_task("Buy groceries", "Milk, eggs, bread")
task2 = todo_manager.add_task("Call dentist")
task3 = todo_manager.add_task("Finish project report", "Include charts and summary")

print(f"   ✓ Added task {task1.id}: {task1.title}")
print(f"   ✓ Added task {task2.id}: {task2.title}")
print(f"   ✓ Added task {task3.id}: {task3.title}")

# View all tasks
print("\n2. Viewing all tasks...")
all_tasks = todo_manager.get_all_tasks()
for task in all_tasks:
    print(f"   {format_task_display(task)}")

# Get statistics
stats = todo_manager.get_task_statistics()
print(f"\n   Summary: {stats['completed']} completed, {stats['pending']} pending, {stats['total']} total")

# Toggle completion
print("\n3. Marking task 2 as complete...")
todo_manager.toggle_task_completion(2)
task2_updated = todo_manager.get_task_by_id(2)
print(f"   {format_task_display(task2_updated)}")

# Update a task
print("\n4. Updating task 1...")
todo_manager.update_task(1, "Buy groceries and fruits", "Milk, eggs, bread, apples, oranges")
task1_updated = todo_manager.get_task_by_id(1)
print(f"   {format_task_display(task1_updated)}")

# Delete a task
print("\n5. Deleting task 3...")
todo_manager.delete_task(3)
print("   ✓ Task 3 deleted")

# View final state
print("\n6. Final task list...")
all_tasks = todo_manager.get_all_tasks()
for task in all_tasks:
    print(f"   {format_task_display(task)}")

stats = todo_manager.get_task_statistics()
print(f"\n   Summary: {stats['completed']} completed, {stats['pending']} pending, {stats['total']} total")

print("\n" + "=" * 50)
print("DEMO COMPLETE - All features working!")
print("=" * 50)
print("\nTo run the interactive app: python -m src.main")
