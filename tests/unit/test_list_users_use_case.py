from datetime import datetime
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.application.use_cases.list_users import ListUsersUseCase
from src.domain.entities.user import User
from src.domain.errors.domain_exceptions import (
    InvalidPageError,
    InvalidPageSizeError,
)


@pytest.fixture
def list_users_use_case(
    mock_user_repository: AsyncMock,
) -> ListUsersUseCase:
    return ListUsersUseCase(
        user_repository=mock_user_repository,
    )


@pytest.mark.asyncio
async def test_list_users_success(
    list_users_use_case,
    mock_user_repository,
):
    mock_user_repository.list_users.return_value = [
        User(
            id=uuid4(),
            username='testuser',
            email='test@example.com',
            password_hash='hashed_password',
            created_at=datetime.utcnow(),
        ),
    ]

    users = await list_users_use_case.execute(
        page=1,
        page_size=10,
    )

    assert users[0].username == 'testuser'
    assert users[0].email == 'test@example.com'
    assert users[0].password_hash == 'hashed_password'
    mock_user_repository.list_users.assert_called_once_with(1, 10)


@pytest.mark.asyncio
async def test_list_users_empty(
    list_users_use_case,
    mock_user_repository,
):
    mock_user_repository.list_users.return_value = []

    users = await list_users_use_case.execute(
        page=1,
        page_size=10,
    )

    assert users == []
    mock_user_repository.list_users.assert_called_once_with(1, 10)


@pytest.mark.asyncio
async def test_list_users_invalid_page(
    list_users_use_case,
    mock_user_repository,
):
    with pytest.raises(InvalidPageError):
        await list_users_use_case.execute(page=0, page_size=10)

    mock_user_repository.list_users.assert_not_called()


@pytest.mark.asyncio
async def test_list_users_invalid_page_size(
    list_users_use_case,
    mock_user_repository,
):
    with pytest.raises(InvalidPageError) as exc:
        await list_users_use_case.execute(page=1, page_size=0)

    mock_user_repository.list_users.assert_not_called()

    assert str(exc.value) == 'Page and page_size must be greater than 0'


@pytest.mark.asyncio
async def test_list_users_invalid_page_and_page_size_negative(
    list_users_use_case,
    mock_user_repository,
):
    with pytest.raises(InvalidPageError) as exc:
        await list_users_use_case.execute(page=-1, page_size=-1)

    mock_user_repository.list_users.assert_not_called()

    assert str(exc.value) == 'Page and page_size must be greater than 0'


@pytest.mark.asyncio
async def test_list_users_invalid_page_and_page_size_zero(
    list_users_use_case,
    mock_user_repository,
):
    with pytest.raises(InvalidPageError) as exc:
        await list_users_use_case.execute(page=0, page_size=0)

    assert str(exc.value) == 'Page and page_size must be greater than 0'


@pytest.mark.asyncio
async def test_list_users_invalid_page_size_greater_than_maximum(
    list_users_use_case,
    mock_user_repository,
):
    with pytest.raises(InvalidPageSizeError) as exc:
        await list_users_use_case.execute(page=1, page_size=101)

    assert str(exc.value) == 'Page size must be less than 100'
