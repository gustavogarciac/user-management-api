from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.repositories.user_repository_implementation import (
    UserRepositoryImplementation,
)
from src.application.use_cases.delete_user import DeleteUserUseCase


def delete_user_factory(session: AsyncSession) -> DeleteUserUseCase:
    user_repository = UserRepositoryImplementation(session)

    return DeleteUserUseCase(user_repository)
