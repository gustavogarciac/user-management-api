from datetime import datetime
from unittest.mock import AsyncMock, Mock
from uuid import uuid4

import pytest

from src.application.use_cases.create_user import CreateUserUseCase
from src.domain.entities.user import User
from src.domain.errors.domain_exceptions import UserAlreadyExistsError


@pytest.fixture
def create_user_use_case(
    mock_user_repository: AsyncMock,
    mock_hash_repository: Mock,
) -> CreateUserUseCase:
    return CreateUserUseCase(
        user_repository=mock_user_repository,
        hash_repository=mock_hash_repository,
    )


@pytest.mark.asyncio
async def test_create_user_success(
    create_user_use_case,
    mock_user_repository,
    mock_hash_repository,
):
    mock_user_repository.get_user_by_email.return_value = None
    mock_user_repository.get_user_by_username.return_value = None
    mock_hash_repository.hash_password.return_value = 'hashed_password'

    mock_user_repository.create_user.return_value = User(
        id=uuid4(),
        username='testuser',
        email='test@example.com',
        password_hash='hashed_password',
        created_at=datetime.utcnow(),
    )

    user = await create_user_use_case.execute(
        username='testuser',
        email='test@example.com',
        password='password',
    )

    assert user.username == 'testuser'
    assert user.email == 'test@example.com'
    assert user.password_hash == 'hashed_password'
    mock_hash_repository.hash_password.assert_called_once_with('password')
    mock_user_repository.create_user.assert_called_once()


@pytest.mark.asyncio
async def test_create_user_duplicate_email(
    create_user_use_case,
    mock_user_repository,
    create_mock_user,
):
    # Arrange
    mock_user_repository.get_user_by_email.return_value = create_mock_user

    with pytest.raises(UserAlreadyExistsError) as exc:
        await create_user_use_case.execute(
            username='testuser',
            email='test@example.com',
            password='password',
        )
    assert str(exc.value) == (
        'User with email test@example.com already exists'
    )


@pytest.mark.asyncio
async def test_create_user_duplicate_username(
    create_user_use_case,
    mock_user_repository,
    create_mock_user,
):
    # Arrange
    mock_user_repository.get_user_by_email.return_value = None
    mock_user_repository.get_user_by_username.return_value = create_mock_user

    with pytest.raises(UserAlreadyExistsError) as exc:
        await create_user_use_case.execute(
            username='testuser',
            email='test@example.com',
            password='password',
        )
    assert str(exc.value) == ('User with username testuser already exists')
