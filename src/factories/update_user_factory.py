from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.repositories.user_repository_implementation import (
    UserRepositoryImplementation,
)
from src.application.use_cases.update_user import UpdateUserUseCase


def update_user_factory(session: AsyncSession) -> UpdateUserUseCase:
    user_repository = UserRepositoryImplementation(session)

    return UpdateUserUseCase(user_repository)
