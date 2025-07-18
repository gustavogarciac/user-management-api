from datetime import datetime
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.application.use_cases.update_user import UpdateUserUseCase
from src.domain.entities.user import User
from src.domain.errors.domain_exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
)


@pytest.fixture
def update_user_use_case(
    mock_user_repository: AsyncMock,
) -> UpdateUserUseCase:
    return UpdateUserUseCase(
        user_repository=mock_user_repository,
    )


@pytest.mark.asyncio
async def test_update_user_success(
    update_user_use_case,
    mock_user_repository,
    create_mock_user,
):
    user_id = uuid4()
    existing_user = create_mock_user
    existing_user.id = user_id

    mock_user_repository.get_user_by_id.return_value = existing_user
    mock_user_repository.get_user_by_email.return_value = None
    mock_user_repository.get_user_by_username.return_value = None

    updated_user = User(
        id=user_id,
        username='newusername',
        email='newemail@example.com',
        password_hash=existing_user.password_hash,
        created_at=existing_user.created_at,
        updated_at=datetime.utcnow(),
    )
    mock_user_repository.update_user.return_value = updated_user

    result = await update_user_use_case.execute(
        user_id=user_id,
        username='newusername',
        email='newemail@example.com',
    )

    assert result.username == 'newusername'
    assert result.email == 'newemail@example.com'
    assert result.id == user_id

    mock_user_repository.get_user_by_id.assert_called_once_with(user_id)
    mock_user_repository.get_user_by_email.assert_called_once_with(
        'newemail@example.com'
    )
    mock_user_repository.get_user_by_username.assert_called_once_with(
        'newusername'
    )
    mock_user_repository.update_user.assert_called_once()


@pytest.mark.asyncio
async def test_update_user_partial_update(
    update_user_use_case,
    mock_user_repository,
    create_mock_user,
):
    user_id = uuid4()
    existing_user = create_mock_user
    existing_user.id = user_id

    mock_user_repository.get_user_by_id.return_value = existing_user
    mock_user_repository.get_user_by_email.return_value = None
    mock_user_repository.get_user_by_username.return_value = None

    updated_user = User(
        id=user_id,
        username='newusername',
        email=existing_user.email,
        password_hash=existing_user.password_hash,
        created_at=existing_user.created_at,
        updated_at=datetime.utcnow(),
    )
    mock_user_repository.update_user.return_value = updated_user

    result = await update_user_use_case.execute(
        user_id=user_id,
        username='newusername',
    )

    assert result.username == 'newusername'
    assert result.email == existing_user.email

    mock_user_repository.get_user_by_id.assert_called_once_with(user_id)
    mock_user_repository.get_user_by_username.assert_called_once_with(
        'newusername'
    )
    mock_user_repository.get_user_by_email.assert_not_called()
    mock_user_repository.update_user.assert_called_once()


@pytest.mark.asyncio
async def test_update_user_not_found(
    update_user_use_case,
    mock_user_repository,
):
    user_id = uuid4()
    mock_user_repository.get_user_by_id.return_value = None

    with pytest.raises(UserNotFoundError) as exc:
        await update_user_use_case.execute(
            user_id=user_id,
            username='newusername',
        )

    assert str(exc.value) == f'User with id {user_id} not found'
    mock_user_repository.get_user_by_id.assert_called_once_with(user_id)
    mock_user_repository.update_user.assert_not_called()


@pytest.mark.asyncio
async def test_update_user_duplicate_email(
    update_user_use_case,
    mock_user_repository,
    create_mock_user,
):
    user_id = uuid4()
    existing_user = create_mock_user
    existing_user.id = user_id

    existing_user.email = 'old@example.com'

    mock_user_repository.get_user_by_id.return_value = existing_user
    mock_user_repository.get_user_by_email.return_value = create_mock_user

    with pytest.raises(UserAlreadyExistsError) as exc:
        await update_user_use_case.execute(
            user_id=user_id,
            email='newemail@example.com',
        )

    assert str(exc.value) == (
        'User with email newemail@example.com already exists'
    )
    mock_user_repository.get_user_by_id.assert_called_once_with(user_id)
    mock_user_repository.get_user_by_email.assert_called_once_with(
        'newemail@example.com'
    )
    mock_user_repository.update_user.assert_not_called()


@pytest.mark.asyncio
async def test_update_user_duplicate_username(
    update_user_use_case,
    mock_user_repository,
    create_mock_user,
):
    user_id = uuid4()
    existing_user = create_mock_user
    existing_user.id = user_id

    existing_user.username = 'oldusername'

    mock_user_repository.get_user_by_id.return_value = existing_user
    mock_user_repository.get_user_by_email.return_value = None
    mock_user_repository.get_user_by_username.return_value = create_mock_user

    with pytest.raises(UserAlreadyExistsError) as exc:
        await update_user_use_case.execute(
            user_id=user_id,
            username='newusername',
        )

    assert str(exc.value) == 'User with username newusername already exists'
    mock_user_repository.get_user_by_id.assert_called_once_with(user_id)
    mock_user_repository.get_user_by_username.assert_called_once_with(
        'newusername'
    )
    mock_user_repository.update_user.assert_not_called()


@pytest.mark.asyncio
async def test_update_user_no_changes(
    update_user_use_case,
    mock_user_repository,
    create_mock_user,
):
    user_id = uuid4()
    existing_user = create_mock_user
    existing_user.id = user_id

    mock_user_repository.get_user_by_id.return_value = existing_user

    updated_user = User(
        id=user_id,
        username=existing_user.username,
        email=existing_user.email,
        password_hash=existing_user.password_hash,
        created_at=existing_user.created_at,
        updated_at=datetime.utcnow(),
    )
    mock_user_repository.update_user.return_value = updated_user

    result = await update_user_use_case.execute(
        user_id=user_id,
        username=existing_user.username,
        email=existing_user.email,
    )

    assert result.username == existing_user.username
    assert result.email == existing_user.email

    mock_user_repository.get_user_by_id.assert_called_once_with(user_id)
    mock_user_repository.get_user_by_email.assert_not_called()
    mock_user_repository.get_user_by_username.assert_not_called()
    mock_user_repository.update_user.assert_called_once()
