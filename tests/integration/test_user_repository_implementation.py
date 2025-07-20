from datetime import datetime, timezone
from uuid import uuid4

import pytest

from src.adapters.repositories.user_repository_implementation import (
    UserRepositoryImplementation,
)
from src.application.use_cases.list_users import ListUsersConfig
from src.domain.entities.user import User
from src.domain.errors.domain_exceptions import UserNotFoundError


@pytest.mark.asyncio
async def test_create_and_get_user_by_id(
    user_repository: UserRepositoryImplementation,
):
    user = User(
        username='testuser',
        email='test@example.com',
        password_hash='hashed_password',
    )

    created_user = await user_repository.create_user(user)
    fetched_user = await user_repository.get_user_by_id(created_user.id)

    assert fetched_user is not None
    assert fetched_user.username == 'testuser'
    assert fetched_user.email == 'test@example.com'
    assert fetched_user.password_hash == 'hashed_password'
    assert fetched_user.id == created_user.id

    assert created_user.id is not None
    assert created_user.email == 'test@example.com'


@pytest.mark.asyncio
async def test_get_user_by_email(
    user_repository: UserRepositoryImplementation,
    make_user,
):
    user = await make_user()

    # Act
    fetched_user = await user_repository.get_user_by_email('test@example.com')

    # Assert
    assert fetched_user is not None
    assert fetched_user.email == 'test@example.com'
    assert fetched_user.id == user.id


@pytest.mark.asyncio
async def test_get_user_by_email_not_found(
    user_repository: UserRepositoryImplementation,
):
    assert (
        await user_repository.get_user_by_email('nonexistent@example.com')
        is None
    )


@pytest.mark.asyncio
async def test_get_user_by_username(
    user_repository: UserRepositoryImplementation,
    make_user,
):
    user = await make_user()

    fetched_user = await user_repository.get_user_by_username('testuser')

    assert fetched_user is not None
    assert fetched_user.username == 'testuser'
    assert fetched_user.id == user.id


@pytest.mark.asyncio
async def test_get_user_by_username_not_found(
    user_repository: UserRepositoryImplementation,
):
    assert await user_repository.get_user_by_username('nonexistent') is None


@pytest.mark.asyncio
async def test_get_user_by_id_not_found(
    user_repository: UserRepositoryImplementation,
):
    assert await user_repository.get_user_by_id(uuid4()) is None


@pytest.mark.asyncio
async def test_update_user(
    user_repository: UserRepositoryImplementation,
    make_user,
):
    user = await make_user()

    updated_user = User(
        id=user.id,
        username='updateduser',
        email='updated@example.com',
        password_hash='new_hash',
        created_at=user.created_at,
        updated_at=datetime.now(timezone.utc),
    )
    result = await user_repository.update_user(updated_user)

    assert result.username == 'updateduser'
    assert result.email == 'updated@example.com'
    assert result.password_hash == 'new_hash'

    fetched_user = await user_repository.get_user_by_id(user.id)
    assert fetched_user.username == 'updateduser'
    assert fetched_user.email == 'updated@example.com'


@pytest.mark.asyncio
async def test_update_user_not_found(
    user_repository: UserRepositoryImplementation,
):
    user = User(
        id=uuid4(),
        username='testuser',
        email='test@example.com',
        password_hash='hashed_password',
    )

    with pytest.raises(UserNotFoundError):
        await user_repository.update_user(user)


@pytest.mark.asyncio
async def test_delete_user(
    user_repository: UserRepositoryImplementation,
    make_user,
):
    created_user = await make_user()

    await user_repository.delete_user(created_user.id)

    deleted_user = await user_repository.get_user_by_id(created_user.id)
    assert deleted_user is None


@pytest.mark.asyncio
async def test_delete_user_not_found(
    user_repository: UserRepositoryImplementation,
):
    with pytest.raises(UserNotFoundError):
        await user_repository.delete_user(uuid4())


@pytest.mark.asyncio
async def test_list_users_with_pagination(
    user_repository: UserRepositoryImplementation,
    make_user,
):
    # Arrange
    users = []
    for i in range(5):
        user = await make_user(
            username=f'user{i}',
            email=f'user{i}@example.com',
        )
        users.append(user)

    # Act
    config = ListUsersConfig(page=1, page_size=3)
    result = await user_repository.list_users(config)

    expected_length = 3

    # Assert
    assert len(result) == expected_length
    assert result[0].username == 'user0'
    assert result[1].username == 'user1'
    assert result[2].username == 'user2'


@pytest.mark.asyncio
async def test_list_users_with_query(
    user_repository: UserRepositoryImplementation,
    make_user,
):
    await make_user(username='testuser', email='test@example.com')
    await make_user(username='otheruser', email='other@example.com')

    config = ListUsersConfig(page=1, page_size=10, query='test')
    result = await user_repository.list_users(config)

    assert len(result) == 1
    assert result[0].username == 'testuser'


@pytest.mark.asyncio
async def test_list_users_with_query_not_found(
    user_repository: UserRepositoryImplementation,
    make_user,
):
    await make_user(username='testuser', email='test@example.com')
    await make_user(username='otheruser', email='other@example.com')

    config = ListUsersConfig(page=1, page_size=10, query='nonexistent')
    result = await user_repository.list_users(config)

    assert len(result) == 0


@pytest.mark.asyncio
async def test_list_users_with_filters(
    user_repository: UserRepositoryImplementation,
    make_user,
):
    await make_user(username='user1', email='user1@example.com')
    await make_user(username='user2', email='user2@example.com')

    config = ListUsersConfig(
        page=1, page_size=10, filters={'username': 'user1'}
    )
    result = await user_repository.list_users(config)

    assert len(result) == 1
    assert result[0].username == 'user1'


@pytest.mark.asyncio
async def test_list_users_with_order_by(
    user_repository: UserRepositoryImplementation,
    make_user,
):
    await make_user(username='auser', email='auser@example.com')
    await make_user(username='buser', email='buser@example.com')

    config = ListUsersConfig(
        page=1, page_size=10, order_by='username', order_direction='desc'
    )
    result = await user_repository.list_users(config)

    assert result[0].username == 'buser'
    assert result[1].username == 'auser'


@pytest.mark.asyncio
async def test_list_users_with_order_by_and_order_direction(
    user_repository: UserRepositoryImplementation,
    make_user,
):
    await make_user(username='auser', email='auser@example.com')
    await make_user(username='buser', email='buser@example.com')

    config = ListUsersConfig(
        page=1, page_size=10, order_by='username', order_direction='asc'
    )
    result = await user_repository.list_users(config)

    assert result[0].username == 'auser'
    assert result[1].username == 'buser'


@pytest.mark.asyncio
async def test_count_users_total(
    user_repository: UserRepositoryImplementation,
    make_user,
):
    for i in range(5):
        await make_user(
            username=f'user{i}',
            email=f'user{i}@example.com',
        )

    config = ListUsersConfig(page=1, page_size=10)
    total = await user_repository.count_users(config)

    expected_total = 5

    assert total == expected_total


@pytest.mark.asyncio
async def test_count_users_with_query(
    user_repository: UserRepositoryImplementation,
    make_user,
):
    # Arrange
    await make_user(username='testuser', email='test@example.com')
    await make_user(username='otheruser', email='other@example.com')

    # Act
    config = ListUsersConfig(page=1, page_size=10, query='test')
    total = await user_repository.count_users(config)

    # Assert
    assert total == 1


@pytest.mark.asyncio
async def test_count_users_with_filters(
    user_repository: UserRepositoryImplementation,
    make_user,
):
    # Arrange
    await make_user(username='user1', email='user1@example.com')
    await make_user(username='user2', email='user2@example.com')

    # Act
    config = ListUsersConfig(
        page=1, page_size=10, filters={'username': 'user1'}
    )
    total = await user_repository.count_users(config)

    # Assert
    assert total == 1


@pytest.mark.asyncio
async def test_count_users_with_query_and_filters(
    user_repository: UserRepositoryImplementation,
    make_user,
):
    # Arrange
    await make_user(username='testuser1', email='test1@example.com')
    await make_user(username='testuser2', email='test2@example.com')
    await make_user(username='otheruser', email='other@example.com')

    # Act
    config = ListUsersConfig(
        page=1,
        page_size=10,
        query='test',
        filters={'email': 'test1@example.com'},
    )
    total = await user_repository.count_users(config)

    # Assert
    assert total == 1
