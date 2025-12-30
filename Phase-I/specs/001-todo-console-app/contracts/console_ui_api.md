# Module Contract: console_ui.py

**Module**: `src/console_ui.py`
**Purpose**: User interface (menu display, input handling, output formatting)
**Layer**: Presentation Layer

---

## Public API

### Function: display_menu

**Signature**:
```python
def display_menu() -> None
```

**Description**: Displays the main menu with 6 options.

**Parameters**: None

**Returns**: None

**Side Effects**: Prints to stdout

**Output Format**:
```
===== TODO APP =====
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Complete/Incomplete
6. Exit
====================
```

**Example**:
```python
display_menu()
# Prints menu to console
```

---

### Function: get_menu_choice

**Signature**:
```python
def get_menu_choice() -> int
```

**Description**: Prompts user for menu selection and validates input (1-6).

**Parameters**: None

**Returns**:
- `int`: Valid menu choice (1-6)

**Side Effects**:
- Prints prompt to stdout
- Reads from stdin
- Re-prompts on invalid input

**Validation**:
- Rejects non-numeric input
- Rejects numbers < 1 or > 6
- Loops until valid input received

**Error Messages**:
- Non-numeric: "Please enter a valid number"
- Out of range: "Please enter a number between 1-6"

**Example**:
```python
choice = get_menu_choice()
# User enters "3" → returns 3
# User enters "abc" → prints error, re-prompts
```

---

### Function: prompt_add_task

**Signature**:
```python
def prompt_add_task() -> None
```

**Description**: Prompts user for task details and calls `add_task()`. Displays success message.

**Parameters**: None

**Returns**: None

**Side Effects**:
- Reads title and description from stdin
- Calls `todo_manager.add_task()`
- Prints success message to stdout

**User Interaction Flow**:
1. Prompt: "Enter task title: "
2. Prompt: "Enter task description (optional, press Enter to skip): "
3. Validate and create task
4. Display: "Task added successfully! ID: {id}"

**Error Handling**:
- Catches `ValidationError` from `add_task()`
- Displays user-friendly error message
- Re-prompts for title on validation failure

**Example**:
```python
prompt_add_task()
# User enters title: "Buy groceries"
# User enters description: "Milk, eggs"
# Prints: "Task added successfully! ID: 1"
```

---

### Function: prompt_view_tasks

**Signature**:
```python
def prompt_view_tasks() -> None
```

**Description**: Retrieves and displays all tasks with statistics. No user input required.

**Parameters**: None

**Returns**: None

**Side Effects**:
- Calls `todo_manager.get_all_tasks()`
- Calls `todo_manager.get_task_statistics()`
- Prints task list and statistics to stdout

**Display Format** (with tasks):
```
===== ALL TASKS =====
[1] ✓ Buy groceries - Milk, eggs, bread
[2] ✗ Call dentist

Summary: 1 completed, 1 pending, 2 total
=====================
Press Enter to continue...
```

**Display Format** (no tasks):
```
No tasks found. Add some tasks!
Press Enter to continue...
```

**Task Display Format**:
- `[{id}] {status} {title}` (if no description)
- `[{id}] {status} {title} - {description}` (if description exists)
- Status symbols: ✓ (completed) or ✗ (incomplete)

**Example**:
```python
prompt_view_tasks()
# Displays all tasks with summary
# Waits for Enter keypress
```

---

### Function: prompt_update_task

**Signature**:
```python
def prompt_update_task() -> None
```

**Description**: Prompts user for task ID and new values, updates the task.

**Parameters**: None

**Returns**: None

**Side Effects**:
- Reads task ID, title, description from stdin
- Calls `todo_manager.get_task_by_id()` and `todo_manager.update_task()`
- Prints success message to stdout

**User Interaction Flow**:
1. Prompt: "Enter task ID to update: "
2. Display current task details
3. Prompt: "Enter new title (press Enter to keep '{current_title}'): "
4. Prompt: "Enter new description (press Enter to keep, '.' to clear): "
5. Update task
6. Display: "Task updated successfully!"

**Special Behavior**:
- Empty title input → keep current title
- Empty description input → keep current description
- Description "." → clear description (set to None)

**Error Handling**:
- Invalid ID type: "Please enter a valid number"
- Task not found: "Task with ID {id} not found"
- Validation errors: Display specific error message (title/description length)

**Example**:
```python
prompt_update_task()
# User enters ID: 1
# Shows: "Current: Buy groceries - Milk, eggs"
# User enters title: "" (keep current)
# User enters description: "Milk, eggs, bread, apples"
# Prints: "Task updated successfully!"
```

---

### Function: prompt_delete_task

**Signature**:
```python
def prompt_delete_task() -> None
```

**Description**: Prompts user for task ID and confirmation, deletes the task.

**Parameters**: None

**Returns**: None

**Side Effects**:
- Reads task ID and confirmation from stdin
- Calls `todo_manager.delete_task()`
- Prints success or cancellation message to stdout

**User Interaction Flow**:
1. Prompt: "Enter task ID to delete: "
2. Prompt: "Are you sure you want to delete this task? (y/n): "
3. If 'y': Delete and display "Task deleted successfully!"
4. If 'n': Display "Deletion cancelled"

**Confirmation Validation**:
- Accepts: 'y', 'Y', 'n', 'N' (case-insensitive)
- Rejects other input: "Please enter 'y' for yes or 'n' for no"
- Loops until valid confirmation received

**Error Handling**:
- Invalid ID type: "Please enter a valid number"
- Task not found: "Task with ID {id} not found"

**Example**:
```python
prompt_delete_task()
# User enters ID: 2
# User enters confirmation: "y"
# Prints: "Task deleted successfully!"
```

---

### Function: prompt_toggle_completion

**Signature**:
```python
def prompt_toggle_completion() -> None
```

**Description**: Prompts user for task ID and toggles its completion status.

**Parameters**: None

**Returns**: None

**Side Effects**:
- Reads task ID from stdin
- Calls `todo_manager.toggle_task_completion()`
- Prints success message with status change to stdout

**User Interaction Flow**:
1. Prompt: "Enter task ID to mark complete/incomplete: "
2. Toggle completion
3. Display: "Task marked as complete!" or "Task marked as incomplete!"

**Status-Specific Messages**:
- Toggled to complete: "Task marked as complete!"
- Toggled to incomplete: "Task marked as incomplete!"

**Error Handling**:
- Invalid ID type: "Please enter a valid number"
- Task not found: "Task with ID {id} not found"

**Example**:
```python
prompt_toggle_completion()
# User enters ID: 1
# Prints: "Task marked as complete!" (if was incomplete)
```

---

### Function: display_welcome

**Signature**:
```python
def display_welcome() -> None
```

**Description**: Displays welcome message on application startup.

**Parameters**: None

**Returns**: None

**Side Effects**: Prints to stdout

**Output Format**:
```
=====================================
   Welcome to Todo Console App!
   Phase I: In-Memory Task Manager
=====================================
Note: All data is stored in memory.
Data will be lost when you exit.
=====================================
```

**Example**:
```python
display_welcome()
# Prints welcome banner
```

---

### Function: display_goodbye

**Signature**:
```python
def display_goodbye() -> None
```

**Description**: Displays goodbye message on application exit.

**Parameters**: None

**Returns**: None

**Side Effects**: Prints to stdout

**Output Format**:
```
Goodbye!
```

**Example**:
```python
display_goodbye()
# Prints: "Goodbye!"
```

---

## Utility Functions

### Function: get_valid_integer

**Signature**:
```python
def get_valid_integer(prompt: str) -> int
```

**Description**: Helper function to get validated integer input from user.

**Parameters**:
- `prompt` (str): The prompt message to display

**Returns**:
- `int`: Valid integer entered by user

**Side Effects**:
- Prints prompt to stdout
- Reads from stdin
- Re-prompts on invalid input

**Error Handling**:
- Catches `ValueError` on non-numeric input
- Displays: "Please enter a valid number"
- Loops until valid integer received

**Example**:
```python
task_id = get_valid_integer("Enter task ID: ")
# User enters "5" → returns 5
# User enters "abc" → prints error, re-prompts
```

---

### Function: format_task_display

**Signature**:
```python
def format_task_display(task: Task) -> str
```

**Description**: Formats a task for display in the task list.

**Parameters**:
- `task` (Task): The task to format

**Returns**:
- `str`: Formatted task string

**Format**:
- With description: `[{id}] {status} {title} - {description}`
- Without description: `[{id}] {status} {title}`
- Status: ✓ if completed, ✗ if incomplete

**Example**:
```python
from src.models import Task
from datetime import datetime

task = Task(1, "Buy groceries", "Milk, eggs", False, datetime.now(), datetime.now())
display_str = format_task_display(task)
print(display_str)  # "[1] ✗ Buy groceries - Milk, eggs"
```

---

## Module Dependencies

**Imports**:
```python
from typing import Optional
from src.models import Task, ValidationError, TaskNotFoundError
from src import todo_manager
```

**Exports**:
- `display_menu` (function)
- `get_menu_choice` (function)
- `prompt_add_task` (function)
- `prompt_view_tasks` (function)
- `prompt_update_task` (function)
- `prompt_delete_task` (function)
- `prompt_toggle_completion` (function)
- `display_welcome` (function)
- `display_goodbye` (function)

---

## Usage Contract

### Consumers

This module is consumed by:
- `main.py`: Calls display and prompt functions to drive the application

### Guarantees

1. **Input Validation**: All user input validated before passing to business logic
2. **Error Translation**: Business logic exceptions converted to user-friendly messages
3. **Re-prompting**: Invalid input prompts user to retry (no crashes)
4. **Consistent Formatting**: All output follows consistent style and symbols

### Requirements

1. **Terminal Support**: Unicode symbols (✓/✗) must be supported
2. **Interactive Input**: Requires stdin/stdout (not suitable for batch/automated use)
3. **Error Handling**: Must catch all exceptions from `todo_manager` module

---

## Error Handling Contract

### Exception Translation Table

| Business Exception | User-Friendly Message |
|--------------------|-----------------------|
| `ValidationError("Title cannot be empty")` | "Title cannot be empty. Please enter a title." |
| `ValidationError("Title must be 100 characters or less")` | "Title must be 100 characters or less" |
| `ValidationError("Description must be 500 characters or less")` | "Description must be 500 characters or less" |
| `TaskNotFoundError(task_id)` | "Task with ID {task_id} not found" |
| `ValueError` (from int conversion) | "Please enter a valid number" |

### Re-prompt Strategy

- All input functions loop until valid input received
- Error messages displayed before re-prompt
- No function exits with invalid state

---

## Testing Contract

### Unit Tests Required

File: `tests/test_console_ui.py`

1. **format_task_display Tests**
   - Test: Format complete task with description
   - Assert: Contains ✓, title, description
   - Test: Format incomplete task without description
   - Assert: Contains ✗, title, no description separator

2. **get_valid_integer Tests** (with mocked input)
   - Test: Valid integer input
   - Assert: Returns integer
   - Test: Invalid input followed by valid
   - Assert: Re-prompts and returns valid integer

3. **Menu Display Tests**
   - Test: display_menu prints 6 options
   - Assert: Output contains all menu items

4. **Error Message Tests**
   - Test: ValidationError handling in prompt functions
   - Assert: User-friendly message displayed

**Note**: Testing interactive functions requires input mocking (e.g., `unittest.mock.patch` for `input()`)

---

## Performance Contract

### Constraints

- All display functions: O(1) time (except `prompt_view_tasks` which is O(n) for task list)
- Memory: O(1) per function call (except temporary task list display)

### User Experience

- Menu display: <100ms
- Task list display: <500ms for 10,000 tasks
- Input validation: Instant feedback on invalid input

---

## Accessibility Considerations

### Unicode Support

- Unicode symbols (✓/✗) required for status display
- Fallback plan (Phase II): ASCII symbols ([ ] [X]) if Unicode unavailable

### User Experience Standards

- Clear prompts for every input
- Immediate feedback on all operations
- Consistent error message format
- "Press Enter to continue" pause after long outputs

---

## Examples

### Example 1: Main UI Loop (from main.py)

```python
from src.console_ui import display_welcome, display_menu, get_menu_choice, display_goodbye
from src.console_ui import prompt_add_task, prompt_view_tasks, prompt_update_task
from src.console_ui import prompt_delete_task, prompt_toggle_completion

display_welcome()

while True:
    display_menu()
    choice = get_menu_choice()

    if choice == 1:
        prompt_add_task()
    elif choice == 2:
        prompt_view_tasks()
    elif choice == 3:
        prompt_update_task()
    elif choice == 4:
        prompt_delete_task()
    elif choice == 5:
        prompt_toggle_completion()
    elif choice == 6:
        display_goodbye()
        break
```

---

## Summary

`console_ui.py` provides:
- ✅ Complete user interface for all 5 CRUD operations
- ✅ Input validation with re-prompting
- ✅ Error translation (business exceptions → user messages)
- ✅ Consistent formatting with Unicode symbols
- ✅ Menu-driven workflow matching spec requirements
- ✅ Welcome and goodbye messages
- ✅ Task statistics display
- ✅ Confirmation prompts for destructive operations
