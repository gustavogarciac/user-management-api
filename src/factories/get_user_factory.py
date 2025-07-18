from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.repositories.user_repository_implementation import (
    UserRepositoryImplementation,
)
from src.application.use_cases.get_user import GetUserUseCase


def get_user_factory(session: AsyncSession) -> GetUserUseCase:
    user_repository = UserRepositoryImplementation(session)

    return GetUserUseCase(user_repository)
