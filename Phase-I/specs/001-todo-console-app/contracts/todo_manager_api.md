# Module Contract: todo_manager.py

**Module**: `src/todo_manager.py`
**Purpose**: Business logic for CRUD operations on tasks
**Layer**: Business Logic Layer

---

## Public API

### Function: add_task

**Signature**:
```python
def add_task(title: str, description: Optional[str] = None) -> Task
```

**Description**: Creates a new task with auto-generated ID and timestamps.

**Parameters**:
- `title` (str): Task title (will be trimmed, must be 1-100 chars after trim)
- `description` (Optional[str]): Optional description (max 500 chars), defaults to None

**Returns**:
- `Task`: The newly created task with assigned ID and timestamps

**Raises**:
- `ValidationError`: If title is empty (after trim) or > 100 chars
- `ValidationError`: If description > 500 chars

**Side Effects**:
- Increments global `next_id` counter
- Appends task to global `tasks` list

**Example**:
```python
task = add_task("Buy groceries", "Milk, eggs, bread")
print(task.id)  # 1 (auto-generated)
```

---

### Function: get_all_tasks

**Signature**:
```python
def get_all_tasks() -> List[Task]
```

**Description**: Returns all tasks sorted by creation date (newest first).

**Parameters**: None

**Returns**:
- `List[Task]`: All tasks in descending order by `created_at`

**Raises**: None (returns empty list if no tasks)

**Side Effects**: None (read-only operation)

**Example**:
```python
tasks = get_all_tasks()
for task in tasks:
    print(task.title)
```

---

### Function: get_task_by_id

**Signature**:
```python
def get_task_by_id(task_id: int) -> Task
```

**Description**: Retrieves a task by its unique ID.

**Parameters**:
- `task_id` (int): The ID of the task to retrieve

**Returns**:
- `Task`: The task with matching ID

**Raises**:
- `TaskNotFoundError`: If no task exists with the given ID

**Side Effects**: None (read-only operation)

**Example**:
```python
try:
    task = get_task_by_id(1)
    print(task.title)
except TaskNotFoundError:
    print("Task not found")
```

---

### Function: update_task

**Signature**:
```python
def update_task(
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None
) -> Task
```

**Description**: Updates a task's title and/or description, refreshing the `updated_at` timestamp.

**Parameters**:
- `task_id` (int): The ID of the task to update
- `title` (Optional[str]): New title (None = keep current), will be trimmed
- `description` (Optional[str]): New description (None = keep current, "." = clear to None)

**Returns**:
- `Task`: The updated task

**Raises**:
- `TaskNotFoundError`: If no task exists with the given ID
- `ValidationError`: If new title is empty or > 100 chars
- `ValidationError`: If new description > 500 chars

**Side Effects**:
- Modifies task in global `tasks` list
- Updates `updated_at` to current time

**Special Behavior**:
- If `description == "."`, sets description to None (clears it)
- If `title is None`, keeps existing title unchanged
- If `description is None`, keeps existing description unchanged

**Example**:
```python
# Update only title
task = update_task(1, title="Buy groceries and fruits")

# Update only description
task = update_task(1, description="Milk, eggs, bread, apples")

# Clear description
task = update_task(1, description=".")

# Update both
task = update_task(1, title="Shopping", description="Weekly groceries")
```

---

### Function: delete_task

**Signature**:
```python
def delete_task(task_id: int) -> None
```

**Description**: Deletes a task by ID. The ID is never reused.

**Parameters**:
- `task_id` (int): The ID of the task to delete

**Returns**: None

**Raises**:
- `TaskNotFoundError`: If no task exists with the given ID

**Side Effects**:
- Removes task from global `tasks` list
- ID is never reused (gap in sequence)

**Example**:
```python
delete_task(2)
# Task with ID 2 is removed
# Future tasks will still get IDs 3, 4, 5... (2 is never reused)
```

---

### Function: toggle_task_completion

**Signature**:
```python
def toggle_task_completion(task_id: int) -> Task
```

**Description**: Toggles a task's completion status and updates the `updated_at` timestamp.

**Parameters**:
- `task_id` (int): The ID of the task to toggle

**Returns**:
- `Task`: The updated task with toggled `completed` status

**Raises**:
- `TaskNotFoundError`: If no task exists with the given ID

**Side Effects**:
- Modifies task's `completed` field (True → False or False → True)
- Updates `updated_at` to current time

**Example**:
```python
task = toggle_task_completion(1)
print(task.completed)  # True (was False) or False (was True)
```

---

### Function: get_task_statistics

**Signature**:
```python
def get_task_statistics() -> Dict[str, int]
```

**Description**: Computes summary statistics for all tasks.

**Parameters**: None

**Returns**:
- `Dict[str, int]`: Dictionary with keys "total", "completed", "pending"

**Raises**: None

**Side Effects**: None (read-only operation)

**Return Value**:
```python
{
    "total": 10,      # Total number of tasks
    "completed": 3,   # Number of completed tasks (completed=True)
    "pending": 7      # Number of pending tasks (completed=False)
}
```

**Example**:
```python
stats = get_task_statistics()
print(f"{stats['completed']} completed, {stats['pending']} pending, {stats['total']} total")
```

---

## Module State

### Global Variables

```python
tasks: List[Task] = []  # List of all active tasks
next_id: int = 1        # Sequential ID counter (never decrements)
```

**State Guarantees**:
- `next_id` always increments (never reused, even after deletion)
- `tasks` contains only valid Task instances
- IDs in `tasks` are unique

---

## Module Dependencies

**Imports**:
```python
from datetime import datetime
from typing import List, Optional, Dict
from src.models import Task, ValidationError, TaskNotFoundError
```

**Exports**:
- `add_task` (function)
- `get_all_tasks` (function)
- `get_task_by_id` (function)
- `update_task` (function)
- `delete_task` (function)
- `toggle_task_completion` (function)
- `get_task_statistics` (function)

---

## Usage Contract

### Consumers

This module is consumed by:
- `console_ui.py`: Calls CRUD functions based on user actions
- `main.py`: May call initialization functions if needed

### Guarantees

1. **ID Uniqueness**: IDs are unique and sequential (1, 2, 3, ...), never reused
2. **Timestamp Management**: `created_at` set once, `updated_at` refreshed on modifications
3. **Atomic Operations**: Each function completes fully or raises exception (no partial updates)
4. **Sorted Output**: `get_all_tasks()` always returns tasks sorted newest-first

### Requirements

1. **Input Validation**: Callers must catch `ValidationError` and `TaskNotFoundError`
2. **Whitespace Handling**: Titles are trimmed before validation
3. **Description Clearing**: Use `description="."` to clear description during update

---

## Error Handling Contract

### Exception Mapping

| Function | Error Condition | Exception | User Message (UI Layer) |
|----------|-----------------|-----------|--------------------------|
| `add_task` | Empty title | `ValidationError` | "Title cannot be empty. Please enter a title." |
| `add_task` | Title > 100 chars | `ValidationError` | "Title must be 100 characters or less" |
| `add_task` | Description > 500 chars | `ValidationError` | "Description must be 500 characters or less" |
| `update_task` | Task not found | `TaskNotFoundError` | "Task with ID {id} not found" |
| `update_task` | Empty title | `ValidationError` | "Title cannot be empty. Please enter a title." |
| `update_task` | Title > 100 chars | `ValidationError` | "Title must be 100 characters or less" |
| `update_task` | Description > 500 chars | `ValidationError` | "Description must be 500 characters or less" |
| `delete_task` | Task not found | `TaskNotFoundError` | "Task with ID {id} not found" |
| `toggle_task_completion` | Task not found | `TaskNotFoundError` | "Task with ID {id} not found" |
| `get_task_by_id` | Task not found | `TaskNotFoundError` | "Task with ID {id} not found" |

---

## Testing Contract

### Unit Tests Required

File: `tests/test_todo_manager.py`

1. **add_task Tests**
   - Test: Add task with title only
   - Assert: ID=1, title set, description=None, completed=False
   - Test: Add task with title and description
   - Assert: Both fields set correctly
   - Test: Add multiple tasks
   - Assert: IDs increment (1, 2, 3)
   - Test: Add task with empty title
   - Assert: Raises `ValidationError`

2. **get_all_tasks Tests**
   - Test: Get tasks from empty list
   - Assert: Returns empty list []
   - Test: Get tasks after adding 3 tasks
   - Assert: Returns 3 tasks, sorted newest-first

3. **get_task_by_id Tests**
   - Test: Get existing task by ID
   - Assert: Returns correct task
   - Test: Get non-existent ID
   - Assert: Raises `TaskNotFoundError`

4. **update_task Tests**
   - Test: Update title only
   - Assert: Title changed, description unchanged, updated_at refreshed
   - Test: Update description only
   - Assert: Description changed, title unchanged, updated_at refreshed
   - Test: Clear description with "."
   - Assert: Description becomes None
   - Test: Update non-existent task
   - Assert: Raises `TaskNotFoundError`

5. **delete_task Tests**
   - Test: Delete existing task
   - Assert: Task removed, total count decreased
   - Test: Delete task and verify ID not reused
   - Assert: Next task gets higher ID, gap remains
   - Test: Delete non-existent task
   - Assert: Raises `TaskNotFoundError`

6. **toggle_task_completion Tests**
   - Test: Toggle incomplete → complete
   - Assert: completed=True, updated_at refreshed
   - Test: Toggle complete → incomplete
   - Assert: completed=False, updated_at refreshed
   - Test: Toggle non-existent task
   - Assert: Raises `TaskNotFoundError`

7. **get_task_statistics Tests**
   - Test: Statistics with no tasks
   - Assert: {total: 0, completed: 0, pending: 0}
   - Test: Statistics with 3 tasks (1 complete, 2 pending)
   - Assert: {total: 3, completed: 1, pending: 2}

---

## Performance Contract

### Complexity

| Function | Time Complexity | Notes |
|----------|-----------------|-------|
| `add_task` | O(1) | Append to list |
| `get_all_tasks` | O(n log n) | Sort operation |
| `get_task_by_id` | O(n) | Linear search |
| `update_task` | O(n) | Linear search + update |
| `delete_task` | O(n) | Linear search + remove |
| `toggle_task_completion` | O(n) | Linear search + update |
| `get_task_statistics` | O(n) | Single pass count |

### Scale Guarantees

- All operations complete in <1 second for n ≤ 10,000 tasks
- Memory usage: O(n) proportional to number of tasks

---

## Concurrency Contract

**Phase I**: Single-threaded, no concurrency support required.

**Future Phases**: May require locking/threading for multi-user support.

---

## Examples

### Example 1: Complete CRUD Workflow

```python
from src.todo_manager import add_task, get_all_tasks, update_task, delete_task, toggle_task_completion

# Create
task1 = add_task("Buy groceries", "Milk, eggs, bread")
task2 = add_task("Call dentist")

# Read
all_tasks = get_all_tasks()
print(f"Total tasks: {len(all_tasks)}")  # 2

# Update
update_task(1, title="Buy groceries and fruits")

# Toggle completion
toggle_task_completion(1)

# Delete
delete_task(2)

# Verify
remaining_tasks = get_all_tasks()
print(f"Remaining tasks: {len(remaining_tasks)}")  # 1
```

### Example 2: Error Handling

```python
from src.todo_manager import add_task, get_task_by_id
from src.models import ValidationError, TaskNotFoundError

# Validation error
try:
    task = add_task("")  # Empty title
except ValidationError as e:
    print(f"Error: {e}")  # "Title cannot be empty"

# Not found error
try:
    task = get_task_by_id(999)
except TaskNotFoundError as e:
    print(f"Error: {e}")  # "Task with ID 999 not found"
```

---

## Summary

`todo_manager.py` provides:
- ✅ Complete CRUD operations for Task entities
- ✅ Sequential ID generation with gap tolerance
- ✅ Automatic timestamp management
- ✅ Sorted task retrieval (newest first)
- ✅ Task statistics computation
- ✅ Comprehensive error handling with custom exceptions
- ✅ O(n) operations acceptable for target scale (10,000 tasks)
