-- Migration 006: Add task status field
-- This adds support for task states: pending, in_progress, completed

-- Add status column with default value
ALTER TABLE tasks
ADD COLUMN IF NOT EXISTS status VARCHAR(20) DEFAULT 'pending';

-- Create index for efficient querying by status
CREATE INDEX IF NOT EXISTS idx_tasks_status
    ON tasks(user_id, status);

-- Add check constraint to ensure valid status values
ALTER TABLE tasks
ADD CONSTRAINT check_status_values
    CHECK (status IN ('pending', 'in_progress', 'completed'));

-- Migrate existing data: sync status with completed boolean
-- Tasks marked as completed should have status = 'completed'
-- Tasks marked as incomplete should have status = 'pending'
UPDATE tasks SET status = 'completed' WHERE completed = true;
UPDATE tasks SET status = 'pending' WHERE completed = false;

-- Note: We're keeping the 'completed' column for backward compatibility
-- In the future, we can deprecate it and use only 'status'
