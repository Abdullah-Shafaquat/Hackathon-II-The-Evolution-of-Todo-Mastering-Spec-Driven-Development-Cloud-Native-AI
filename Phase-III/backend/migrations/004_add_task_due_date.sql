-- Migration: Add due_date column to tasks table
-- Created: 2026-01-08
-- Description: Adds optional due_date field to support task scheduling

-- ============================================================================
-- ADD DUE_DATE COLUMN
-- ============================================================================

-- Add due_date column to tasks table
ALTER TABLE tasks
ADD COLUMN IF NOT EXISTS due_date DATE;

-- Add index for due_date queries
CREATE INDEX IF NOT EXISTS idx_tasks_due_date
    ON tasks(user_id, due_date);

-- Add comment to due_date column
COMMENT ON COLUMN tasks.due_date IS 'Optional due date for task completion';

-- ============================================================================
-- VERIFICATION
-- ============================================================================

-- Verify column was added
DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'tasks'
        AND column_name = 'due_date'
    ) THEN
        RAISE NOTICE 'Column "due_date" added successfully to tasks table';
    END IF;
END $$;
