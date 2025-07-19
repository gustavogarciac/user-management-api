from datetime import datetime, timedelta, timezone
from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.application.use_cases.list_users import (
    ListUsersRequest,
    ListUsersUseCase,
)
from src.domain.entities.user import User
from src.domain.errors.domain_exceptions import (
    InvalidFilterError,
    InvalidOrderByError,
    InvalidOrderDirectionError,
    InvalidPageError,
    InvalidPageSizeError,
)
from src.domain.ports.user_repository import ListUsersConfig


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
    create_mock_user,
):
    mock_user = create_mock_user

    mock_user_repository.list_users.return_value = [mock_user]

    response = await list_users_use_case.execute(
        ListUsersRequest(
            page=1,
            page_size=10,
        )
    )

    expected_response = {
        'items': [mock_user],
        'page': 1,
        'page_size': 10,
        'total_items': 1,
    }

    assert response == expected_response
    mock_user_repository.list_users.assert_called_once_with(
        ListUsersConfig(
            page=1,
            page_size=10,
        )
    )


@pytest.mark.asyncio
async def test_list_users_empty(
    list_users_use_case,
    mock_user_repository,
):
    mock_user_repository.list_users.return_value = []

    response = await list_users_use_case.execute(
        ListUsersRequest(
            page=1,
            page_size=10,
        )
    )

    expected_response = {
        'items': [],
        'page': 1,
        'page_size': 10,
        'total_items': 0,
    }

    assert response == expected_response
    mock_user_repository.list_users.assert_called_once_with(
        ListUsersConfig(
            page=1,
            page_size=10,
        )
    )


@pytest.mark.asyncio
async def test_list_users_invalid_page(
    list_users_use_case,
    mock_user_repository,
):
    with pytest.raises(InvalidPageError):
        await list_users_use_case.execute(
            ListUsersRequest(
                page=0,
                page_size=10,
            )
        )

    mock_user_repository.list_users.assert_not_called()


@pytest.mark.asyncio
async def test_list_users_invalid_page_size(
    list_users_use_case,
    mock_user_repository,
):
    with pytest.raises(InvalidPageSizeError) as exc:
        await list_users_use_case.execute(
            ListUsersRequest(
                page=1,
                page_size=0,
            )
        )

    mock_user_repository.list_users.assert_not_called()

    assert str(exc.value) == 'Page size must be greater than 0'


@pytest.mark.asyncio
async def test_list_users_invalid_page_and_page_size_negative(
    list_users_use_case,
    mock_user_repository,
):
    with pytest.raises(InvalidPageError) as exc:
        await list_users_use_case.execute(
            ListUsersRequest(
                page=-1,
                page_size=-1,
            )
        )

    mock_user_repository.list_users.assert_not_called()

    assert str(exc.value) == 'Page must be greater than 0'


@pytest.mark.asyncio
async def test_list_users_invalid_page_and_page_size_zero(
    list_users_use_case,
    mock_user_repository,
):
    with pytest.raises(InvalidPageError) as exc:
        await list_users_use_case.execute(
            ListUsersRequest(
                page=0,
                page_size=0,
            )
        )

    assert str(exc.value) == 'Page must be greater than 0'


@pytest.mark.asyncio
async def test_list_users_invalid_page_size_greater_than_maximum(
    list_users_use_case,
    mock_user_repository,
):
    with pytest.raises(InvalidPageSizeError) as exc:
        await list_users_use_case.execute(
            ListUsersRequest(
                page=1,
                page_size=101,
            )
        )

    assert str(exc.value) == 'Page size must be less than 100'


@pytest.mark.asyncio
async def test_list_users_with_order_by(
    list_users_use_case,
    mock_user_repository,
    create_mock_user,
):
    first_mock_user = create_mock_user
    second_mock_user = User(
        id=uuid4(),
        username='testuser2',
        email='test2@example.com',
        password_hash='hashed_password',
        created_at=datetime.now(timezone.utc) + timedelta(days=1),
    )

    mock_user_repository.list_users.return_value = [
        first_mock_user,
        second_mock_user,
    ]

    response = await list_users_use_case.execute(
        ListUsersRequest(
            page=1,
            page_size=10,
            order_by='created_at',
            order_direction='asc',
        )
    )

    assert response['items'][0].created_at == first_mock_user.created_at
    assert response['items'][1].created_at == second_mock_user.created_at

    mock_user_repository.list_users.assert_called_once_with(
        ListUsersConfig(
            page=1,
            page_size=10,
            order_by='created_at',
            order_direction='asc',
        )
    )


@pytest.mark.asyncio
async def test_list_users_with_order_by_and_order_direction(
    list_users_use_case,
    mock_user_repository,
    create_mock_user,
):
    first_mock_user = create_mock_user
    second_mock_user = User(
        id=uuid4(),
        username='testuser2',
        email='test2@example.com',
        password_hash='hashed_password',
        created_at=datetime.now(timezone.utc) + timedelta(days=1),
    )

    mock_user_repository.list_users.return_value = [
        second_mock_user,
        first_mock_user,
    ]

    response = await list_users_use_case.execute(
        ListUsersRequest(
            page=1,
            page_size=10,
            order_by='created_at',
            order_direction='desc',
        )
    )

    assert response['items'][0].created_at == second_mock_user.created_at
    assert response['items'][1].created_at == first_mock_user.created_at

    mock_user_repository.list_users.assert_called_once_with(
        ListUsersConfig(
            page=1,
            page_size=10,
            order_by='created_at',
            order_direction='desc',
        )
    )


@pytest.mark.asyncio
async def test_list_users_with_invalid_order_by(
    list_users_use_case,
    mock_user_repository,
):
    with pytest.raises(InvalidOrderByError) as exc:
        await list_users_use_case.execute(
            ListUsersRequest(
                page=1,
                page_size=10,
                order_by='invalid_order_by',
                order_direction='asc',
            )
        )

    mock_user_repository.list_users.assert_not_called()

    assert str(exc.value) == (
        "Order by must be ['username', 'email', 'created_at']"
    )


@pytest.mark.asyncio
async def test_list_users_with_invalid_order_direction(
    list_users_use_case,
    mock_user_repository,
):
    with pytest.raises(InvalidOrderDirectionError) as exc:
        await list_users_use_case.execute(
            ListUsersRequest(
                page=1,
                page_size=10,
                order_by='created_at',
                order_direction='invalid_order_direction',
            )
        )

    mock_user_repository.list_users.assert_not_called()

    assert str(exc.value) == "Order direction must be ['asc', 'desc']"


@pytest.mark.asyncio
async def test_list_users_with_query(
    list_users_use_case,
    mock_user_repository,
    create_mock_user,
):
    second_mock_user = User(
        id=uuid4(),
        username='gustavo',
        email='gustavo@example.com',
        password_hash='hashed_password',
        created_at=datetime.now(timezone.utc) + timedelta(days=1),
    )

    mock_user_repository.list_users.return_value = [second_mock_user]

    response = await list_users_use_case.execute(
        ListUsersRequest(
            page=1,
            page_size=10,
            query='gustavo',
        )
    )

    assert response['items'] == [second_mock_user]
    assert response['total_items'] == 1

    mock_user_repository.list_users.assert_called_once_with(
        ListUsersConfig(
            page=1,
            page_size=10,
            query='gustavo',
        )
    )


@pytest.mark.asyncio
async def test_list_users_with_filters(
    list_users_use_case,
    mock_user_repository,
    create_mock_user,
):
    second_mock_user = User(
        id=uuid4(),
        username='gustavo',
        email='gustavo@example.com',
        password_hash='hashed_password',
        created_at=datetime.now(timezone.utc) + timedelta(days=1),
    )

    mock_user_repository.list_users.return_value = [
        second_mock_user,
    ]

    response = await list_users_use_case.execute(
        ListUsersRequest(
            page=1,
            page_size=10,
            filters={
                'username': 'gustavo',
            },
        )
    )

    assert response['items'] == [second_mock_user]
    assert response['total_items'] == 1

    mock_user_repository.list_users.assert_called_once_with(
        ListUsersConfig(
            page=1,
            page_size=10,
            filters={'username': 'gustavo'},
        )
    )


@pytest.mark.asyncio
async def test_list_users_with_invalid_filter(
    list_users_use_case,
    mock_user_repository,
):
    with pytest.raises(InvalidFilterError) as exc:
        await list_users_use_case.execute(
            ListUsersRequest(
                page=1,
                page_size=10,
                filters={
                    'invalid_filter': 'invalid_value',
                },
            )
        )

    mock_user_repository.list_users.assert_not_called()

    assert str(exc.value) == "Filter must be ['username', 'email']"
