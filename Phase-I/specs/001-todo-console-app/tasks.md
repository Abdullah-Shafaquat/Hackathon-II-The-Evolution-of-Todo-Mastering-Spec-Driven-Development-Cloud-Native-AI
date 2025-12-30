# Tasks: Todo Console App - Phase I

**Input**: Design documents from `/specs/001-todo-console-app/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Constitution mandates comprehensive unit tests (100% coverage of basic functionality). Test tasks included as part of TDD workflow.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (US1, US2, US3, US4, US5)
- Include exact file paths in descriptions

## Path Conventions

Single project structure (from plan.md):
- Source: `src/` at repository root
- Tests: `tests/` at repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create src/ directory with __init__.py for package initialization
- [ ] T002 Create tests/ directory with __init__.py for test discovery
- [ ] T003 [P] Create empty placeholder files: src/main.py, src/models.py, src/todo_manager.py, src/console_ui.py
- [ ] T004 [P] Create empty test files: tests/test_models.py, tests/test_todo_manager.py, tests/test_console_ui.py

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core data model and exceptions that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T005 [US-Foundation] Define custom exceptions (ValidationError, TaskNotFoundError) in src/models.py
- [ ] T006 [US-Foundation] Create Task dataclass with 6 fields (id, title, description, completed, created_at, updated_at) in src/models.py
- [ ] T007 [US-Foundation] Implement Task.__post_init__() validation method in src/models.py
- [ ] T008 [US-Foundation] Add Task validation helpers (_validate_id, _validate_title, _validate_description, _validate_timestamps) in src/models.py
- [ ] T009 [US-Foundation] Initialize global state (tasks list, next_id counter) in src/todo_manager.py

**Checkpoint**: Foundation ready - Task model complete with validation, global storage initialized

---

## Phase 3: User Story 1 - Task Creation (Priority: P1) 🎯 MVP

**Goal**: Enable users to add new tasks with title and optional description

**Independent Test**: Launch app, select "Add Task", enter title and description, verify task created with ID 1 and success message

### Tests for User Story 1

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T010 [P] [US1] Test Task creation with all fields in tests/test_models.py
- [ ] T011 [P] [US1] Test Task creation with minimal fields (no description) in tests/test_models.py
- [ ] T012 [P] [US1] Test empty title rejection in tests/test_models.py
- [ ] T013 [P] [US1] Test 101-character title rejection in tests/test_models.py
- [ ] T014 [P] [US1] Test 100-character title acceptance (boundary) in tests/test_models.py
- [ ] T015 [P] [US1] Test 501-character description rejection in tests/test_models.py
- [ ] T016 [P] [US1] Test 500-character description acceptance (boundary) in tests/test_models.py
- [ ] T017 [P] [US1] Test whitespace trimming for title in tests/test_models.py
- [ ] T018 [P] [US1] Test add_task() with title only in tests/test_todo_manager.py
- [ ] T019 [P] [US1] Test add_task() with title and description in tests/test_todo_manager.py
- [ ] T020 [P] [US1] Test sequential ID generation (1, 2, 3) in tests/test_todo_manager.py
- [ ] T021 [P] [US1] Test ValidationError on empty title in tests/test_todo_manager.py

### Implementation for User Story 1

- [ ] T022 [US1] Implement add_task(title, description) function in src/todo_manager.py
- [ ] T023 [US1] Add title trimming and validation in add_task() in src/todo_manager.py
- [ ] T024 [US1] Add description validation in add_task() in src/todo_manager.py
- [ ] T025 [US1] Implement Task instantiation with auto-generated ID and timestamps in src/todo_manager.py
- [ ] T026 [US1] Append new task to global tasks list in src/todo_manager.py
- [ ] T027 [US1] Increment next_id counter in src/todo_manager.py
- [ ] T028 [US1] Implement prompt_add_task() UI function in src/console_ui.py
- [ ] T029 [US1] Add user prompts for title and description in src/console_ui.py
- [ ] T030 [US1] Add ValidationError handling with user-friendly messages in src/console_ui.py
- [ ] T031 [US1] Display success message "Task added successfully! ID: {id}" in src/console_ui.py
- [ ] T032 [US1] Run User Story 1 tests and verify all pass

**Checkpoint**: Users can add tasks with validation. Test independently by running add_task tests.

---

## Phase 4: User Story 2 - Task Viewing (Priority: P1)

**Goal**: Enable users to view all tasks sorted newest-first with status symbols and statistics

**Independent Test**: Add 3 tasks (1 complete, 2 incomplete), select "View All Tasks", verify correct display with ✓/✗ symbols and summary

### Tests for User Story 2

- [ ] T033 [P] [US2] Test get_all_tasks() with empty list in tests/test_todo_manager.py
- [ ] T034 [P] [US2] Test get_all_tasks() returns tasks sorted newest-first in tests/test_todo_manager.py
- [ ] T035 [P] [US2] Test get_task_statistics() with no tasks in tests/test_todo_manager.py
- [ ] T036 [P] [US2] Test get_task_statistics() with mixed complete/incomplete in tests/test_todo_manager.py
- [ ] T037 [P] [US2] Test format_task_display() with complete task (✓) in tests/test_console_ui.py
- [ ] T038 [P] [US2] Test format_task_display() with incomplete task (✗) in tests/test_console_ui.py
- [ ] T039 [P] [US2] Test format_task_display() with description separator in tests/test_console_ui.py
- [ ] T040 [P] [US2] Test format_task_display() without description in tests/test_console_ui.py

### Implementation for User Story 2

- [ ] T041 [US2] Implement get_all_tasks() with sorting by created_at descending in src/todo_manager.py
- [ ] T042 [US2] Implement get_task_statistics() returning dict with total/completed/pending in src/todo_manager.py
- [ ] T043 [US2] Implement format_task_display(task) with ✓/✗ symbols in src/console_ui.py
- [ ] T044 [US2] Add title-description separator formatting in src/console_ui.py
- [ ] T045 [US2] Implement prompt_view_tasks() UI function in src/console_ui.py
- [ ] T046 [US2] Add empty list message "No tasks found. Add some tasks!" in src/console_ui.py
- [ ] T047 [US2] Display task list with formatting in src/console_ui.py
- [ ] T048 [US2] Display summary "X completed, Y pending, Z total" in src/console_ui.py
- [ ] T049 [US2] Add "Press Enter to continue..." prompt in src/console_ui.py
- [ ] T050 [US2] Run User Story 2 tests and verify all pass

**Checkpoint**: Users can view tasks with correct symbols and statistics. Test independently.

---

## Phase 5: User Story 3 - Task Modification (Priority: P2)

**Goal**: Enable users to update task title and/or description with special "." to clear description

**Independent Test**: Create task, select "Update Task", modify title or description, verify changes saved with updated timestamp

### Tests for User Story 3

- [ ] T051 [P] [US3] Test get_task_by_id() returns correct task in tests/test_todo_manager.py
- [ ] T052 [P] [US3] Test get_task_by_id() raises TaskNotFoundError in tests/test_todo_manager.py
- [ ] T053 [P] [US3] Test update_task() title only (keep description) in tests/test_todo_manager.py
- [ ] T054 [P] [US3] Test update_task() description only (keep title) in tests/test_todo_manager.py
- [ ] T055 [P] [US3] Test update_task() clear description with "." in tests/test_todo_manager.py
- [ ] T056 [P] [US3] Test update_task() updates updated_at timestamp in tests/test_todo_manager.py
- [ ] T057 [P] [US3] Test update_task() preserves created_at timestamp in tests/test_todo_manager.py
- [ ] T058 [P] [US3] Test update_task() raises TaskNotFoundError for invalid ID in tests/test_todo_manager.py

### Implementation for User Story 3

- [ ] T059 [US3] Implement get_task_by_id(task_id) with linear search in src/todo_manager.py
- [ ] T060 [US3] Add TaskNotFoundError raise in get_task_by_id() in src/todo_manager.py
- [ ] T061 [US3] Implement update_task(task_id, title, description) in src/todo_manager.py
- [ ] T062 [US3] Add logic to keep current title if None passed in src/todo_manager.py
- [ ] T063 [US3] Add logic to keep current description if None passed in src/todo_manager.py
- [ ] T064 [US3] Add special "." handling to clear description in src/todo_manager.py
- [ ] T065 [US3] Update task.updated_at to datetime.now() in src/todo_manager.py
- [ ] T066 [US3] Recreate Task instance with updated values in src/todo_manager.py
- [ ] T067 [US3] Implement get_valid_integer(prompt) helper in src/console_ui.py
- [ ] T068 [US3] Implement prompt_update_task() UI function in src/console_ui.py
- [ ] T069 [US3] Display current task values before prompting for new ones in src/console_ui.py
- [ ] T070 [US3] Add prompts with "(press Enter to keep...)" hints in src/console_ui.py
- [ ] T071 [US3] Add TaskNotFoundError handling with "Task with ID X not found" in src/console_ui.py
- [ ] T072 [US3] Display "Task updated successfully!" message in src/console_ui.py
- [ ] T073 [US3] Run User Story 3 tests and verify all pass

**Checkpoint**: Users can update tasks with validation. Test independently.

---

## Phase 6: User Story 4 - Task Removal (Priority: P2)

**Goal**: Enable users to delete tasks by ID with y/n confirmation, preserving other task IDs

**Independent Test**: Create task, select "Delete Task", confirm with 'y', verify task removed and IDs not reused

### Tests for User Story 4

- [ ] T074 [P] [US4] Test delete_task() removes task from list in tests/test_todo_manager.py
- [ ] T075 [P] [US4] Test delete_task() raises TaskNotFoundError for invalid ID in tests/test_todo_manager.py
- [ ] T076 [P] [US4] Test delete_task() preserves other task IDs in tests/test_todo_manager.py
- [ ] T077 [P] [US4] Test delete_task() creates gap in ID sequence in tests/test_todo_manager.py
- [ ] T078 [P] [US4] Test next task after deletion gets higher ID (gap not reused) in tests/test_todo_manager.py

### Implementation for User Story 4

- [ ] T079 [US4] Implement delete_task(task_id) in src/todo_manager.py
- [ ] T080 [US4] Find task by ID and remove from list in src/todo_manager.py
- [ ] T081 [US4] Add TaskNotFoundError raise for invalid ID in src/todo_manager.py
- [ ] T082 [US4] Implement prompt_delete_task() UI function in src/console_ui.py
- [ ] T083 [US4] Add confirmation prompt "Are you sure? (y/n): " in src/console_ui.py
- [ ] T084 [US4] Validate confirmation input (y/Y/n/N only) with re-prompting in src/console_ui.py
- [ ] T085 [US4] Display "Task deleted successfully!" on 'y' in src/console_ui.py
- [ ] T086 [US4] Display "Deletion cancelled" on 'n' in src/console_ui.py
- [ ] T087 [US4] Add TaskNotFoundError handling in src/console_ui.py
- [ ] T088 [US4] Run User Story 4 tests and verify all pass

**Checkpoint**: Users can delete tasks with confirmation. Test independently.

---

## Phase 7: User Story 5 - Progress Tracking (Priority: P2)

**Goal**: Enable users to toggle task completion status and see ✓/✗ symbol change

**Independent Test**: Create task, toggle to complete (✓), toggle to incomplete (✗), verify status changes

### Tests for User Story 5

- [ ] T089 [P] [US5] Test toggle_task_completion() incomplete → complete in tests/test_todo_manager.py
- [ ] T090 [P] [US5] Test toggle_task_completion() complete → incomplete in tests/test_todo_manager.py
- [ ] T091 [P] [US5] Test toggle_task_completion() updates updated_at in tests/test_todo_manager.py
- [ ] T092 [P] [US5] Test toggle_task_completion() preserves created_at in tests/test_todo_manager.py
- [ ] T093 [P] [US5] Test toggle_task_completion() raises TaskNotFoundError in tests/test_todo_manager.py
- [ ] T094 [P] [US5] Test multiple toggles alternate correctly in tests/test_todo_manager.py

### Implementation for User Story 5

- [ ] T095 [US5] Implement toggle_task_completion(task_id) in src/todo_manager.py
- [ ] T096 [US5] Find task by ID and flip completed boolean in src/todo_manager.py
- [ ] T097 [US5] Update task.updated_at to datetime.now() in src/todo_manager.py
- [ ] T098 [US5] Recreate Task instance with toggled completed field in src/todo_manager.py
- [ ] T099 [US5] Add TaskNotFoundError raise for invalid ID in src/todo_manager.py
- [ ] T100 [US5] Implement prompt_toggle_completion() UI function in src/console_ui.py
- [ ] T101 [US5] Add prompt "Enter task ID to mark complete/incomplete: " in src/console_ui.py
- [ ] T102 [US5] Display "Task marked as complete!" when toggled to True in src/console_ui.py
- [ ] T103 [US5] Display "Task marked as incomplete!" when toggled to False in src/console_ui.py
- [ ] T104 [US5] Add TaskNotFoundError handling in src/console_ui.py
- [ ] T105 [US5] Run User Story 5 tests and verify all pass

**Checkpoint**: Users can toggle task completion. All 5 user stories now functional independently.

---

## Phase 8: Application Integration & Main Loop

**Purpose**: Wire all user stories together with menu system and application entry point

- [ ] T106 Implement display_menu() showing 6 options in src/console_ui.py
- [ ] T107 Implement get_menu_choice() with validation (1-6) in src/console_ui.py
- [ ] T108 [P] Implement display_welcome() with welcome banner in src/console_ui.py
- [ ] T109 [P] Implement display_goodbye() with "Goodbye!" message in src/console_ui.py
- [ ] T110 Implement setup_signal_handlers() for Ctrl+C (SIGINT) in src/main.py
- [ ] T111 Add signal handler that prints "\nGoodbye!" and exits in src/main.py
- [ ] T112 Implement run_main_loop() with menu dispatch in src/main.py
- [ ] T113 Add action dispatch for all 6 menu options in src/main.py
- [ ] T114 Implement main() orchestrating welcome, loop, goodbye in src/main.py
- [ ] T115 Add if __name__ == "__main__": main() entry point in src/main.py

**Checkpoint**: Complete application ready for end-to-end testing

---

## Phase 9: Edge Cases & Error Handling

**Purpose**: Handle all 8 edge cases from spec.md

- [ ] T116 Test maximum title length (100 chars) handling in tests/test_models.py
- [ ] T117 Test maximum description length (500 chars) handling in tests/test_models.py
- [ ] T118 Test rapid toggling of completion status in tests/test_todo_manager.py
- [ ] T119 Test multiple deletions creating ID gaps in tests/test_todo_manager.py
- [ ] T120 Test non-numeric input for task ID in tests/test_console_ui.py
- [ ] T121 Test Ctrl+C graceful exit with "Goodbye!" message (manual test)
- [ ] T122 Test empty task list across all operations in tests/test_todo_manager.py
- [ ] T123 Test whitespace-only title rejection in tests/test_models.py

**Checkpoint**: All edge cases covered with tests

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Final quality checks and documentation

- [ ] T124 [P] Verify PEP 8 compliance across all modules
- [ ] T125 [P] Add type hints to all functions in all modules
- [ ] T126 [P] Add docstrings to all public functions (Google style)
- [ ] T127 [P] Verify error messages match spec exactly
- [ ] T128 Run all tests with unittest discover and verify 100% pass rate
- [ ] T129 Manual testing checklist from quickstart.md (26 test scenarios)
- [ ] T130 Verify all 25 acceptance scenarios from spec.md work correctly
- [ ] T131 [P] Performance test with 10,000 tasks (<1 second operations)
- [ ] T132 [P] Startup time test (<2 seconds as per spec SC-005)
- [ ] T133 Test Unicode symbols (✓/✗) on Windows/macOS/Linux
- [ ] T134 Code review for separation of concerns (Models/Logic/UI/App)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - US1 (P1) - Task Creation: Can start after Foundational ✅ MVP
  - US2 (P1) - Task Viewing: Can start after Foundational ✅ MVP
  - US3 (P2) - Task Modification: Can start after Foundational (integrates with US1/US2 for display)
  - US4 (P2) - Task Removal: Can start after Foundational (integrates with US2 for verification)
  - US5 (P2) - Progress Tracking: Can start after Foundational (integrates with US2 for display)
- **Application Integration (Phase 8)**: Depends on all 5 user stories being complete
- **Edge Cases (Phase 9)**: Depends on Application Integration
- **Polish (Phase 10)**: Depends on all previous phases

### User Story Dependencies

- **User Story 1 (P1)**: FOUNDATIONAL → Can implement independently ✅ MVP
- **User Story 2 (P1)**: FOUNDATIONAL → Can implement independently ✅ MVP
- **User Story 3 (P2)**: FOUNDATIONAL + (integrates with US1/US2 but testable alone)
- **User Story 4 (P2)**: FOUNDATIONAL + (integrates with US2 for verification but testable alone)
- **User Story 5 (P2)**: FOUNDATIONAL + (integrates with US2 for display but testable alone)

### Within Each User Story

1. Tests FIRST (write, ensure they FAIL)
2. Models (T005-T009 foundational Task model)
3. Business logic (todo_manager.py functions)
4. UI layer (console_ui.py functions)
5. Run tests, verify all PASS
6. Independent story validation

### Parallel Opportunities

**Setup Phase (Phase 1)**:
- T003 and T004 can run in parallel (different directories)

**Foundational Phase (Phase 2)**:
- All tasks sequential (building shared Task model)

**User Story 1 Tests**:
- T010-T021 can all run in parallel (independent test files/functions)

**User Story 1 Implementation**:
- T022-T027 sequential (building add_task function)
- T028-T031 sequential (building UI function)

**User Story 2 Tests**:
- T033-T040 can all run in parallel

**User Story 2 Implementation**:
- T041-T042 can run in parallel (different functions)
- T043-T044 sequential
- T045-T049 sequential

**User Story 3-5**: Similar parallel test opportunities, sequential implementation

**Application Integration (Phase 8)**:
- T108-T109 can run in parallel (independent display functions)
- T106-T107, T110-T115 sequential

**Edge Cases (Phase 9)**:
- All tests can run in parallel

**Polish (Phase 10)**:
- T124-T127 can run in parallel (different concerns)
- T131-T133 can run in parallel (independent tests)

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task T010: "Test Task creation with all fields in tests/test_models.py"
Task T011: "Test Task creation with minimal fields in tests/test_models.py"
Task T012: "Test empty title rejection in tests/test_models.py"
Task T013: "Test 101-character title rejection in tests/test_models.py"
Task T014: "Test 100-character title acceptance in tests/test_models.py"
Task T015: "Test 501-character description rejection in tests/test_models.py"
Task T016: "Test 500-character description acceptance in tests/test_models.py"
Task T017: "Test whitespace trimming for title in tests/test_models.py"
Task T018: "Test add_task() with title only in tests/test_todo_manager.py"
Task T019: "Test add_task() with title and description in tests/test_todo_manager.py"
Task T020: "Test sequential ID generation in tests/test_todo_manager.py"
Task T021: "Test ValidationError on empty title in tests/test_todo_manager.py"

# After tests written and failing, implement in sequence:
Task T022: "Implement add_task(title, description) in src/todo_manager.py"
Task T023-T027: Build add_task function sequentially
Task T028-T031: Build prompt_add_task UI sequentially
Task T032: "Run User Story 1 tests and verify all pass"
```

---

## Implementation Strategy

### MVP First (User Story 1 + User Story 2 Only)

1. Complete Phase 1: Setup (T001-T004)
2. Complete Phase 2: Foundational (T005-T009) - CRITICAL
3. Complete Phase 3: User Story 1 - Task Creation (T010-T032)
4. Complete Phase 4: User Story 2 - Task Viewing (T033-T050)
5. **STOP and VALIDATE**: Test US1 and US2 independently
6. Add basic menu integration to demo MVP

**MVP Deliverable**: Users can add tasks and view them - core value demonstrated

### Incremental Delivery

1. Setup + Foundational (T001-T009) → Foundation ready
2. Add US1 (T010-T032) → Can create tasks → Test independently
3. Add US2 (T033-T050) → Can view tasks → Test independently → **MVP DEMO**
4. Add US3 (T051-T073) → Can update tasks → Test independently → Deploy/Demo
5. Add US4 (T074-T088) → Can delete tasks → Test independently → Deploy/Demo
6. Add US5 (T089-T105) → Can track completion → Test independently → Deploy/Demo
7. Add Integration (T106-T115) → Complete app → End-to-end test
8. Add Polish (T116-T134) → Production ready

### Parallel Team Strategy

With 3 developers:

1. **Together**: Complete Setup (Phase 1) + Foundational (Phase 2)
2. **After Foundational completes**:
   - Developer A: User Story 1 + User Story 2 (P1 stories for MVP)
   - Developer B: User Story 3 + User Story 4 (P2 stories)
   - Developer C: User Story 5 + Main Loop (P2 + integration)
3. **Merge and integrate**: Each story tested independently before integration

---

## Notes

- [P] tasks = different files/functions, can run in parallel
- [Story] label (US1-US5) maps task to specific user story for traceability
- [US-Foundation] = blocking prerequisite for all stories
- Each user story independently completable and testable
- TDD workflow: Write tests FIRST, ensure they FAIL, then implement
- Constitution mandates: PEP 8, type hints, docstrings, 100% test coverage
- Commit after each logical group of tasks (e.g., after each user story)
- Stop at checkpoints to validate story independently
- Performance target: <1 second all operations, <2 seconds startup
- Unicode symbols ✓/✗ required - test on all platforms

---

## Task Count Summary

- **Total Tasks**: 134
- **Setup (Phase 1)**: 4 tasks
- **Foundational (Phase 2)**: 5 tasks
- **User Story 1 (Phase 3)**: 23 tasks (12 tests + 11 implementation)
- **User Story 2 (Phase 4)**: 18 tasks (8 tests + 10 implementation)
- **User Story 3 (Phase 5)**: 23 tasks (8 tests + 15 implementation)
- **User Story 4 (Phase 6)**: 15 tasks (5 tests + 10 implementation)
- **User Story 5 (Phase 7)**: 17 tasks (6 tests + 11 implementation)
- **Application Integration (Phase 8)**: 10 tasks
- **Edge Cases (Phase 9)**: 8 tasks
- **Polish (Phase 10)**: 11 tasks

**Test Tasks**: 39 (29% test coverage planning)
**Implementation Tasks**: 95 (71% implementation)

**MVP Scope** (recommended): Phases 1-4 (T001-T050) = User Story 1 + User Story 2 (55 tasks)

**Parallel Opportunities**: 50+ tasks marked [P] can run concurrently
