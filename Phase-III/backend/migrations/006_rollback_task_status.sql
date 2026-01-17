-- Rollback Migration 006: Remove task status field
-- This removes the status column and its associated constraints

-- Drop the check constraint
ALTER TABLE tasks
DROP CONSTRAINT IF EXISTS check_status_values;

-- Drop the index
DROP INDEX IF EXISTS idx_tasks_status;

-- Drop the status column
ALTER TABLE tasks
DROP COLUMN IF EXISTS status;
