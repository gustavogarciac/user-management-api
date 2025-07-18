from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.repositories.user_repository_implementation import (
    UserRepositoryImplementation,
)
from src.application.use_cases.list_users import ListUsersUseCase


def list_users_factory(session: AsyncSession) -> ListUsersUseCase:
    user_repository = UserRepositoryImplementation(session)

    return ListUsersUseCase(user_repository)
