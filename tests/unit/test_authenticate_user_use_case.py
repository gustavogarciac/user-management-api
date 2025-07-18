from datetime import datetime
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.application.use_cases.authenticate_user import AuthenticateUserUseCase
from src.domain.entities.user import User
from src.domain.errors.domain_exceptions import CredentialsError


@pytest.fixture
def authenticate_user_use_case(
    mock_user_repository: AsyncMock,
    mock_hash_repository: AsyncMock,
    mock_auth_service: AsyncMock,
) -> AuthenticateUserUseCase:
    return AuthenticateUserUseCase(
        user_repository=mock_user_repository,
        hash_service=mock_hash_repository,
        auth_service=mock_auth_service,
    )


@pytest.mark.asyncio
async def test_authenticate_user_success(
    authenticate_user_use_case,
    mock_user_repository,
    mock_hash_repository,
    mock_auth_service,
):
    email = 'test@example.com'
    password = 'password'

    mock_user_repository.get_user_by_email.return_value = User(
        id=uuid4(),
        username='testuser',
        email=email,
        password_hash='hashed_password',
        created_at=datetime.utcnow(),
    )
    mock_hash_repository.verify_password.return_value = True
    mock_auth_service.authenticate.return_value = 'valid_token'

    token = await authenticate_user_use_case.execute(email, password)

    assert token is not None
    mock_user_repository.get_user_by_email.assert_called_once_with(email)
    mock_hash_repository.verify_password.assert_called_once_with(
        password,
        'hashed_password',
    )
    mock_auth_service.authenticate.assert_called_once_with(email, password)


@pytest.mark.asyncio
async def test_authenticate_user_invalid_email(
    authenticate_user_use_case,
    mock_user_repository,
    mock_hash_repository,
    mock_auth_service,
):
    email = 'invalid@example.com'
    password = 'password'

    mock_user_repository.get_user_by_email.return_value = None

    with pytest.raises(CredentialsError):
        await authenticate_user_use_case.execute(email, password)

    mock_user_repository.get_user_by_email.assert_called_once_with(email)
    mock_hash_repository.verify_password.assert_not_called()
    mock_auth_service.authenticate.assert_not_called()


@pytest.mark.asyncio
async def test_authenticate_user_invalid_password(
    authenticate_user_use_case,
    mock_user_repository,
    mock_hash_repository,
    mock_auth_service,
):
    email = 'test@example.com'
    password = 'wrong_password'

    mock_user_repository.get_user_by_email.return_value = User(
        id=uuid4(),
        username='testuser',
        email=email,
        password_hash='hashed_password',
        created_at=datetime.utcnow(),
    )
    mock_hash_repository.verify_password.return_value = False

    with pytest.raises(CredentialsError):
        await authenticate_user_use_case.execute(email, password)

    mock_user_repository.get_user_by_email.assert_called_once_with(email)
    mock_hash_repository.verify_password.assert_called_once_with(
        password,
        'hashed_password',
    )
    mock_auth_service.authenticate.assert_not_called()
