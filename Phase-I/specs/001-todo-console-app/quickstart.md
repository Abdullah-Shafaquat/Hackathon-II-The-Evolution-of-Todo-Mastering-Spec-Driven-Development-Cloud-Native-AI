# Quickstart Guide: Todo Console App - Phase I

**Feature**: 001-todo-console-app
**Date**: 2025-12-30
**Audience**: Developers implementing the Todo Console App

---

## Prerequisites

- **Python**: 3.13 or higher
- **Terminal**: Unicode-capable (Windows Terminal, macOS Terminal, Linux terminal)
- **No External Dependencies**: Only Python standard library required

---

## Project Setup

### 1. Directory Structure

Create the following structure:

```
todo-console-app/
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── todo_manager.py
│   └── console_ui.py
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_todo_manager.py
│   └── test_console_ui.py
└── README.md
```

### 2. Create Empty Files

**On Windows (PowerShell)**:
```powershell
# Create directories
New-Item -ItemType Directory -Path src, tests

# Create source files
New-Item -ItemType File -Path src\__init__.py, src\main.py, src\models.py, src\todo_manager.py, src\console_ui.py

# Create test files
New-Item -ItemType File -Path tests\__init__.py, tests\test_models.py, tests\test_todo_manager.py, tests\test_console_ui.py
```

**On macOS/Linux (Bash)**:
```bash
# Create directories
mkdir -p src tests

# Create source files
touch src/{__init__.py,main.py,models.py,todo_manager.py,console_ui.py}

# Create test files
touch tests/{__init__.py,test_models.py,test_todo_manager.py,test_console_ui.py}
```

---

## Implementation Order

Follow this sequence to build the application layer by layer:

### Phase 1: Data Layer (models.py)

**Goal**: Create Task data model with validation.

**Tasks**:
1. Import required modules: `dataclasses`, `datetime`, `typing`
2. Define custom exceptions: `ValidationError`, `TaskNotFoundError`
3. Create `Task` dataclass with 6 fields
4. Implement `__post_init__()` validation
5. Add validation helper methods

**Reference**: See `contracts/models_api.md` for complete API specification.

**Test**: Run `python -m pytest tests/test_models.py` (or use unittest)

---

### Phase 2: Business Logic (todo_manager.py)

**Goal**: Implement CRUD operations and ID generation.

**Tasks**:
1. Initialize global state: `tasks = []`, `next_id = 1`
2. Implement `add_task(title, description)` → Task
3. Implement `get_all_tasks()` → List[Task] (sorted newest first)
4. Implement `get_task_by_id(task_id)` → Task
5. Implement `update_task(task_id, title, description)` → Task
6. Implement `delete_task(task_id)` → None
7. Implement `toggle_task_completion(task_id)` → Task
8. Implement `get_task_statistics()` → Dict[str, int]

**Reference**: See `contracts/todo_manager_api.md` for complete API specification.

**Test**: Run `python -m pytest tests/test_todo_manager.py`

---

### Phase 3: Presentation Layer (console_ui.py)

**Goal**: Build user interface and input handling.

**Tasks**:
1. Implement `display_menu()` → None (print 6-option menu)
2. Implement `get_menu_choice()` → int (validate 1-6)
3. Implement `format_task_display(task)` → str (format with ✓/✗)
4. Implement `prompt_add_task()` → None
5. Implement `prompt_view_tasks()` → None
6. Implement `prompt_update_task()` → None
7. Implement `prompt_delete_task()` → None (with confirmation)
8. Implement `prompt_toggle_completion()` → None
9. Implement `display_welcome()` and `display_goodbye()`
10. Implement `get_valid_integer(prompt)` → int (helper)

**Reference**: See `contracts/console_ui_api.md` for complete API specification.

**Test**: Run `python -m pytest tests/test_console_ui.py` (requires input mocking)

---

### Phase 4: Application Layer (main.py)

**Goal**: Create entry point and main loop.

**Tasks**:
1. Import `signal`, `sys`, and `console_ui`
2. Implement `signal_handler(sig, frame)` for Ctrl+C
3. Implement `setup_signal_handlers()` → None
4. Implement `run_main_loop()` → None (infinite loop with dispatch)
5. Implement `main()` → None (orchestrate startup, loop, shutdown)
6. Add `if __name__ == "__main__": main()` block

**Reference**: See `contracts/main_api.md` for complete API specification.

**Test**: Manual testing (launch application and test all features)

---

## Running the Application

### Development Mode

```bash
# From project root
python -m src.main
```

### Production Mode (Future)

```bash
# Create executable (Phase II)
pyinstaller --onefile src/main.py
```

---

## Testing

### Run All Tests

**Using unittest** (stdlib):
```bash
python -m unittest discover -s tests -p "test_*.py"
```

**Using pytest** (if installed):
```bash
pytest tests/
```

### Run Specific Test File

```bash
python -m unittest tests.test_models
python -m unittest tests.test_todo_manager
python -m unittest tests.test_console_ui
```

### Test Coverage

```bash
# If coverage.py is installed
coverage run -m unittest discover
coverage report
coverage html  # Generate HTML report
```

**Target**: 100% coverage of basic functionality (per constitution)

---

## Manual Testing Checklist

Use this checklist after implementation to verify all features:

### Feature 1: Add Task
- [ ] Launch app, select option 1
- [ ] Add task with title only → Verify success message with ID
- [ ] Add task with title and description → Verify both stored
- [ ] Try empty title → Verify error and re-prompt
- [ ] Try 101-character title → Verify error
- [ ] Try 501-character description → Verify error

### Feature 2: View Tasks
- [ ] Select option 2 with no tasks → Verify "No tasks found" message
- [ ] Add 3 tasks (1 complete, 2 incomplete)
- [ ] Select option 2 → Verify all tasks shown with correct symbols (✓/✗)
- [ ] Verify summary shows "1 completed, 2 pending, 3 total"
- [ ] Verify tasks sorted newest first

### Feature 3: Update Task
- [ ] Select option 3, enter valid ID
- [ ] Update title only (press Enter for description) → Verify update
- [ ] Update description only (press Enter for title) → Verify update
- [ ] Clear description with "." → Verify description removed
- [ ] Try non-existent ID → Verify "Task not found" error

### Feature 4: Delete Task
- [ ] Select option 4, enter valid ID
- [ ] Confirm with 'y' → Verify deletion success
- [ ] Add another task and delete with 'n' → Verify cancellation
- [ ] Try invalid confirmation ('x') → Verify error and re-prompt
- [ ] Verify deleted ID is not reused (gap in sequence)

### Feature 5: Toggle Completion
- [ ] Select option 5, toggle incomplete task → Verify "marked as complete"
- [ ] Toggle same task again → Verify "marked as incomplete"
- [ ] View tasks to confirm status symbols updated (✓ ↔ ✗)

### Feature 6: Exit
- [ ] Select option 6 → Verify "Goodbye!" message and clean exit
- [ ] Press Ctrl+C during any operation → Verify "Goodbye!" and exit

### Error Handling
- [ ] Enter invalid menu choice (7, 0, -1, "abc") → Verify error message
- [ ] Enter invalid task ID (non-numeric) → Verify "Please enter a valid number"

---

## Development Tips

### Code Style

- **PEP 8**: Use `black` or `autopep8` for auto-formatting
- **Type Hints**: Add to all function signatures
- **Docstrings**: Use Google-style docstrings

Example:
```python
def add_task(title: str, description: Optional[str] = None) -> Task:
    """
    Create a new task with auto-generated ID and timestamps.

    Args:
        title: Task title (1-100 characters after trim)
        description: Optional description (max 500 characters)

    Returns:
        The newly created Task instance

    Raises:
        ValidationError: If title or description fail validation
    """
    # Implementation here
```

### Debugging

**Print Debugging**:
```python
# Temporary debug prints (remove before commit)
print(f"DEBUG: task_id={task_id}, tasks={tasks}")
```

**Interactive Debugging**:
```python
# Insert breakpoint
import pdb; pdb.set_trace()
```

### Common Pitfalls

1. **Forgetting to Trim Title**: Always `title.strip()` before validation
2. **Not Updating Timestamps**: Remember to set `updated_at = datetime.now()` on modifications
3. **ID Reuse**: Never decrement `next_id` or reuse deleted IDs
4. **Unicode Symbols**: Test on all platforms (Windows may have encoding issues)

---

## Troubleshooting

### Issue: Unicode Symbols Not Displaying

**Symptoms**: ✓/✗ appear as boxes or question marks

**Solutions**:
1. Use a modern terminal (Windows Terminal, iTerm2, GNOME Terminal)
2. Set terminal encoding to UTF-8
3. On Windows: Run `chcp 65001` before launching app

### Issue: "ModuleNotFoundError: No module named 'src'"

**Cause**: Running from wrong directory

**Solution**:
```bash
# Ensure you're in project root (todo-console-app/)
cd /path/to/todo-console-app
python -m src.main
```

### Issue: Tests Failing with Import Errors

**Cause**: Missing `__init__.py` files

**Solution**:
```bash
# Ensure __init__.py exists in src/ and tests/
touch src/__init__.py tests/__init__.py
```

---

## Next Steps

After completing Phase I implementation:

1. **Run Manual Tests**: Complete the manual testing checklist above
2. **Verify Acceptance Criteria**: Check all 25 scenarios from `spec.md`
3. **Code Review**: Ensure PEP 8 compliance, type hints, docstrings
4. **Commit**: Create git commit with message referencing task IDs
5. **Phase II Planning**: File persistence, configuration, advanced features

---

## Reference Documents

- **Feature Spec**: `specs/001-todo-console-app/spec.md`
- **Implementation Plan**: `specs/001-todo-console-app/plan.md`
- **Data Model**: `specs/001-todo-console-app/data-model.md`
- **Research**: `specs/001-todo-console-app/research.md`
- **API Contracts**:
  - `contracts/models_api.md`
  - `contracts/todo_manager_api.md`
  - `contracts/console_ui_api.md`
  - `contracts/main_api.md`

---

## Estimated Timeline

- **Phase 1 (Data Layer)**: 30 minutes
- **Phase 2 (Business Logic)**: 1 hour
- **Phase 3 (Presentation Layer)**: 1.5 hours
- **Phase 4 (Application Layer)**: 30 minutes
- **Testing & Debugging**: 1 hour
- **Total**: ~4.5 hours

**Note**: Times are estimates for experienced Python developers. Adjust based on your experience level.

---

## Success Criteria

Your implementation is complete when:

- ✅ All unit tests pass
- ✅ All manual test checklist items verified
- ✅ All 25 acceptance scenarios from spec.md work correctly
- ✅ Code follows PEP 8 with type hints and docstrings
- ✅ No runtime errors during normal operation
- ✅ Application starts in <2 seconds
- ✅ All operations respond in <1 second

**Ready to proceed to Phase II** when all criteria above are met.

---

## Support

For questions or issues during implementation:

1. Review the API contracts in `contracts/` directory
2. Check the feature specification in `spec.md`
3. Refer to research decisions in `research.md`
4. Consult the constitution at `.specify/memory/constitution.md`

**Remember**: This is Phase I (in-memory only). Persistence and advanced features are intentionally out of scope.
