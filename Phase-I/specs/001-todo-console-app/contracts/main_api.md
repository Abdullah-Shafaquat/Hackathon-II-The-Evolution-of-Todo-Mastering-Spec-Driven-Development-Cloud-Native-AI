# Module Contract: main.py

**Module**: `src/main.py`
**Purpose**: Application entry point and main loop orchestration
**Layer**: Application Layer

---

## Public API

### Function: main

**Signature**:
```python
def main() -> None
```

**Description**: Entry point for the Todo Console App. Initializes signal handling and runs the main event loop.

**Parameters**: None

**Returns**: None

**Side Effects**:
- Registers Ctrl+C signal handler
- Runs infinite loop (exits on user choice 6 or Ctrl+C)
- Calls functions from `console_ui` module
- Calls functions from `todo_manager` module indirectly (via UI)

**Flow**:
1. Register signal handler for Ctrl+C (SIGINT)
2. Display welcome message
3. Enter main loop:
   - Display menu
   - Get user choice
   - Dispatch to appropriate handler
   - Repeat until exit choice (6)
4. Display goodbye message
5. Exit cleanly

**Example**:
```python
if __name__ == "__main__":
    main()
```

---

### Function: setup_signal_handlers

**Signature**:
```python
def setup_signal_handlers() -> None
```

**Description**: Registers signal handler for graceful Ctrl+C exit.

**Parameters**: None

**Returns**: None

**Side Effects**:
- Registers SIGINT handler
- Handler prints "Goodbye!" and exits with code 0

**Signal Handling**:
```python
def signal_handler(sig, frame):
    print("\nGoodbye!")
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
```

**Example**:
```python
setup_signal_handlers()
# User presses Ctrl+C → prints "Goodbye!" and exits gracefully
```

---

### Function: run_main_loop

**Signature**:
```python
def run_main_loop() -> None
```

**Description**: Infinite loop that displays menu, gets user input, and dispatches actions.

**Parameters**: None

**Returns**: None (exits via `break` on choice 6 or exception)

**Side Effects**:
- Calls `console_ui.display_menu()`
- Calls `console_ui.get_menu_choice()`
- Dispatches to action handlers based on choice
- Breaks loop on exit choice (6)

**Action Dispatch**:
```python
menu_actions = {
    1: console_ui.prompt_add_task,
    2: console_ui.prompt_view_tasks,
    3: console_ui.prompt_update_task,
    4: console_ui.prompt_delete_task,
    5: console_ui.prompt_toggle_completion,
    6: None  # Exit
}
```

**Example**:
```python
run_main_loop()
# Infinite loop until user selects option 6 or presses Ctrl+C
```

---

## Module Structure

### Execution Flow

```
main()
  ├── setup_signal_handlers()
  │     └── Registers Ctrl+C handler
  ├── console_ui.display_welcome()
  ├── run_main_loop()
  │     ├── console_ui.display_menu()
  │     ├── console_ui.get_menu_choice()
  │     └── Dispatch to action (1-6)
  │           ├── 1: console_ui.prompt_add_task()
  │           ├── 2: console_ui.prompt_view_tasks()
  │           ├── 3: console_ui.prompt_update_task()
  │           ├── 4: console_ui.prompt_delete_task()
  │           ├── 5: console_ui.prompt_toggle_completion()
  │           └── 6: break (exit loop)
  └── console_ui.display_goodbye()
```

---

## Module Dependencies

**Imports**:
```python
import sys
import signal
from src import console_ui
```

**Entry Point**:
```python
if __name__ == "__main__":
    main()
```

---

## Usage Contract

### Execution

**Command**:
```bash
python -m src.main
# or
python src/main.py
```

**Platform Support**:
- Windows: ✅ (with PowerShell or Command Prompt)
- macOS: ✅ (with Terminal)
- Linux: ✅ (with any shell)

**Requirements**:
- Python 3.13+
- Unicode-capable terminal (for ✓/✗ symbols)

---

## Error Handling Contract

### Uncaught Exceptions

**Strategy**: Let exceptions bubble up to terminate the program with traceback (debug mode).

**Rationale**:
- User-facing errors handled in `console_ui` layer
- System errors (e.g., out of memory) should terminate visibly
- Phase I focuses on happy path; comprehensive error handling deferred to Phase II

### Signal Handling

**SIGINT (Ctrl+C)**:
- Handler: Prints "\nGoodbye!" and exits cleanly
- Exit code: 0 (success)
- No cleanup needed (in-memory data intentionally discarded)

**Other Signals** (Phase I):
- Not handled (default behavior applies)
- Phase II may add SIGTERM handling for graceful shutdown

---

## Testing Contract

### Unit Tests

File: `tests/test_main.py`

**Note**: Testing `main()` requires significant mocking (signal, sys.exit, console_ui calls). May be deferred to integration tests.

**Recommended Tests**:
1. **Test: Signal handler setup**
   - Mock `signal.signal`
   - Assert: SIGINT handler registered

2. **Test: Main loop dispatch**
   - Mock `console_ui` functions
   - Provide sequence of menu choices
   - Assert: Correct functions called in order

3. **Test: Exit on choice 6**
   - Mock menu choice to return 6
   - Assert: Loop breaks, goodbye displayed

### Integration Tests

**Manual Testing Checklist** (from constitution):
- Launch application
- Verify welcome message displays
- Select each menu option (1-6) and verify correct behavior
- Press Ctrl+C and verify "Goodbye!" message
- Verify application exits cleanly

---

## Performance Contract

### Startup Time

- Target: <2 seconds (per spec SC-005)
- Actual: <100ms expected (minimal initialization)

### Main Loop

- Menu display: <100ms
- Action dispatch: <10ms (delegated to UI layer)
- Overall responsiveness: <1 second per operation

---

## Phase I Scope

### In Scope

- ✅ Main event loop with menu dispatch
- ✅ Graceful Ctrl+C handling
- ✅ Welcome and goodbye messages
- ✅ Integration of all 5 CRUD operations

### Out of Scope (Future Phases)

- ❌ Configuration file loading
- ❌ Command-line arguments (e.g., `--help`, `--version`)
- ❌ Logging framework
- ❌ Exception handling middleware
- ❌ Multi-user session management
- ❌ Persistence initialization

---

## Code Example

### Complete main.py Implementation (Conceptual)

```python
"""
Todo Console App - Main Entry Point

Phase I: In-Memory Task Manager
"""

import sys
import signal
from src import console_ui


def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully."""
    print("\nGoodbye!")
    sys.exit(0)


def setup_signal_handlers() -> None:
    """Register signal handlers for graceful shutdown."""
    signal.signal(signal.SIGINT, signal_handler)


def run_main_loop() -> None:
    """Run the main application loop."""
    while True:
        console_ui.display_menu()
        choice = console_ui.get_menu_choice()

        if choice == 1:
            console_ui.prompt_add_task()
        elif choice == 2:
            console_ui.prompt_view_tasks()
        elif choice == 3:
            console_ui.prompt_update_task()
        elif choice == 4:
            console_ui.prompt_delete_task()
        elif choice == 5:
            console_ui.prompt_toggle_completion()
        elif choice == 6:
            break  # Exit loop


def main() -> None:
    """Main entry point for Todo Console App."""
    setup_signal_handlers()
    console_ui.display_welcome()
    run_main_loop()
    console_ui.display_goodbye()


if __name__ == "__main__":
    main()
```

---

## Architectural Role

### Responsibilities

- **Orchestration**: Coordinates UI and business logic layers
- **Lifecycle Management**: Handles startup, main loop, shutdown
- **Signal Handling**: Intercepts system signals for graceful exit
- **Entry Point**: Provides `if __name__ == "__main__"` execution

### Non-Responsibilities (Delegated)

- ❌ User input validation → `console_ui`
- ❌ Business logic → `todo_manager`
- ❌ Data modeling → `models`
- ❌ Display formatting → `console_ui`

### Layering Compliance

```
main.py (Application Layer)
   ↓
console_ui.py (Presentation Layer)
   ↓
todo_manager.py (Business Logic Layer)
   ↓
models.py (Data Layer)
```

**Key Principle**: `main.py` only depends on `console_ui`, never directly on `todo_manager` or `models`.

---

## Summary

`main.py` provides:
- ✅ Clean application entry point
- ✅ Graceful Ctrl+C handling with "Goodbye!" message (per spec FR-017)
- ✅ Main event loop with menu dispatch
- ✅ Minimal coupling (only imports `console_ui` and stdlib)
- ✅ Cross-platform compatibility
- ✅ <2 second startup time (exceeds target)
- ✅ Clear separation from business logic and UI layers
