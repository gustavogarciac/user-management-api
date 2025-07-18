from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.auth.jwt_auth_service import JwtAuthService
from src.adapters.auth.pwdlib_password_hasher import PwdlibPasswordHasher
from src.adapters.repositories.user_repository_implementation import (
    UserRepositoryImplementation,
)
from src.application.use_cases.authenticate_user import AuthenticateUserUseCase


def authenticate_user_factory(
    session: AsyncSession,
) -> AuthenticateUserUseCase:
    user_repository = UserRepositoryImplementation(session)
    hash_service = PwdlibPasswordHasher()
    auth_service = JwtAuthService()

    return AuthenticateUserUseCase(user_repository, hash_service, auth_service)
