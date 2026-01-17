"""
Test Configuration and Fixtures
Provides shared fixtures for database, authentication, and test client
"""

import pytest
import uuid
from datetime import datetime
from typing import Generator, Dict
from sqlmodel import Session, SQLModel, create_engine, select
from sqlmodel.pool import StaticPool
from fastapi.testclient import TestClient

from app.main import app
from app.database import get_session
from app.models import User, Task, Conversation, Message
from app.middleware.auth import create_access_token


# In-memory SQLite database for testing
@pytest.fixture(name="session")
def session_fixture() -> Generator[Session, None, None]:
    """
    Create a fresh in-memory database session for each test.

    Yields:
        Session: SQLModel database session
    """
    # Create in-memory SQLite engine
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Create all tables
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    # Cleanup after test
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(name="client")
def client_fixture(session: Session) -> Generator[TestClient, None, None]:
    """
    Create a test client with database session override.

    Args:
        session: Test database session

    Yields:
        TestClient: FastAPI test client
    """
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client

    app.dependency_overrides.clear()


@pytest.fixture(name="test_user")
def test_user_fixture(session: Session) -> User:
    """
    Create a test user in the database.

    Args:
        session: Database session

    Returns:
        User: Created test user
    """
    user = User(
        id="test_user_123",
        email="test@example.com",
        name="Test User",
        email_verified=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="test_user_2")
def test_user_2_fixture(session: Session) -> User:
    """
    Create a second test user for authorization testing.

    Args:
        session: Database session

    Returns:
        User: Created test user
    """
    user = User(
        id="test_user_456",
        email="test2@example.com",
        name="Test User 2",
        email_verified=True,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@pytest.fixture(name="auth_headers")
def auth_headers_fixture(test_user: User) -> Dict[str, str]:
    """
    Create authentication headers with valid JWT token.

    Args:
        test_user: Test user to create token for

    Returns:
        Dict: Headers with Authorization token
    """
    token = create_access_token(
        data={"sub": test_user.id, "user_id": test_user.id}
    )
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(name="auth_headers_2")
def auth_headers_2_fixture(test_user_2: User) -> Dict[str, str]:
    """
    Create authentication headers for second test user.

    Args:
        test_user_2: Second test user

    Returns:
        Dict: Headers with Authorization token
    """
    token = create_access_token(
        data={"sub": test_user_2.id, "user_id": test_user_2.id}
    )
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture(name="test_task")
def test_task_fixture(session: Session, test_user: User) -> Task:
    """
    Create a test task in the database.

    Args:
        session: Database session
        test_user: User who owns the task

    Returns:
        Task: Created test task
    """
    task = Task(
        user_id=test_user.id,
        title="Test Task",
        description="This is a test task",
        completed=False,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@pytest.fixture(name="test_conversation")
def test_conversation_fixture(session: Session, test_user: User) -> Conversation:
    """
    Create a test conversation in the database.

    Args:
        session: Database session
        test_user: User who owns the conversation

    Returns:
        Conversation: Created test conversation
    """
    conversation = Conversation(
        user_id=test_user.id,
        created_at=datetime.utcnow(),
        updated_at=datetime.utcnow()
    )
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return conversation


@pytest.fixture(name="test_messages")
def test_messages_fixture(
    session: Session,
    test_user: User,
    test_conversation: Conversation
) -> list[Message]:
    """
    Create test messages in a conversation.

    Args:
        session: Database session
        test_user: User who owns the messages
        test_conversation: Conversation containing the messages

    Returns:
        list[Message]: List of created test messages
    """
    messages = [
        Message(
            user_id=test_user.id,
            conversation_id=test_conversation.id,
            role="user",
            content="Hello, can you help me?",
            created_at=datetime.utcnow()
        ),
        Message(
            user_id=test_user.id,
            conversation_id=test_conversation.id,
            role="assistant",
            content="Of course! I'm here to help.",
            created_at=datetime.utcnow()
        )
    ]

    for message in messages:
        session.add(message)

    session.commit()

    for message in messages:
        session.refresh(message)

    return messages


@pytest.fixture(name="mock_openai_response")
def mock_openai_response_fixture():
    """
    Provides a mock OpenAI response structure for testing.

    Returns:
        Dict: Mock response data
    """
    return {
        "response": "I've added 'Buy groceries' to your tasks.",
        "tool_calls": [
            {
                "tool": "add_task",
                "arguments": {"title": "Buy groceries"},
                "result": {"success": True, "task_id": 1}
            }
        ]
    }
