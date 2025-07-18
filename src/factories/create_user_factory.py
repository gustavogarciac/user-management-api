from src.application.use_cases.create_user import CreateUserUseCase
from src.adapters.repositories.user_repository_implementation import UserRepositoryImplementation
from src.adapters.auth.pwdlib_password_hasher import HashServiceImplementation


def create_user_factory() -> CreateUserUseCase:
    user_repository = UserRepositoryImplementation()
    hash_repository = HashServiceImplementation()

    return CreateUserUseCase(user_repository, hash_repository)