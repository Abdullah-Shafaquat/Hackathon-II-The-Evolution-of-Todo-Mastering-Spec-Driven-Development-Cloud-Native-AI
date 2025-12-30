# Module Contract: models.py

**Module**: `src/models.py`
**Purpose**: Task data model and validation
**Layer**: Data Layer

---

## Public API

### Class: Task

**Description**: Dataclass representing a todo task with validation.

**Constructor**:
```python
def __init__(
    self,
    id: int,
    title: str,
    description: Optional[str],
    completed: bool,
    created_at: datetime,
    updated_at: datetime
) -> None
```

**Parameters**:
- `id` (int): Unique positive integer identifier
- `title` (str): Non-empty string, 1-100 characters (after trim)
- `description` (Optional[str]): Optional string, max 500 characters (None allowed)
- `completed` (bool): Completion status (True = complete, False = incomplete)
- `created_at` (datetime): Creation timestamp
- `updated_at` (datetime): Last modification timestamp

**Raises**:
- `ValueError`: If any field fails validation

**Validation Rules**:
1. `id > 0` (positive integer)
2. `title.strip()` is non-empty and ≤ 100 chars
3. `description` is None or ≤ 500 chars
4. `updated_at >= created_at`

**Example**:
```python
from datetime import datetime
from src.models import Task

task = Task(
    id=1,
    title="Buy groceries",
    description="Milk, eggs, bread",
    completed=False,
    created_at=datetime.now(),
    updated_at=datetime.now()
)
```

---

### Exception: ValidationError

**Description**: Custom exception for task validation failures.

**Base Class**: `Exception`

**Usage**:
```python
class ValidationError(Exception):
    """Raised when task data fails validation."""
    pass
```

**When Raised**:
- Invalid title length or content
- Invalid description length
- Invalid ID value
- Timestamp inconsistencies

---

### Exception: TaskNotFoundError

**Description**: Custom exception for task lookup failures.

**Base Class**: `Exception`

**Constructor**:
```python
def __init__(self, task_id: int) -> None
```

**Attributes**:
- `task_id` (int): The ID that was not found

**Usage**:
```python
class TaskNotFoundError(Exception):
    """Raised when task ID does not exist."""
    def __init__(self, task_id: int) -> None:
        self.task_id = task_id
        super().__init__(f"Task with ID {task_id} not found")
```

---

## Module Dependencies

**Imports**:
```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
```

**Exports**:
- `Task` (class)
- `ValidationError` (exception)
- `TaskNotFoundError` (exception)

---

## Type Signatures

```python
# Public API type signatures
Task: type
ValidationError: type[Exception]
TaskNotFoundError: type[Exception]

# Task attributes (read-only after creation, except via todo_manager)
Task.id: int
Task.title: str
Task.description: Optional[str]
Task.completed: bool
Task.created_at: datetime
Task.updated_at: datetime
```

---

## Usage Contract

### Consumers

This module is consumed by:
- `todo_manager.py`: Creates and validates Task instances
- `console_ui.py`: Reads Task attributes for display

### Guarantees

1. **Immutability**: Task instances are created with valid data; modification handled by `todo_manager`
2. **Validation**: All constraints checked in `__post_init__`
3. **No Side Effects**: Task creation does not modify global state

### Requirements

1. **Python Version**: 3.13+ (uses dataclass from stdlib)
2. **No External Dependencies**: Uses only Python standard library

---

## Error Handling Contract

### Validation Errors

| Condition | Exception | Message Template |
|-----------|-----------|------------------|
| ID ≤ 0 | `ValueError` | "Task ID must be a positive integer" |
| Empty title | `ValueError` | "Title cannot be empty" |
| Title > 100 chars | `ValueError` | "Title must be 100 characters or less" |
| Description > 500 chars | `ValueError` | "Description must be 500 characters or less" |
| updated_at < created_at | `ValueError` | "updated_at cannot be before created_at" |

**Caller Responsibility**: Catch `ValueError` and convert to user-friendly messages in UI layer.

---

## Testing Contract

### Unit Tests Required

File: `tests/test_models.py`

1. **Valid Task Creation**
   - Test: Create task with all fields
   - Test: Create task with minimal fields (description=None)
   - Assert: No exceptions raised, all fields match input

2. **ID Validation**
   - Test: Create task with ID=0
   - Assert: Raises `ValueError`
   - Test: Create task with ID=-1
   - Assert: Raises `ValueError`

3. **Title Validation**
   - Test: Create task with title=""
   - Assert: Raises `ValueError`
   - Test: Create task with title=" " (whitespace only)
   - Assert: Raises `ValueError`
   - Test: Create task with 101-character title
   - Assert: Raises `ValueError`
   - Test: Create task with 100-character title
   - Assert: Success (boundary test)

4. **Description Validation**
   - Test: Create task with description=None
   - Assert: Success
   - Test: Create task with 501-character description
   - Assert: Raises `ValueError`
   - Test: Create task with 500-character description
   - Assert: Success (boundary test)

5. **Timestamp Validation**
   - Test: Create task with updated_at < created_at
   - Assert: Raises `ValueError`
   - Test: Create task with updated_at = created_at
   - Assert: Success

6. **Completed Flag**
   - Test: Create task with completed=False
   - Assert: Success, completed attribute is False
   - Test: Create task with completed=True
   - Assert: Success, completed attribute is True

---

## Performance Contract

### Constraints

- **Instantiation**: O(1) time complexity
- **Validation**: O(1) time complexity (fixed-time checks)
- **Memory**: ~200-800 bytes per instance (varies with title/description length)

### Scale Guarantees

- Supports creation of 10,000+ instances without performance degradation
- Validation time independent of number of existing tasks

---

## Backward Compatibility

**Version**: 1.0 (Phase I)

**Future Compatibility Notes**:
- Phase II may add fields (e.g., priority, due_date, tags)
- Phase II may add methods (e.g., to_dict(), from_dict() for serialization)
- Current fields will not change signature in minor versions

---

## Examples

### Example 1: Valid Task Creation

```python
from datetime import datetime
from src.models import Task

now = datetime.now()
task = Task(
    id=1,
    title="Buy groceries",
    description="Milk, eggs, bread",
    completed=False,
    created_at=now,
    updated_at=now
)

print(task.title)  # "Buy groceries"
print(task.completed)  # False
```

### Example 2: Task with No Description

```python
from datetime import datetime
from src.models import Task

now = datetime.now()
task = Task(
    id=2,
    title="Call dentist",
    description=None,
    completed=False,
    created_at=now,
    updated_at=now
)

print(task.description)  # None
```

### Example 3: Validation Error

```python
from datetime import datetime
from src.models import Task

now = datetime.now()

try:
    task = Task(
        id=3,
        title="",  # Empty title (invalid)
        description=None,
        completed=False,
        created_at=now,
        updated_at=now
    )
except ValueError as e:
    print(e)  # "Title cannot be empty"
```

---

## Summary

`models.py` provides:
- ✅ Immutable Task data structure with validation
- ✅ Custom exceptions for error handling
- ✅ Type-safe with comprehensive type hints
- ✅ No dependencies beyond Python stdlib
- ✅ O(1) creation and validation
- ✅ Clear error messages for all validation failures
