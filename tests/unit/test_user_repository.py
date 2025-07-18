from unittest.mock import AsyncMock
from uuid import uuid4

import pytest

from src.domain.entities.user import User
from src.domain.ports.user_repository import ListUsersConfig, UserRepository


@pytest.fixture
def mock_repository():
    return AsyncMock(spec=UserRepository)


@pytest.fixture
def sample_user():
    return User(
        username='testuser',
        email='test@example.com',
        password_hash='hashed_password',
    )


@pytest.fixture
def list_config():
    return ListUsersConfig(page=1, page_size=10)


@pytest.mark.asyncio
async def test_create_user_abstract_method(mock_repository, sample_user):
    mock_repository.create_user.return_value = sample_user
    result = await mock_repository.create_user(sample_user)
    assert result == sample_user


@pytest.mark.asyncio
async def test_get_user_by_id_abstract_method(mock_repository):
    user_id = uuid4()
    mock_repository.get_user_by_id.return_value = None
    result = await mock_repository.get_user_by_id(user_id)
    assert result is None


@pytest.mark.asyncio
async def test_get_user_by_email_abstract_method(mock_repository):
    email = 'test@example.com'
    mock_repository.get_user_by_email.return_value = None
    result = await mock_repository.get_user_by_email(email)
    assert result is None


@pytest.mark.asyncio
async def test_get_user_by_username_abstract_method(mock_repository):
    mock_repository.get_user_by_username.return_value = None
    result = await mock_repository.get_user_by_username('testuser')
    assert result is None


@pytest.mark.asyncio
async def test_update_user_abstract_method(mock_repository, sample_user):
    mock_repository.update_user.return_value = sample_user
    result = await mock_repository.update_user(sample_user)
    assert result == sample_user


@pytest.mark.asyncio
async def test_delete_user_abstract_method(mock_repository):
    user_id = uuid4()
    await mock_repository.delete_user(user_id)


@pytest.mark.asyncio
async def test_list_users_abstract_method(mock_repository, list_config):
    mock_repository.list_users.return_value = []
    result = await mock_repository.list_users(list_config)
    assert result == []


def test_list_users_config_dataclass():
    config = ListUsersConfig(page=1, page_size=10)

    expected_config = ListUsersConfig(page=1, page_size=10)

    assert config == expected_config


def test_list_users_config_with_optional_fields():
    config = ListUsersConfig(
        page=2,
        page_size=20,
        query='test',
        order_by='username',
        order_direction='asc',
        filters={'username': 'testuser'},
    )

    expected_config = ListUsersConfig(
        page=2,
        page_size=20,
        query='test',
        order_by='username',
        order_direction='asc',
        filters={'username': 'testuser'},
    )

    assert config == expected_config


def test_user_repository_is_abstract():
    with pytest.raises(TypeError):
        UserRepository()
