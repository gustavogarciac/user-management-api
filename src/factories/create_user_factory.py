from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.auth.pwdlib_password_hasher import PwdlibPasswordHasher
from src.adapters.repositories.user_repository_implementation import (
    UserRepositoryImplementation,
)
from src.application.use_cases.create_user import CreateUserUseCase


def create_user_factory(session: AsyncSession) -> CreateUserUseCase:
    user_repository = UserRepositoryImplementation(session)
    hash_repository = PwdlibPasswordHasher()

    return CreateUserUseCase(user_repository, hash_repository)
