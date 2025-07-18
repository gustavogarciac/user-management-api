from datetime import datetime, timezone
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from src.domain.entities.user import User


@pytest.fixture
def mock_user_repository():
    return AsyncMock()


@pytest.fixture
def mock_hash_repository():
    return Mock()


@pytest.fixture
def mock_auth_service():
    return AsyncMock()


@pytest.fixture
def create_mock_user(
    username: str = 'testuser',
    email: str = 'test@example.com',
    password_hash: str = 'hashed_password',
    created_at: datetime | None = None,
) -> User:
    if created_at is None:
        created_at = datetime.now(timezone.utc)

    return User(
        id=uuid4(),
        username=username,
        email=email,
        password_hash=password_hash,
        created_at=created_at,
    )
