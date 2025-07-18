from uuid import UUID

from src.domain.errors.domain_exceptions import UserNotFoundError
from src.domain.ports.user_repository import UserRepository


class DeleteUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, user_id: UUID) -> None:
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError(f'User with id {user_id} not found')

        await self.user_repository.delete_user(user_id)
