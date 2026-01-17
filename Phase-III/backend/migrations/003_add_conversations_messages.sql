-- Phase III Migration: Add Conversations and Messages Tables
-- Created: 2026-01-04
-- Description: Creates conversations and messages tables for AI chatbot functionality

-- ============================================================================
-- CONVERSATIONS TABLE
-- ============================================================================

-- Create conversations table for chat sessions
CREATE TABLE IF NOT EXISTS conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_conversations_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

-- Create indexes for conversations table
CREATE INDEX IF NOT EXISTS idx_conversations_user_id
    ON conversations(user_id);

CREATE INDEX IF NOT EXISTS idx_conversations_user_updated
    ON conversations(user_id, updated_at DESC);

-- Add comment to conversations table
COMMENT ON TABLE conversations IS 'Chat sessions between users and AI assistant';
COMMENT ON COLUMN conversations.id IS 'Unique conversation identifier (UUID)';
COMMENT ON COLUMN conversations.user_id IS 'Owner of the conversation (FK to users.id)';
COMMENT ON COLUMN conversations.created_at IS 'When the conversation was started';
COMMENT ON COLUMN conversations.updated_at IS 'Last message timestamp';

-- ============================================================================
-- MESSAGES TABLE
-- ============================================================================

-- Create messages table for chat history
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    conversation_id UUID NOT NULL,
    role VARCHAR(50) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_messages_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE,
    CONSTRAINT fk_messages_conversation
        FOREIGN KEY (conversation_id)
        REFERENCES conversations(id)
        ON DELETE CASCADE
);

-- Create indexes for messages table
CREATE INDEX IF NOT EXISTS idx_messages_conversation_id
    ON messages(conversation_id);

CREATE INDEX IF NOT EXISTS idx_messages_conversation_created
    ON messages(conversation_id, created_at ASC);

CREATE INDEX IF NOT EXISTS idx_messages_user_id
    ON messages(user_id);

-- Add comments to messages table
COMMENT ON TABLE messages IS 'Individual chat messages within conversations';
COMMENT ON COLUMN messages.id IS 'Unique message identifier (auto-increment)';
COMMENT ON COLUMN messages.user_id IS 'Owner of the conversation (denormalized for filtering)';
COMMENT ON COLUMN messages.conversation_id IS 'Parent conversation (FK to conversations.id)';
COMMENT ON COLUMN messages.role IS 'Message sender: "user" or "assistant"';
COMMENT ON COLUMN messages.content IS 'Message text content (max 50K chars)';
COMMENT ON COLUMN messages.created_at IS 'Message timestamp';

-- ============================================================================
-- VERIFICATION
-- ============================================================================

-- Verify tables were created
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'conversations') THEN
        RAISE NOTICE 'Table "conversations" created successfully';
    END IF;

    IF EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'messages') THEN
        RAISE NOTICE 'Table "messages" created successfully';
    END IF;
END $$;

-- Display table information
SELECT
    'conversations' as table_name,
    COUNT(*) as row_count
FROM conversations
UNION ALL
SELECT
    'messages' as table_name,
    COUNT(*) as row_count
FROM messages;
