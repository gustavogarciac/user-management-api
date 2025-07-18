from src.domain.errors.domain_exceptions import CredentialsError
from src.domain.ports.auth_service import AuthService
from src.domain.ports.hash_service import HashService
from src.domain.ports.user_repository import UserRepository


class AuthenticateUserUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        hash_service: HashService,
        auth_service: AuthService,
    ):
        self.user_repository = user_repository
        self.hash_service = hash_service
        self.auth_service = auth_service

    async def execute(self, email: str, password: str) -> str:
        user = await self.user_repository.get_user_by_email(email)
        if not user:
            raise CredentialsError('Invalid credentials')

        if not self.hash_service.verify_password(password, user.password_hash):
            raise CredentialsError('Invalid credentials')

        return await self.auth_service.authenticate(email, password)
