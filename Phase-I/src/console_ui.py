"""User interface (menu display, input handling, output formatting)"""

from typing import Optional
from src.models import Task, ValidationError, TaskNotFoundError
from src import todo_manager


def prompt_add_task() -> None:
    """
    Prompt user for task details and call add_task() (T028).
    Display success message with task ID (T031).
    """
    print("\n=== Add New Task ===")

    # Prompt for title (T029)
    while True:
        title = input("Enter task title: ").strip()
        if not title:
            print("Title cannot be empty. Please enter a title.")
            continue

        # Prompt for description (T029)
        description = input("Enter task description (optional, press Enter to skip): ").strip()
        if not description:
            description = None

        # Attempt to create task with validation (T030)
        try:
            task = todo_manager.add_task(title, description)
            # Display success message (T031)
            print(f"\nTask added successfully! ID: {task.id}")
            break
        except ValidationError as e:
            # User-friendly error messages (T030)
            print(f"\nError: {e}")
            print("Please try again.\n")


def format_task_display(task: Task) -> str:
    """
    Format a task for display in the task list (T043).

    Args:
        task: The task to format

    Returns:
        Formatted task string with status symbol, ID, title, description
    """
    # Status symbol: ✓ for complete, ✗ for incomplete (T043)
    status = "✓" if task.completed else "✗"

    # Format with or without description (T044)
    if task.description:
        return f"[{task.id}] {status} {task.title} - {task.description}"
    else:
        return f"[{task.id}] {status} {task.title}"


def prompt_view_tasks() -> None:
    """
    Retrieve and display all tasks with statistics (T045).
    """
    print("\n===== ALL TASKS =====")

    # Get all tasks sorted newest-first
    all_tasks = todo_manager.get_all_tasks()

    # Handle empty list (T046)
    if not all_tasks:
        print("No tasks found. Add some tasks!")
    else:
        # Display task list with formatting (T047)
        for task in all_tasks:
            print(format_task_display(task))

        # Display summary statistics (T048)
        stats = todo_manager.get_task_statistics()
        print(f"\nSummary: {stats['completed']} completed, {stats['pending']} pending, {stats['total']} total")

    print("=====================")

    # Pause before returning to menu (T049)
    input("\nPress Enter to continue...")


def get_valid_integer(prompt: str) -> int:
    """
    Helper to get validated integer input from user (T067).

    Args:
        prompt: The prompt message to display

    Returns:
        Valid integer entered by user
    """
    while True:
        try:
            value = int(input(prompt))
            return value
        except ValueError:
            print("Please enter a valid number")


def prompt_update_task() -> None:
    """
    Prompt user for task ID and new values, update the task (T068).
    """
    print("\n=== Update Task ===")

    try:
        # Get task ID (T067)
        task_id = get_valid_integer("Enter task ID to update: ")

        # Get current task to display values (T069)
        task = todo_manager.get_task_by_id(task_id)
        print(f"\nCurrent task: {format_task_display(task)}")

        # Prompt for new values with hints (T070)
        new_title = input(f"Enter new title (press Enter to keep '{task.title}'): ")
        new_description = input("Enter new description (press Enter to keep, '.' to clear): ")

        # Update task
        if not new_title:
            new_title = None
        if not new_description:
            new_description = None

        todo_manager.update_task(task_id, new_title, new_description)
        print("\nTask updated successfully!")  # T072

    except TaskNotFoundError as e:
        print(f"\nError: {e}")  # T071
    except ValidationError as e:
        print(f"\nError: {e}")


def prompt_delete_task() -> None:
    """
    Prompt user for task ID and confirmation, delete the task (T082).
    """
    print("\n=== Delete Task ===")

    try:
        # Get task ID
        task_id = get_valid_integer("Enter task ID to delete: ")

        # Get confirmation (T083, T084)
        while True:
            confirmation = input("Are you sure you want to delete this task? (y/n): ").strip().lower()
            if confirmation in ['y', 'yes']:
                todo_manager.delete_task(task_id)
                print("\nTask deleted successfully!")  # T085
                break
            elif confirmation in ['n', 'no']:
                print("\nDeletion cancelled")  # T086
                break
            else:
                print("Please enter 'y' for yes or 'n' for no")  # T084

    except TaskNotFoundError as e:
        print(f"\nError: {e}")  # T087


def prompt_toggle_completion() -> None:
    """
    Prompt user for task ID and toggle its completion status (T100).
    """
    print("\n=== Mark Complete/Incomplete ===")

    try:
        # Get task ID (T101)
        task_id = get_valid_integer("Enter task ID to mark complete/incomplete: ")

        # Toggle completion
        task = todo_manager.toggle_task_completion(task_id)

        # Display appropriate message (T102, T103)
        if task.completed:
            print("\nTask marked as complete!")
        else:
            print("\nTask marked as incomplete!")

    except TaskNotFoundError as e:
        print(f"\nError: {e}")  # T104


def display_menu() -> None:
    """Display the main menu with 6 options (T106)."""
    print("\n===== TODO APP =====")
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Complete/Incomplete")
    print("6. Exit")
    print("====================")


def get_menu_choice() -> int:
    """
    Prompt user for menu selection and validate input (1-6) (T107).

    Returns:
        Valid menu choice (1-6)
    """
    while True:
        try:
            choice = int(input("\nEnter your choice (1-6): "))
            if 1 <= choice <= 6:
                return choice
            else:
                print("Please enter a number between 1-6")
        except ValueError:
            print("Please enter a valid number")


def display_welcome() -> None:
    """Display welcome message on application startup (T108)."""
    print("=" * 50)
    print("   Welcome to Todo Console App!")
    print("   Phase I: In-Memory Task Manager")
    print("=" * 50)
    print("Note: All data is stored in memory.")
    print("Data will be lost when you exit.")
    print("=" * 50)


def display_goodbye() -> None:
    """Display goodbye message on application exit (T109)."""
    print("\nGoodbye!")
