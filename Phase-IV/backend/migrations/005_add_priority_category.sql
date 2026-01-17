-- Migration: Add priority and category columns to tasks table
-- Created: 2026-01-08
-- Description: Adds priority and category fields for better task organization

-- ============================================================================
-- ADD PRIORITY AND CATEGORY COLUMNS
-- ============================================================================

-- Add priority column (default: medium)
ALTER TABLE tasks
ADD COLUMN IF NOT EXISTS priority VARCHAR(20) DEFAULT 'medium';

-- Add category column (default: other)
ALTER TABLE tasks
ADD COLUMN IF NOT EXISTS category VARCHAR(50) DEFAULT 'other';

-- Add indexes for filtering and sorting
CREATE INDEX IF NOT EXISTS idx_tasks_priority
    ON tasks(user_id, priority);

CREATE INDEX IF NOT EXISTS idx_tasks_category
    ON tasks(user_id, category);

-- Add check constraints for valid values
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'check_priority_values') THEN
        ALTER TABLE tasks
        ADD CONSTRAINT check_priority_values
            CHECK (priority IN ('low', 'medium', 'high'));
    END IF;

    IF NOT EXISTS (SELECT 1 FROM pg_constraint WHERE conname = 'check_category_values') THEN
        ALTER TABLE tasks
        ADD CONSTRAINT check_category_values
            CHECK (category IN ('personal', 'work', 'study', 'health', 'shopping', 'other'));
    END IF;
END $$;

-- Add comments to columns
COMMENT ON COLUMN tasks.priority IS 'Task priority level: low, medium, or high';
COMMENT ON COLUMN tasks.category IS 'Task category: personal, work, study, health, shopping, or other';

-- ============================================================================
-- VERIFICATION
-- ============================================================================

-- Verify columns were added
DO $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'tasks'
        AND column_name IN ('priority', 'category')
    ) THEN
        RAISE NOTICE 'Columns "priority" and "category" added successfully to tasks table';
    END IF;
END $$;
