"""
Chat Endpoints Tests
Tests for chat message and conversation management endpoints
"""

import pytest
import uuid
from unittest.mock import patch, Mock, MagicMock
from datetime import datetime
from fastapi.testclient import TestClient
from sqlmodel import Session, select

from app.models import Conversation, Message, Task, User
from app.middleware.rate_limit import chat_rate_limiter


class TestSendChatMessage:
    """Tests for POST /api/{user_id}/chat endpoint"""

    @patch('app.routes.chat.process_message_with_agent')
    def test_send_message_new_conversation(
        self,
        mock_process: Mock,
        client: TestClient,
        session: Session,
        test_user: User,
        auth_headers: dict,
        mock_openai_response: dict
    ):
        """Test sending a message creates a new conversation"""
        # Arrange
        mock_process.return_value = mock_openai_response
        chat_rate_limiter.requests.clear()  # Reset rate limiter

        # Act
        response = client.post(
            f"/api/{test_user.id}/chat",
            json={"message": "Add task to buy groceries"},
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 200
        data = response.json()

        # Verify response structure
        assert "conversation_id" in data
        assert "response" in data
        assert "tool_calls" in data
        assert "created_at" in data

        # Verify response content
        assert data["response"] == mock_openai_response["response"]
        assert data["tool_calls"] == mock_openai_response["tool_calls"]

        # Verify conversation created in database
        conversation_id = uuid.UUID(data["conversation_id"])
        conversation = session.get(Conversation, conversation_id)
        assert conversation is not None
        assert conversation.user_id == test_user.id

        # Verify messages saved
        messages = session.exec(
            select(Message).where(Message.conversation_id == conversation_id)
        ).all()
        assert len(messages) == 2
        assert messages[0].role == "user"
        assert messages[0].content == "Add task to buy groceries"
        assert messages[1].role == "assistant"

    @patch('app.routes.chat.process_message_with_agent')
    def test_send_message_existing_conversation(
        self,
        mock_process: Mock,
        client: TestClient,
        session: Session,
        test_user: User,
        test_conversation: Conversation,
        test_messages: list,
        auth_headers: dict,
        mock_openai_response: dict
    ):
        """Test sending a message to an existing conversation"""
        # Arrange
        mock_process.return_value = mock_openai_response
        chat_rate_limiter.requests.clear()

        # Act
        response = client.post(
            f"/api/{test_user.id}/chat",
            json={
                "conversation_id": str(test_conversation.id),
                "message": "What tasks do I have?"
            },
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 200
        data = response.json()

        # Verify same conversation ID
        assert data["conversation_id"] == str(test_conversation.id)

        # Verify messages count increased
        messages = session.exec(
            select(Message).where(Message.conversation_id == test_conversation.id)
        ).all()
        assert len(messages) == 4  # 2 existing + 2 new (user + assistant)

    @patch('app.routes.chat.process_message_with_agent')
    def test_conversation_history_loaded(
        self,
        mock_process: Mock,
        client: TestClient,
        test_user: User,
        test_conversation: Conversation,
        test_messages: list,
        auth_headers: dict,
        mock_openai_response: dict
    ):
        """Test that conversation history is passed to the agent"""
        # Arrange
        mock_process.return_value = mock_openai_response
        chat_rate_limiter.requests.clear()

        # Act
        response = client.post(
            f"/api/{test_user.id}/chat",
            json={
                "conversation_id": str(test_conversation.id),
                "message": "Continue our conversation"
            },
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 200

        # Verify agent was called with history
        mock_process.assert_called_once()
        call_args = mock_process.call_args
        history = call_args.kwargs["history"]

        # Should have the 2 test messages
        assert len(history) == 2
        assert history[0].content == "Hello, can you help me?"
        assert history[1].content == "Of course! I'm here to help."

    def test_send_message_requires_authentication(
        self,
        client: TestClient,
        test_user: User
    ):
        """Test that authentication is required"""
        # Act - No auth headers
        response = client.post(
            f"/api/{test_user.id}/chat",
            json={"message": "Test message"}
        )

        # Assert
        assert response.status_code == 401

    def test_send_message_wrong_user(
        self,
        client: TestClient,
        test_user: User,
        test_user_2: User,
        auth_headers: dict
    ):
        """Test that user cannot send message as another user"""
        # Arrange
        chat_rate_limiter.requests.clear()

        # Act - User 1 tries to send message as User 2
        response = client.post(
            f"/api/{test_user_2.id}/chat",
            json={"message": "Test message"},
            headers=auth_headers  # User 1's token
        )

        # Assert
        assert response.status_code == 403
        assert "Access denied" in response.json()["detail"]

    def test_send_message_conversation_not_found(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict
    ):
        """Test error when conversation ID doesn't exist"""
        # Arrange
        fake_conversation_id = str(uuid.uuid4())
        chat_rate_limiter.requests.clear()

        # Act
        response = client.post(
            f"/api/{test_user.id}/chat",
            json={
                "conversation_id": fake_conversation_id,
                "message": "Test message"
            },
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 404
        assert "not found" in response.json()["detail"]

    def test_send_message_access_other_user_conversation(
        self,
        client: TestClient,
        session: Session,
        test_user: User,
        test_user_2: User,
        auth_headers: dict
    ):
        """Test that user cannot access another user's conversation"""
        # Arrange - Create conversation for user 2
        conversation = Conversation(
            user_id=test_user_2.id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        chat_rate_limiter.requests.clear()

        # Act - User 1 tries to use User 2's conversation
        response = client.post(
            f"/api/{test_user.id}/chat",
            json={
                "conversation_id": str(conversation.id),
                "message": "Test message"
            },
            headers=auth_headers  # User 1's token
        )

        # Assert
        assert response.status_code == 403
        assert "another user" in response.json()["detail"]

    def test_send_message_empty_message(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict
    ):
        """Test validation error for empty message"""
        # Arrange
        chat_rate_limiter.requests.clear()

        # Act
        response = client.post(
            f"/api/{test_user.id}/chat",
            json={"message": ""},
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 422  # Validation error

    def test_send_message_too_long(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict
    ):
        """Test validation error for message exceeding max length"""
        # Arrange
        chat_rate_limiter.requests.clear()
        long_message = "x" * 5001  # Max is 5000

        # Act
        response = client.post(
            f"/api/{test_user.id}/chat",
            json={"message": long_message},
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 422  # Validation error


class TestListConversations:
    """Tests for GET /api/{user_id}/conversations endpoint"""

    def test_list_conversations_success(
        self,
        client: TestClient,
        session: Session,
        test_user: User,
        auth_headers: dict
    ):
        """Test listing user's conversations"""
        # Arrange - Create multiple conversations
        conversations = []
        for i in range(3):
            conv = Conversation(
                user_id=test_user.id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(conv)
            conversations.append(conv)

        session.commit()

        # Act
        response = client.get(
            f"/api/{test_user.id}/conversations",
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 200
        data = response.json()

        assert "conversations" in data
        assert "total" in data
        assert "limit" in data
        assert "offset" in data

        assert data["total"] == 3
        assert len(data["conversations"]) == 3

    def test_list_conversations_pagination(
        self,
        client: TestClient,
        session: Session,
        test_user: User,
        auth_headers: dict
    ):
        """Test pagination of conversations"""
        # Arrange - Create 5 conversations
        for i in range(5):
            conv = Conversation(
                user_id=test_user.id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            session.add(conv)

        session.commit()

        # Act
        response = client.get(
            f"/api/{test_user.id}/conversations?limit=2&offset=1",
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 200
        data = response.json()

        assert data["total"] == 5
        assert len(data["conversations"]) == 2
        assert data["limit"] == 2
        assert data["offset"] == 1

    def test_list_conversations_user_isolation(
        self,
        client: TestClient,
        session: Session,
        test_user: User,
        test_user_2: User,
        auth_headers: dict
    ):
        """Test that users only see their own conversations"""
        # Arrange - Create conversations for both users
        conv1 = Conversation(user_id=test_user.id, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
        conv2 = Conversation(user_id=test_user_2.id, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
        session.add(conv1)
        session.add(conv2)
        session.commit()

        # Act - User 1 lists their conversations
        response = client.get(
            f"/api/{test_user.id}/conversations",
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 200
        data = response.json()

        # Should only see their own conversation
        assert data["total"] == 1
        assert data["conversations"][0]["id"] == str(conv1.id)

    def test_list_conversations_requires_auth(
        self,
        client: TestClient,
        test_user: User
    ):
        """Test that authentication is required"""
        # Act
        response = client.get(f"/api/{test_user.id}/conversations")

        # Assert
        assert response.status_code == 401


class TestGetConversationHistory:
    """Tests for GET /api/{user_id}/conversations/{conversation_id} endpoint"""

    def test_get_conversation_history_success(
        self,
        client: TestClient,
        test_user: User,
        test_conversation: Conversation,
        test_messages: list,
        auth_headers: dict
    ):
        """Test retrieving conversation history"""
        # Act
        response = client.get(
            f"/api/{test_user.id}/conversations/{test_conversation.id}",
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 200
        data = response.json()

        assert "conversation" in data
        assert "messages" in data

        # Verify conversation details
        assert data["conversation"]["id"] == str(test_conversation.id)

        # Verify messages
        assert len(data["messages"]) == 2
        assert data["messages"][0]["role"] == "user"
        assert data["messages"][1]["role"] == "assistant"

    def test_get_conversation_not_found(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict
    ):
        """Test error when conversation doesn't exist"""
        # Arrange
        fake_id = uuid.uuid4()

        # Act
        response = client.get(
            f"/api/{test_user.id}/conversations/{fake_id}",
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 404

    def test_get_conversation_wrong_user(
        self,
        client: TestClient,
        session: Session,
        test_user: User,
        test_user_2: User,
        auth_headers: dict
    ):
        """Test that user cannot access another user's conversation"""
        # Arrange - Create conversation for user 2
        conv = Conversation(
            user_id=test_user_2.id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(conv)
        session.commit()
        session.refresh(conv)

        # Act - User 1 tries to access User 2's conversation
        response = client.get(
            f"/api/{test_user.id}/conversations/{conv.id}",
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 403


class TestDeleteConversation:
    """Tests for DELETE /api/{user_id}/conversations/{conversation_id} endpoint"""

    def test_delete_conversation_success(
        self,
        client: TestClient,
        session: Session,
        test_user: User,
        test_conversation: Conversation,
        test_messages: list,
        auth_headers: dict
    ):
        """Test deleting a conversation"""
        # Arrange
        conversation_id = test_conversation.id

        # Act
        response = client.delete(
            f"/api/{test_user.id}/conversations/{conversation_id}",
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 204

        # Verify conversation deleted from database
        conversation = session.get(Conversation, conversation_id)
        assert conversation is None

        # Verify messages also deleted (CASCADE)
        messages = session.exec(
            select(Message).where(Message.conversation_id == conversation_id)
        ).all()
        assert len(messages) == 0

    def test_delete_conversation_not_found(
        self,
        client: TestClient,
        test_user: User,
        auth_headers: dict
    ):
        """Test error when deleting non-existent conversation"""
        # Arrange
        fake_id = uuid.uuid4()

        # Act
        response = client.delete(
            f"/api/{test_user.id}/conversations/{fake_id}",
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 404

    def test_delete_conversation_wrong_user(
        self,
        client: TestClient,
        session: Session,
        test_user: User,
        test_user_2: User,
        auth_headers: dict
    ):
        """Test that user cannot delete another user's conversation"""
        # Arrange - Create conversation for user 2
        conv = Conversation(
            user_id=test_user_2.id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(conv)
        session.commit()
        session.refresh(conv)

        # Act - User 1 tries to delete User 2's conversation
        response = client.delete(
            f"/api/{test_user.id}/conversations/{conv.id}",
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 403

        # Verify conversation still exists
        conv_check = session.get(Conversation, conv.id)
        assert conv_check is not None


class TestErrorHandling:
    """Tests for error handling scenarios"""

    @patch('app.routes.chat.process_message_with_agent')
    def test_openai_rate_limit_error(
        self,
        mock_process: Mock,
        client: TestClient,
        test_user: User,
        auth_headers: dict
    ):
        """Test handling of OpenAI rate limit errors"""
        # Arrange
        from openai import RateLimitError
        mock_process.side_effect = RateLimitError(
            "Rate limit exceeded",
            response=Mock(status_code=429),
            body=None
        )
        chat_rate_limiter.requests.clear()

        # Act
        response = client.post(
            f"/api/{test_user.id}/chat",
            json={"message": "Test"},
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 503
        assert "Retry-After" in response.headers
        assert "busy" in response.json()["detail"].lower()

    @patch('app.routes.chat.process_message_with_agent')
    def test_openai_api_error(
        self,
        mock_process: Mock,
        client: TestClient,
        test_user: User,
        auth_headers: dict
    ):
        """Test handling of OpenAI API errors"""
        # Arrange
        from openai import APIError
        mock_process.side_effect = APIError(
            "API Error",
            request=Mock(),
            body=None
        )
        chat_rate_limiter.requests.clear()

        # Act
        response = client.post(
            f"/api/{test_user.id}/chat",
            json={"message": "Test"},
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 500
        assert "technical difficulties" in response.json()["detail"].lower()

    @patch('app.routes.chat.process_message_with_agent')
    def test_database_error(
        self,
        mock_process: Mock,
        client: TestClient,
        test_user: User,
        auth_headers: dict
    ):
        """Test handling of database errors"""
        # Arrange
        mock_process.side_effect = Exception("Database connection failed")
        chat_rate_limiter.requests.clear()

        # Act
        response = client.post(
            f"/api/{test_user.id}/chat",
            json={"message": "Test"},
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 500
        assert "temporarily unavailable" in response.json()["detail"].lower()


class TestRateLimiting:
    """Tests for rate limiting functionality"""

    @patch('app.routes.chat.process_message_with_agent')
    def test_rate_limit_enforcement(
        self,
        mock_process: Mock,
        client: TestClient,
        test_user: User,
        auth_headers: dict,
        mock_openai_response: dict
    ):
        """Test that rate limiting is enforced (30 req/min)"""
        # Arrange
        mock_process.return_value = mock_openai_response
        chat_rate_limiter.requests.clear()

        # Act - Send 31 requests rapidly
        for i in range(30):
            response = client.post(
                f"/api/{test_user.id}/chat",
                json={"message": f"Message {i}"},
                headers=auth_headers
            )
            assert response.status_code == 200

        # 31st request should be rate limited
        response = client.post(
            f"/api/{test_user.id}/chat",
            json={"message": "Message 31"},
            headers=auth_headers
        )

        # Assert
        assert response.status_code == 429
        assert "Retry-After" in response.headers
        assert "Rate limit exceeded" in response.json()["detail"]

    @patch('app.routes.chat.process_message_with_agent')
    def test_rate_limit_per_user(
        self,
        mock_process: Mock,
        client: TestClient,
        test_user: User,
        test_user_2: User,
        auth_headers: dict,
        auth_headers_2: dict,
        mock_openai_response: dict
    ):
        """Test that rate limiting is enforced per user"""
        # Arrange
        mock_process.return_value = mock_openai_response
        chat_rate_limiter.requests.clear()

        # Act - User 1 sends 30 requests
        for i in range(30):
            response = client.post(
                f"/api/{test_user.id}/chat",
                json={"message": f"Message {i}"},
                headers=auth_headers
            )
            assert response.status_code == 200

        # User 2 should still be able to send messages
        response = client.post(
            f"/api/{test_user_2.id}/chat",
            json={"message": "User 2 message"},
            headers=auth_headers_2
        )

        # Assert
        assert response.status_code == 200  # Not rate limited
