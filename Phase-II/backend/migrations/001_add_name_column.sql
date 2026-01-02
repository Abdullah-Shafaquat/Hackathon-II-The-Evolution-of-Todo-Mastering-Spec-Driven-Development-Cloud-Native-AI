-- Migration: Add name column to users table
-- This adds the missing 'name' column to the users table

-- Add name column (if it doesn't exist)
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT column_name
        FROM information_schema.columns
        WHERE table_name='users' AND column_name='name'
    ) THEN
        ALTER TABLE users ADD COLUMN name VARCHAR(100);
        RAISE NOTICE 'Added name column to users table';
    ELSE
        RAISE NOTICE 'Column name already exists';
    END IF;
END $$;
