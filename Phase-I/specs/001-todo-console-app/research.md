# Research: Todo Console App - Phase I

**Feature**: 001-todo-console-app
**Date**: 2025-12-30
**Phase**: Phase 0 - Research & Design Validation

## Overview

This document resolves technical unknowns and establishes best practices for implementing the Todo Console App Phase I. All technical context items were already well-defined in the specification, so this research validates the chosen approaches.

## Technical Decisions

### Decision 1: Python Standard Library Only

**Decision**: Use Python 3.13+ standard library exclusively, no external dependencies.

**Rationale**:
- Simplicity: No dependency management or installation complexity
- Portability: Works anywhere Python 3.13+ is installed
- Phase I Scope: In-memory storage doesn't require advanced libraries
- Constitution Mandate: Explicitly required by project constitution

**Alternatives Considered**:
- **Rich/Textual**: Rejected - adds complexity and external dependency for minimal UX benefit in Phase I
- **Click/Typer**: Rejected - CLI framework overkill for simple menu-driven interface
- **Pydantic**: Rejected - validation can be implemented simply with native Python

**Libraries Selected**:
- `datetime`: For creation and update timestamps
- `typing`: For type hints (Optional, List, Dict)
- `signal`: For graceful Ctrl+C handling
- `unittest`: For testing framework

---

### Decision 2: In-Memory Storage with Python Lists

**Decision**: Store tasks in a Python list, use sequential counter for IDs.

**Rationale**:
- Simplicity: Single list of Task objects is straightforward
- Performance: List operations O(n) acceptable for target scale (10,000 tasks)
- ID Generation: Simple counter incremented on each add
- Constitution Mandate: In-memory only, no persistence required

**Alternatives Considered**:
- **Dictionary (ID → Task)**: Rejected - list is simpler and sorting by creation date is natural
- **SQLite**: Rejected - violates no-dependency constraint, overkill for Phase I
- **JSON Files**: Rejected - persistence is explicitly out of scope for Phase I

**Implementation Strategy**:
```python
tasks: List[Task] = []  # Global task list
next_id: int = 1        # Sequential ID counter
```

---

### Decision 3: Dataclass for Task Model

**Decision**: Use Python `@dataclass` decorator for Task model with validation methods.

**Rationale**:
- Built-in: Part of standard library (dataclasses module)
- Concise: Auto-generates `__init__`, `__repr__`, `__eq__`
- Type Safety: Works seamlessly with type hints
- Validation: Can add custom `__post_init__` for validation logic

**Alternatives Considered**:
- **Manual Class**: Rejected - more boilerplate code than dataclass
- **NamedTuple**: Rejected - immutability conflicts with update operations
- **Plain Dict**: Rejected - no type safety or validation

**Implementation Pattern**:
```python
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Task:
    id: int
    title: str
    description: Optional[str]
    completed: bool
    created_at: datetime
    updated_at: datetime

    def __post_init__(self):
        # Validation logic here
        pass
```

---

### Decision 4: Exception-Based Error Handling

**Decision**: Raise custom exceptions for validation errors, catch in UI layer for user messages.

**Rationale**:
- Separation of Concerns: Business logic raises exceptions, UI handles display
- Python Idiomatic: "Easier to ask forgiveness than permission" (EAFP)
- Clarity: Exception types document error conditions
- Testability: Easy to verify exceptions in unit tests

**Alternatives Considered**:
- **Return Codes/Tuples**: Rejected - less Pythonic, harder to enforce error handling
- **Result Type Pattern**: Rejected - requires additional abstraction, not standard library

**Implementation Strategy**:
- Custom exceptions: `ValidationError`, `TaskNotFoundError`
- UI layer catches and converts to user-friendly messages
- All user input validated before business logic execution

---

### Decision 5: Simple Menu Loop with Input Validation

**Decision**: Infinite loop with menu display, input(), validation, and action dispatch.

**Rationale**:
- Simplicity: Straightforward control flow, easy to understand
- Standard Pattern: Common approach for console applications
- User Experience: Clear menu after every operation as per spec

**Alternatives Considered**:
- **Command Parser**: Rejected - overkill for fixed 6-option menu
- **State Machine**: Rejected - unnecessary complexity for linear workflow

**Implementation Pattern**:
```python
def main():
    while True:
        display_menu()
        choice = get_validated_input()
        execute_action(choice)
```

---

### Decision 6: Unicode Symbols for Status Display

**Decision**: Use ✓ (U+2713) and ✗ (U+2717) for task completion status.

**Rationale**:
- Specification Requirement: Explicitly required by spec
- Visual Clarity: Instantly recognizable completion status
- Standard Support: Widely supported in modern terminals

**Alternatives Considered**:
- **ASCII Only ([ ] [X])**: Rejected - spec requires Unicode symbols
- **Emoji (✅ ❌)**: Rejected - less professional, potential rendering issues

**Risk Mitigation**:
- Document terminal requirements in README
- Test on Windows, macOS, Linux terminals
- Consider fallback to ASCII if issues arise in testing

---

### Decision 7: Testing Strategy

**Decision**: Use unittest framework with test files mirroring source structure.

**Rationale**:
- Standard Library: No external dependencies
- Comprehensive: Supports fixtures, assertions, test discovery
- Familiar: Widely known testing framework

**Test Coverage Plan**:
1. **test_models.py**: Task validation, field constraints, timestamp handling
2. **test_todo_manager.py**: CRUD operations, ID generation, error conditions
3. **test_console_ui.py**: Input validation, menu display, error message formatting

**Alternatives Considered**:
- **pytest**: Rejected - external dependency (violates constraints)
- **doctest**: Rejected - insufficient for comprehensive testing needs

---

## Best Practices

### Python 3.13+ Features to Utilize

1. **Type Hints**: Use for all function signatures
2. **Dataclasses**: For Task model definition
3. **F-strings**: For all string formatting
4. **Match Statement**: For menu action dispatch (if cleaner than if/elif)

### Code Quality Checklist

- ✅ PEP 8 compliance (enforced by review)
- ✅ Type hints on all functions
- ✅ Docstrings on all public functions (Google style)
- ✅ Meaningful variable names (no single-letter except loop counters)
- ✅ Max line length: 100 characters
- ✅ No dead code or commented-out code

### Error Message Standards

All error messages must be:
- **User-friendly**: No technical jargon or stack traces
- **Actionable**: Tell user what to do to fix the error
- **Consistent**: Same format and tone throughout

Examples:
- ❌ "ValueError: invalid literal for int()"
- ✅ "Please enter a valid number"

---

## Integration Patterns

### Module Interaction Flow

```
main.py (Entry Point)
    ↓
console_ui.py (Presentation Layer)
    ↓
todo_manager.py (Business Logic)
    ↓
models.py (Data Layer)
```

**Key Principles**:
- **One-way dependencies**: Upper layers depend on lower, never reverse
- **No circular imports**: Strict layering prevents cycles
- **Clear interfaces**: Each module exposes minimal public API

### Signal Handling for Ctrl+C

```python
import signal
import sys

def signal_handler(sig, frame):
    print("\nGoodbye!")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
```

---

## Performance Considerations

### Target Performance (from spec)

- Startup: <2 seconds
- Operations: <1 second each
- Capacity: Up to 10,000 tasks

### Implementation Notes

- **Linear Search**: Acceptable for Phase I scale (O(n) with n≤10,000)
- **Sorting**: Python's Timsort is O(n log n), performs well for this scale
- **Memory**: Each task ~200 bytes → 10,000 tasks = ~2MB (well under budget)

**Optimization Deferred to Future Phases**:
- Indexing/hashing for faster lookups
- Pagination for task list display
- Caching of sorted views

---

## Risk Mitigation

### Risk 1: Unicode Symbol Display Issues

**Mitigation**:
- Test on all target platforms (Windows/macOS/Linux)
- Document terminal requirements
- Consider ASCII fallback if issues discovered during testing

### Risk 2: User Accidentally Losing Data

**Mitigation**:
- Clear documentation that data is in-memory only
- Welcome message mentions data is not saved
- Exit confirmation (out of scope for Phase I, but noted for Phase II)

### Risk 3: Performance Degradation at Scale

**Mitigation**:
- Test with 10,000 tasks to verify performance
- Linear algorithms acceptable for target scale
- Future phases can optimize if needed

---

## Research Validation

All technical unknowns from Technical Context section have been resolved:

- ✅ **Language/Version**: Python 3.13+ confirmed
- ✅ **Dependencies**: Standard library modules identified (datetime, typing, signal, unittest)
- ✅ **Storage**: In-memory list with sequential ID strategy validated
- ✅ **Testing**: unittest selected and test structure defined
- ✅ **Performance**: Approach validated for target scale
- ✅ **Platform**: Cross-platform console compatibility confirmed

**Phase 0 Complete** - Ready to proceed to Phase 1 (Design & Contracts).
