# Task Management Features - Testing Guide

This guide will help you test all the new features implemented in Waves 1-4.

## Prerequisites

1. **Start Backend Server:**
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```

2. **Start Frontend Server:**
   ```bash
   cd frontend
   npm run dev
   ```

3. **Navigate to:** http://localhost:3000

---

## Feature Testing Checklist

### ✅ Wave 1: Backend Foundation

#### Test 1.1: Create Task with All Fields
- [ ] Click on "Add Task" form
- [ ] Fill in:
  - Title: "Test Work Meeting"
  - Description: "Important meeting"
  - Due Date: Tomorrow's date
  - Priority: High
  - Category: Work
- [ ] Click "Add Task"
- [ ] **Expected:** Task appears with all fields displayed

#### Test 1.2: Verify Default Values
- [ ] Create a task with only title: "Minimal Task"
- [ ] **Expected:**
  - Priority: Medium (default)
  - Category: Other (default)
  - Status: Pending (default)
  - Due Date: None

---

### ✅ Wave 2: Frontend Core Features

#### Test 2.1: Date Picker
- [ ] Open "Add Task" form
- [ ] Click on Due Date field
- [ ] **Expected:** HTML5 date picker appears
- [ ] Select a date
- [ ] **Expected:** Date is selected and shows in field
- [ ] **Expected:** Cannot select past dates (disabled)

#### Test 2.2: Task Sorting
- [ ] Create 3+ tasks with different priorities (high, medium, low)
- [ ] Click on "Sort by" dropdown
- [ ] Select "Priority"
- [ ] **Expected:** Tasks reorder with high priority first
- [ ] Select "Due Date"
- [ ] **Expected:** Overdue tasks appear first, then by due date ascending
- [ ] Select "Recently Added"
- [ ] **Expected:** Most recent tasks appear first

#### Test 2.3: Category Filter
- [ ] Create tasks in different categories (Work, Personal, Shopping, etc.)
- [ ] Click category filter chips
- [ ] Select "Work" category
- [ ] **Expected:** Only work tasks are shown
- [ ] Select multiple categories
- [ ] **Expected:** Tasks from all selected categories shown
- [ ] Click "All"
- [ ] **Expected:** All tasks shown again

#### Test 2.4: Enhanced Search
- [ ] Create tasks with different titles, descriptions, categories
- [ ] Type "work" in search bar
- [ ] **Expected:** Tasks with "work" in title, description, category, or priority shown
- [ ] Type "high"
- [ ] **Expected:** All high priority tasks shown
- [ ] Clear search
- [ ] **Expected:** All tasks shown again

#### Test 2.5: Task Editing
- [ ] Click edit (pencil icon) on any task
- [ ] **Expected:** All fields become editable
- [ ] Change:
  - Title
  - Description
  - Due Date
  - Priority
  - Category
- [ ] Click Save
- [ ] **Expected:** Task updates with new values

---

### ✅ Wave 3: Task Status & Reminders

#### Test 3.1: Status Toggle Buttons
- [ ] Find a task
- [ ] Click "⏸️ Pending" button
- [ ] **Expected:** Task marked as pending
- [ ] Click "🔄 In Progress" button
- [ ] **Expected:** Task status changes to in progress, button highlighted
- [ ] Click "✅ Completed" button
- [ ] **Expected:** Task marked as completed, checkbox also checked

#### Test 3.2: Overdue Task Visual Indicators
- [ ] Create a task with due date = 2 days ago
- [ ] **Expected:** Task has red border and red background
- [ ] **Expected:** Task appears at the top of the list (auto-sorted)

#### Test 3.3: Reminder Banner
- [ ] Create tasks:
  - One with due date = today
  - One with due date = 2 days ago (overdue)
- [ ] **Expected:** Banner appears at top showing:
  - "⚠️ X Overdue" in red
  - "📅 X Due Today" in purple
- [ ] **Expected:** Banner shows up to 3 task previews
- [ ] Complete all overdue/due today tasks
- [ ] **Expected:** Banner disappears

#### Test 3.4: Browser Notifications
- [ ] Reload the page
- [ ] **Expected:** Browser asks for notification permission
- [ ] Click "Allow"
- [ ] If you have overdue tasks:
  - **Expected:** Desktop notification appears saying "X Tasks Overdue!"
- [ ] If you have tasks due today:
  - **Expected:** Desktop notification appears saying "X Tasks Due Today"
- [ ] **Expected:** Notifications only appear once per session

---

### ✅ Wave 4: Power User Features

#### Test 4.1: Bulk Complete
- [ ] Create 3+ pending tasks
- [ ] Click "Select Multiple Tasks" button
- [ ] **Expected:** Checkboxes appear on each task
- [ ] Select 2-3 tasks by clicking checkboxes
- [ ] **Expected:** Blue bulk action bar appears at top
- [ ] **Expected:** Shows "X tasks selected"
- [ ] Click "Select All"
- [ ] **Expected:** All visible tasks selected
- [ ] Click "Mark as Completed"
- [ ] **Expected:** All selected tasks marked as completed
- [ ] **Expected:** Bulk action bar disappears

#### Test 4.2: Daily Summary Component
- [ ] Scroll to Daily Summary section (below Task Statistics)
- [ ] **Expected:** Six metric cards showing:
  1. **Overdue** (red if > 0)
  2. **Due Today** (purple if > 0)
  3. **Completed Today** (green)
  4. **In Progress** (yellow)
  5. **Pending** (blue)
  6. **Total** (white)
- [ ] **Expected:** Metrics update when tasks change
- [ ] **Expected:** "Quick Insights" section shows actionable messages

#### Test 4.3: AI Chat - Category Filtering
- [ ] Navigate to Chat page (click "Chat" button in header)
- [ ] Type: "Show my work tasks"
- [ ] **Expected:** AI lists only tasks with category = "work"
- [ ] Type: "Show shopping tasks"
- [ ] **Expected:** AI lists only shopping tasks

#### Test 4.4: AI Chat - Status Filtering
- [ ] In chat, type: "What tasks are in progress?"
- [ ] **Expected:** AI lists only tasks with status = "in_progress"
- [ ] Type: "Show completed tasks"
- [ ] **Expected:** AI lists only completed tasks

#### Test 4.5: AI Chat - Sorting
- [ ] In chat, type: "Show tasks by priority"
- [ ] **Expected:** AI lists tasks sorted by priority (high → medium → low)
- [ ] Type: "Show tasks by due date"
- [ ] **Expected:** AI lists tasks sorted by due date

#### Test 4.6: AI Chat - Combined Filters
- [ ] In chat, type: "Show my work tasks sorted by priority"
- [ ] **Expected:** AI filters by category="work" AND sorts by priority
- [ ] Type: "What are my high priority tasks due today?"
- [ ] **Expected:** AI shows tasks with priority="high" and due_date=today

---

## Automated Test Script

Once your servers are running, you can run the automated test suite:

```bash
cd backend
python test_new_features.py
```

This will automatically test:
1. ✅ Create tasks with all fields (priority, category, due_date, status)
2. ✅ Filter tasks (all, pending, completed)
3. ✅ Update task status (pending → in_progress → completed)
4. ✅ Update priority, category, and due_date
5. ✅ Sorting and category filtering
6. ✅ Overdue task detection
7. ✅ Bulk complete operations
8. ✅ Daily summary calculations
9. ✅ Enhanced search (title, description, category, priority)
10. ✅ Backward compatibility (tasks without new fields)

---

## Expected Results Summary

### Database Schema
- ✅ `status` column exists with values: pending, in_progress, completed
- ✅ `due_date` column stores dates in YYYY-MM-DD format
- ✅ `priority` column with values: high, medium, low
- ✅ `category` column with values: personal, work, study, health, shopping, other
- ✅ Index on (user_id, status) for efficient queries
- ✅ Check constraint ensuring valid status values

### Backend API
- ✅ POST /api/tasks accepts: title, description, due_date, priority, category
- ✅ PATCH /api/tasks/:id accepts: status, due_date, priority, category
- ✅ GET /api/tasks returns all fields including status
- ✅ Status sync: when status="completed", completed=true (backward compat)

### Frontend Components
- ✅ TaskForm: Date picker, priority selector, category selector
- ✅ TaskItem: Status buttons, edit mode for all fields, overdue styling
- ✅ TaskSorter: 4 sort options (date, priority, status, recent)
- ✅ CategoryFilter: Multi-select category chips
- ✅ DailySummary: 6 metrics with quick insights
- ✅ Dashboard: Reminder banner, bulk select, enhanced search
- ✅ Notifications: Browser push notifications for overdue/due today

### AI Chat (Gemini)
- ✅ list_tasks tool supports: category, status, sort_by parameters
- ✅ Agent can filter by category: "show work tasks"
- ✅ Agent can filter by status: "what's in progress?"
- ✅ Agent can sort: "show by priority", "show by due date"
- ✅ Agent can combine filters: "work tasks by priority"

---

## Troubleshooting

### Issue: "Column 'status' does not exist"
**Solution:** Run the migration:
```bash
cd backend
python run_migration.py
```

### Issue: Frontend not showing new fields
**Solution:**
1. Clear browser cache (Ctrl+Shift+R)
2. Restart frontend server
3. Check browser console for errors

### Issue: Notifications not working
**Solution:**
1. Check browser notification permissions
2. Make sure you allowed notifications
3. Refresh the page to trigger permission request

### Issue: AI chat not filtering
**Solution:**
1. Check backend logs for MCP tool errors
2. Verify GEMINI_API_KEY is set in backend/.env
3. Restart backend server

---

## Success Criteria

✅ **All features implemented:**
- Task Priority (High, Medium, Low) with sorting
- Task Categories (Personal, Work, Study, Health, Shopping, Other) with filtering
- Task Status (Pending, In Progress, Completed) with toggle buttons
- Task Reminders (banner, visual indicators, browser notifications)
- Task Editing (all fields editable)
- Natural Language Commands (AI chat with advanced filtering)
- Smart Date Detection (date picker, overdue detection)
- Task Sorting Options (4 sort modes)
- Search Improvements (title, description, category, priority)
- Bulk Complete (select multiple, complete all at once)
- Daily Summary (6 key metrics)

✅ **Zero regression bugs** - Old features still work
✅ **Backward compatible** - Old tasks work with defaults
✅ **UI responsive** - Works on desktop and mobile
✅ **No console errors** - Clean browser console

---

## Test Results

Record your test results here:

| Feature | Status | Notes |
|---------|--------|-------|
| Create task with all fields | ⬜ | |
| Date picker | ⬜ | |
| Task sorting | ⬜ | |
| Category filter | ⬜ | |
| Enhanced search | ⬜ | |
| Task editing | ⬜ | |
| Status toggle | ⬜ | |
| Overdue indicators | ⬜ | |
| Reminder banner | ⬜ | |
| Browser notifications | ⬜ | |
| Bulk complete | ⬜ | |
| Daily summary | ⬜ | |
| AI chat - category filter | ⬜ | |
| AI chat - status filter | ⬜ | |
| AI chat - sorting | ⬜ | |
| Backward compatibility | ⬜ | |

**Legend:** ✅ Pass | ❌ Fail | ⬜ Not Tested

---

**Once you've completed all tests, all features should be working correctly!**
