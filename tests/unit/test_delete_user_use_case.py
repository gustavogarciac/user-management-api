from datetime import datetime
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.application.use_cases.delete_user import DeleteUserUseCase
from src.domain.entities.user import User
from src.domain.errors.domain_exceptions import UserNotFoundError


@pytest.fixture
def delete_user_use_case(
    mock_user_repository: AsyncMock,
) -> DeleteUserUseCase:
    return DeleteUserUseCase(
        user_repository=mock_user_repository,
    )


@pytest.mark.asyncio
async def test_delete_user_success(
    delete_user_use_case,
    mock_user_repository,
):
    user_id = uuid4()

    mock_user_repository.get_user_by_id.return_value = User(
        id=user_id,
        username='testuser',
        email='test@example.com',
        password_hash='hashed_password',
        created_at=datetime.utcnow(),
    )

    await delete_user_use_case.execute(
        user_id=user_id,
    )

    mock_user_repository.get_user_by_id.assert_called_once_with(user_id)
    mock_user_repository.delete_user.assert_called_once_with(user_id)


@pytest.mark.asyncio
async def test_delete_user_not_found(
    delete_user_use_case,
    mock_user_repository,
):
    user_id = uuid4()
    mock_user_repository.get_user_by_id.return_value = None

    with pytest.raises(UserNotFoundError):
        await delete_user_use_case.execute(user_id=user_id)

    mock_user_repository.get_user_by_id.assert_called_once_with(user_id)
    mock_user_repository.delete_user.assert_not_called()
