# Chat Endpoint Tests

Comprehensive test suite for Phase III AI Chatbot endpoints.

## Test Coverage

### Test Files

- **`test_chat_endpoints.py`** - Chat API endpoint tests (Task 5.5)

### Test Classes

1. **TestSendChatMessage** - Tests for `POST /api/{user_id}/chat`
   - ✅ Send message (new conversation)
   - ✅ Send message (existing conversation)
   - ✅ Conversation history loading
   - ✅ Authentication required
   - ✅ User isolation (403 errors)
   - ✅ Conversation not found (404 errors)
   - ✅ Access denied for other user's conversation
   - ✅ Empty message validation
   - ✅ Message length validation (max 5000 chars)

2. **TestListConversations** - Tests for `GET /api/{user_id}/conversations`
   - ✅ List conversations successfully
   - ✅ Pagination (limit, offset)
   - ✅ User isolation
   - ✅ Authentication required

3. **TestGetConversationHistory** - Tests for `GET /api/{user_id}/conversations/{id}`
   - ✅ Get conversation history successfully
   - ✅ Conversation not found (404)
   - ✅ Access denied (wrong user)

4. **TestDeleteConversation** - Tests for `DELETE /api/{user_id}/conversations/{id}`
   - ✅ Delete conversation successfully
   - ✅ Verify CASCADE deletion of messages
   - ✅ Conversation not found (404)
   - ✅ Access denied (wrong user)

5. **TestErrorHandling** - Error handling scenarios
   - ✅ OpenAI rate limit errors (503)
   - ✅ OpenAI API errors (500)
   - ✅ Database errors (500)
   - ✅ Generic error messages (no sensitive data)

6. **TestRateLimiting** - Rate limiting functionality
   - ✅ Rate limit enforcement (30 req/min)
   - ✅ Per-user rate limiting
   - ✅ 429 response with Retry-After header

## Running Tests

### Prerequisites

```bash
# Install test dependencies
pip install -r requirements.txt
```

### Quick Start

**Linux/Mac:**
```bash
chmod +x run_tests.sh
./run_tests.sh
```

**Windows:**
```cmd
run_tests.bat
```

### Manual Commands

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run specific test file
pytest tests/test_chat_endpoints.py

# Run specific test class
pytest tests/test_chat_endpoints.py::TestSendChatMessage

# Run specific test
pytest tests/test_chat_endpoints.py::TestSendChatMessage::test_send_message_new_conversation

# Run with coverage
pytest --cov=app --cov-report=term-missing

# Generate HTML coverage report
pytest --cov=app --cov-report=html
# Then open: htmlcov/index.html
```

### Test Markers

```bash
# Run only unit tests (if marked)
pytest -m unit

# Skip slow tests
pytest -m "not slow"
```

## Test Fixtures

Located in `conftest.py`:

- **session** - In-memory SQLite database session
- **client** - FastAPI test client with database override
- **test_user** - Default test user
- **test_user_2** - Second test user (for authorization tests)
- **auth_headers** - JWT authentication headers for test_user
- **auth_headers_2** - JWT authentication headers for test_user_2
- **test_task** - Sample task for testing
- **test_conversation** - Sample conversation
- **test_messages** - Sample conversation messages
- **mock_openai_response** - Mock OpenAI API response

## Mocking Strategy

OpenAI API calls are mocked using `unittest.mock.patch`:

```python
@patch('app.routes.chat.process_message_with_agent')
def test_example(mock_process, client, auth_headers):
    mock_process.return_value = {
        "response": "Test response",
        "tool_calls": []
    }
    # Test code...
```

This prevents actual OpenAI API calls during testing.

## Coverage Goals

- **Target**: 80%+ code coverage
- **Current**: Run `pytest --cov` to see current coverage

## Test Data Isolation

- Each test uses a fresh in-memory database
- Database is created before test and dropped after
- No persistent data between tests
- Tests are fully isolated and can run in any order

## Troubleshooting

### Import Errors

```bash
# Ensure PYTHONPATH includes app directory
export PYTHONPATH="${PYTHONPATH}:${PWD}"
```

### Database Errors

- Tests use SQLite in-memory database
- No need for PostgreSQL/Neon during testing
- All tables created automatically via SQLModel

### Authentication Errors

- JWT tokens are generated in fixtures
- No need for actual authentication server
- Tokens are valid for test duration

## Task 5.5 Acceptance Criteria

All acceptance criteria from `specs/002-phase3-ai-chatbot/tasks.md` Task 5.5:

- ✅ Test send message (new conversation)
- ✅ Test send message (existing conversation)
- ✅ Test conversation history loading
- ✅ Test user isolation (prevent cross-user access)
- ✅ Test authentication requirement (401 errors)
- ✅ Test conversation not found (404 error)
- ✅ Test list conversations
- ✅ Test delete conversation
- ✅ Mock OpenAI API calls
- ✅ All tests pass

## Next Steps

After tests pass:
1. Review coverage report
2. Add additional edge case tests if needed
3. Move to Phase 6 (Frontend ChatKit)
4. Run tests in CI/CD pipeline
