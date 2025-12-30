# Todo Console App - Phase I

A console-based todo application built with Python 3.13+ standard library only, featuring in-memory storage.

## Features

✅ **5 Core Operations:**
1. **Add Task** - Create tasks with title and optional description
2. **View Tasks** - Display all tasks with ✓/✗ status symbols and statistics
3. **Update Task** - Modify task title and/or description
4. **Delete Task** - Remove tasks with confirmation prompt
5. **Toggle Complete** - Mark tasks as complete/incomplete

## Requirements

- Python 3.13 or higher
- No external dependencies (uses Python standard library only)
- Unicode-capable terminal (for ✓/✗ symbols)

## Installation

1. Clone or download this repository
2. Navigate to the project directory:
```bash
cd todo-console-app
```

## Usage

Run the application:

```bash
python -m src.main
```

Or:

```bash
python src/main.py
```

### Features in Action

**Welcome Screen:**
```
==================================================
   Welcome to Todo Console App!
   Phase I: In-Memory Task Manager
==================================================
Note: All data is stored in memory.
Data will be lost when you exit.
==================================================
```

**Main Menu:**
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

**Task Display Format:**
```
[1] ✗ Buy groceries - Milk, eggs, bread
[2] ✓ Call dentist
[3] ✗ Finish report

Summary: 1 completed, 2 pending, 3 total
```

## Testing

Run all unit tests:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

Run specific test modules:

```bash
python -m unittest tests.test_models
python -m unittest tests.test_todo_manager
python -m unittest tests.test_console_ui
```

## Project Structure

```
todo-console-app/
├── src/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # Application entry point
│   ├── models.py            # Task data model and validation
│   ├── todo_manager.py      # Business logic (CRUD operations)
│   └── console_ui.py        # User interface (menu and I/O)
├── tests/
│   ├── __init__.py
│   ├── test_models.py       # Unit tests for Task model
│   ├── test_todo_manager.py # Unit tests for CRUD operations
│   └── test_console_ui.py   # Unit tests for UI functions
├── specs/                   # Feature specifications and design docs
├── .gitignore
└── README.md
```

## Technical Details

### Architecture

**Layered Design:**
- **Data Layer** (`models.py`): Task dataclass with validation
- **Business Logic** (`todo_manager.py`): CRUD operations and ID management
- **Presentation Layer** (`console_ui.py`): User interface and input handling
- **Application Layer** (`main.py`): Entry point and main loop

### Data Model

**Task Entity:**
- `id` (int): Unique sequential identifier (1, 2, 3...)
- `title` (str): Required, 1-100 characters (after trim)
- `description` (Optional[str]): Optional, max 500 characters
- `completed` (bool): Completion status (default: False)
- `created_at` (datetime): Creation timestamp
- `updated_at` (datetime): Last modification timestamp

### Validation Rules

- **Title**: Non-empty, 1-100 characters (whitespace trimmed)
- **Description**: Optional, max 500 characters
- **ID**: Positive integers, sequential generation, never reused
- **Timestamps**: Auto-managed (created_at immutable, updated_at refreshed on changes)

### Storage

- **In-Memory Only**: All data stored in Python lists/dictionaries
- **No Persistence**: Data is lost when the application exits (by design for Phase I)
- **Capacity**: Tested up to 10,000 tasks

### Error Handling

- **Graceful**: All errors handled with user-friendly messages
- **Validation**: Input validated before processing
- **Recovery**: Users can retry after errors
- **Ctrl+C**: Graceful exit with "Goodbye!" message

## Code Quality

- ✅ **PEP 8 Compliant**: Follows Python style guide
- ✅ **Type Hints**: All functions have complete type annotations
- ✅ **Docstrings**: All public functions documented (Google style)
- ✅ **Testing**: Comprehensive unit test coverage
- ✅ **No External Dependencies**: Python stdlib only

## Performance

- **Startup**: <2 seconds
- **Operations**: <1 second response time
- **Scale**: Supports up to 10,000 tasks efficiently

## Limitations (Phase I Scope)

❌ **Not Included in Phase I:**
- File persistence or database storage
- Multi-user support or authentication
- Web interface or GUI
- Advanced features (priorities, tags, due dates, search)
- Bulk operations
- Undo/redo functionality
- Data export/import

These features are planned for future phases.

## Development Methodology

This project follows **Spec-Driven Development (SDD)**:
1. Specifications written first (before any code)
2. Code generated following detailed design documents
3. Test-Driven Development (TDD) approach
4. 100% alignment with acceptance criteria

## Documentation

Comprehensive design documents available in `specs/001-todo-console-app/`:
- `spec.md` - Feature specification with user stories and requirements
- `plan.md` - Technical implementation plan
- `data-model.md` - Data entity specifications
- `contracts/` - API specifications for each module
- `research.md` - Technical decisions and rationale
- `tasks.md` - Detailed task breakdown (134 tasks)
- `quickstart.md` - Implementation guide

## License

This project is for educational/demonstration purposes.

## Version

**Phase I - Version 1.0.0**
Date: 2025-12-30

---

**Note**: This is an in-memory application. All data is lost when you exit. Future phases will add persistence and additional features.
