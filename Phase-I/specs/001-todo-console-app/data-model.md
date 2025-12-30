# Data Model: Todo Console App - Phase I

**Feature**: 001-todo-console-app
**Date**: 2025-12-30
**Phase**: Phase 1 - Design & Contracts

## Overview

This document defines the data model for the Todo Console App Phase I. The model consists of a single entity (Task) with validation rules derived from the feature specification.

---

## Entities

### Task

**Description**: Represents a single todo item with metadata for tracking creation, modification, and completion status.

**Fields**:

| Field | Type | Required | Constraints | Default | Description |
|-------|------|----------|-------------|---------|-------------|
| `id` | `int` | Yes | > 0, unique, sequential | Auto-generated | Unique identifier starting from 1 |
| `title` | `str` | Yes | 1-100 chars (after trim) | N/A | Task title/summary |
| `description` | `Optional[str]` | No | Max 500 chars | `None` | Optional detailed description |
| `completed` | `bool` | Yes | N/A | `False` | Completion status flag |
| `created_at` | `datetime` | Yes | Valid datetime | Auto-generated | Creation timestamp |
| `updated_at` | `datetime` | Yes | Valid datetime, >= created_at | Auto-generated | Last modification timestamp |

---

## Field Validation Rules

### ID Field
- **Type**: Positive integer
- **Generation**: Sequential starting from 1 (1, 2, 3, ...)
- **Uniqueness**: Must be unique across all tasks
- **Persistence**: IDs are never reused, even after deletion (gaps allowed)

**Validation**:
```python
assert id > 0, "Task ID must be positive"
assert id not in existing_ids, "Task ID must be unique"
```

---

### Title Field
- **Type**: Non-empty string
- **Length**: 1-100 characters (after whitespace trimming)
- **Whitespace**: Leading/trailing whitespace trimmed before validation
- **Whitespace-only**: Rejected (empty after trim)

**Validation**:
```python
title = title.strip()
assert len(title) > 0, "Title cannot be empty"
assert len(title) <= 100, "Title must be 100 characters or less"
```

**Error Messages** (from spec):
- Empty: "Title cannot be empty. Please enter a title."
- Too long: "Title must be 100 characters or less"

---

### Description Field
- **Type**: Optional string (can be None)
- **Length**: Maximum 500 characters (no trimming)
- **Empty String**: Treated as None
- **Special Input**: Period "." clears description (sets to None) during update

**Validation**:
```python
if description is not None:
    if description.strip() == "":
        description = None
    elif len(description) > 500:
        raise ValidationError("Description must be 500 characters or less")
```

**Error Messages**:
- Too long: "Description must be 500 characters or less"

---

### Completed Field
- **Type**: Boolean
- **Default**: `False` (new tasks are incomplete)
- **Toggle**: Can switch between True/False freely
- **Display**: Rendered as ✓ (True) or ✗ (False)

**Validation**:
```python
assert isinstance(completed, bool), "Completed must be boolean"
```

---

### Timestamp Fields (created_at, updated_at)
- **Type**: `datetime.datetime` object
- **Timezone**: Naive datetime (no timezone awareness in Phase I)
- **created_at**: Set once at task creation, never modified
- **updated_at**: Set at creation, updated on any modification (title, description, completed)

**Validation**:
```python
assert isinstance(created_at, datetime), "created_at must be datetime"
assert isinstance(updated_at, datetime), "updated_at must be datetime"
assert updated_at >= created_at, "updated_at cannot be before created_at"
```

**Auto-Update Triggers**:
- Task creation: Both set to `datetime.now()`
- Title update: `updated_at = datetime.now()`
- Description update: `updated_at = datetime.now()`
- Completion toggle: `updated_at = datetime.now()`

---

## State Transitions

### Task Lifecycle

```
[Non-existent]
     ↓
  [Create] → id=N, title="...", completed=False, created_at=now, updated_at=now
     ↓
  [Active]
     ↓
     ├── [Update Title/Description] → updated_at=now
     ├── [Toggle Completion] → completed=!completed, updated_at=now
     └── [Delete] → [Removed from list, ID never reused]
```

**Valid State Transitions**:

| From State | Action | To State | Side Effects |
|------------|--------|----------|--------------|
| Non-existent | Create | Active (incomplete) | ID assigned, timestamps set |
| Active | Update Title | Active | updated_at refreshed |
| Active | Update Description | Active | updated_at refreshed |
| Active | Toggle Complete | Active | completed flipped, updated_at refreshed |
| Active | Delete | Non-existent | Task removed, ID gap created |

**Invariants**:
- Once created, ID never changes
- created_at never changes after creation
- updated_at always >= created_at
- Deleted task IDs are never reused

---

## Data Storage

### In-Memory Structure

**Primary Storage**:
```python
tasks: List[Task] = []  # List of all active tasks
next_id: int = 1        # Counter for sequential ID generation
```

**Indexing Strategy** (Phase I):
- No indexing (linear search acceptable for scale)
- Find by ID: `O(n)` linear scan through list
- Find all: `O(1)` return entire list

**Sorting**:
- Display order: Sorted by `created_at` descending (newest first)
- Sorting method: Python's `sorted()` with key function
- Complexity: `O(n log n)` per view operation

```python
def get_all_tasks_sorted() -> List[Task]:
    return sorted(tasks, key=lambda t: t.created_at, reverse=True)
```

---

## Relationships

**Phase I has no relationships** - Task is a single, independent entity.

**Future Phases** (out of scope):
- Task → Category (many-to-one)
- Task → Tag (many-to-many)
- Task → User (many-to-one for multi-user support)
- Task → Subtask (self-referential hierarchy)

---

## Data Model Implementation

### Python Dataclass Definition

```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Task:
    """
    Represents a todo task with metadata.

    Attributes:
        id: Unique sequential identifier (> 0)
        title: Task title (1-100 characters after trim)
        description: Optional detailed description (max 500 chars)
        completed: Completion status (default False)
        created_at: Creation timestamp (immutable)
        updated_at: Last modification timestamp
    """
    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime

    def __post_init__(self) -> None:
        """Validate field constraints after initialization."""
        self._validate_id()
        self._validate_title()
        self._validate_description()
        self._validate_timestamps()

    def _validate_id(self) -> None:
        """Ensure ID is a positive integer."""
        if not isinstance(self.id, int) or self.id <= 0:
            raise ValueError("Task ID must be a positive integer")

    def _validate_title(self) -> None:
        """Ensure title meets length constraints."""
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty")
        if len(self.title) > 100:
            raise ValueError("Title must be 100 characters or less")

    def _validate_description(self) -> None:
        """Ensure description meets length constraints if present."""
        if self.description is not None and len(self.description) > 500:
            raise ValueError("Description must be 500 characters or less")

    def _validate_timestamps(self) -> None:
        """Ensure timestamp consistency."""
        if self.updated_at < self.created_at:
            raise ValueError("updated_at cannot be before created_at")
```

---

## Validation Error Handling

### Custom Exceptions

```python
class ValidationError(Exception):
    """Raised when task data fails validation."""
    pass

class TaskNotFoundError(Exception):
    """Raised when task ID does not exist."""
    pass
```

### Error Mapping (Business Logic → User Messages)

| Validation Rule | Internal Exception | User Error Message |
|-----------------|--------------------|--------------------|
| Empty title | `ValueError("Title cannot be empty")` | "Title cannot be empty. Please enter a title." |
| Title too long | `ValueError("Title must be 100 characters or less")` | "Title must be 100 characters or less" |
| Description too long | `ValueError("Description must be 500 characters or less")` | "Description must be 500 characters or less" |
| Task not found | `TaskNotFoundError(id)` | "Task with ID {id} not found" |
| Invalid ID type | `ValueError("...")` | "Please enter a valid number" |

---

## Data Model Testing

### Unit Test Coverage

**Test Cases** (to be implemented in `tests/test_models.py`):

1. **Valid Task Creation**
   - Create task with all fields
   - Create task with minimal fields (no description)
   - Verify auto-generated timestamps

2. **ID Validation**
   - Reject ID = 0
   - Reject ID < 0
   - Reject non-integer ID

3. **Title Validation**
   - Reject empty string
   - Reject whitespace-only string
   - Reject 101-character title
   - Accept 100-character title (boundary)
   - Accept 1-character title (boundary)
   - Trim leading/trailing whitespace

4. **Description Validation**
   - Accept None (no description)
   - Reject 501-character description
   - Accept 500-character description (boundary)
   - Accept empty string (converted to None)

5. **Timestamp Validation**
   - Reject updated_at < created_at
   - Accept updated_at = created_at
   - Accept updated_at > created_at

6. **Completed Flag**
   - Default to False
   - Accept True/False values

---

## Performance Characteristics

### Memory Footprint

**Single Task Estimate**:
- id: 28 bytes (int object)
- title: ~50-150 bytes (average string)
- description: ~0-500 bytes (optional)
- completed: 28 bytes (bool object)
- created_at: 48 bytes (datetime object)
- updated_at: 48 bytes (datetime object)

**Total per task**: ~200-800 bytes (varies with title/description length)

**Capacity Analysis**:
- 1,000 tasks: ~0.2-0.8 MB
- 10,000 tasks: ~2-8 MB (well within budget)

### Operation Complexity

| Operation | Time Complexity | Notes |
|-----------|-----------------|-------|
| Create Task | O(1) | Append to list |
| Find by ID | O(n) | Linear search |
| Update Task | O(n) | Find + modify |
| Delete Task | O(n) | Find + remove |
| Get All Sorted | O(n log n) | Sort operation |
| Validate Task | O(1) | Fixed-time checks |

**Scale Target**: All operations <1 second for n ≤ 10,000

---

## Summary

The Task data model is:
- **Simple**: Single entity with 6 fields
- **Validated**: Comprehensive constraints derived from spec
- **Testable**: Clear validation rules with expected error messages
- **Performant**: Suitable for target scale (10,000 tasks)
- **Extensible**: Can add relationships in future phases

**Phase 1 Data Model Complete** - Ready for contract generation.
