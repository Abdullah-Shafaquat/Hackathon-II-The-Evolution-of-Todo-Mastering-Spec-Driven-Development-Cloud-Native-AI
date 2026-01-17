-- Phase III Rollback: Remove Conversations and Messages Tables
-- Created: 2026-01-04
-- Description: Rollback script to remove Phase III tables

-- WARNING: This will delete all conversation and message data!

-- ============================================================================
-- DROP TABLES (in reverse order due to foreign key dependencies)
-- ============================================================================

-- Drop messages table first (has FK to conversations)
DROP TABLE IF EXISTS messages CASCADE;

-- Drop conversations table
DROP TABLE IF EXISTS conversations CASCADE;

-- ============================================================================
-- VERIFICATION
-- ============================================================================

-- Verify tables were dropped
DO $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'conversations') THEN
        RAISE NOTICE 'Table "conversations" dropped successfully';
    END IF;

    IF NOT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'messages') THEN
        RAISE NOTICE 'Table "messages" dropped successfully';
    END IF;
END $$;

-- Display remaining tables
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
  AND table_type = 'BASE TABLE'
ORDER BY table_name;
