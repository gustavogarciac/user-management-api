import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.repositories.user_repository_implementation import (
    UserRepositoryImplementation,
)
from src.domain.entities.user import User


@pytest.fixture
def user_repository(
    async_session: AsyncSession,
) -> UserRepositoryImplementation:
    return UserRepositoryImplementation(async_session)


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
