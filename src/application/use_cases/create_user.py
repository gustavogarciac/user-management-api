from src.domain.entities.user import User
from src.domain.errors.domain_exceptions import UserAlreadyExistsError
from src.domain.ports.hash_service import HashService
from src.domain.ports.user_repository import UserRepository


class CreateUserUseCase:
    def __init__(
        self, user_repository: UserRepository, hash_repository: HashService
    ):
        self.user_repository = user_repository
        self.hash_repository = hash_repository

    async def execute(self, username: str, email: str, password: str) -> User:
        existing_user = await self.user_repository.get_user_by_email(email)
        if existing_user:
            raise UserAlreadyExistsError(
                f'User with email {email} already exists'
            )

        existing_user = await self.user_repository.get_user_by_username(
            username
        )
        if existing_user:
            raise UserAlreadyExistsError(
                f'User with username {username} already exists'
            )

        password_hash = self.hash_repository.hash_password(password)

        user = User(
            username=username,
            email=email,
            password_hash=password_hash,
        )

        return await self.user_repository.create_user(user)
