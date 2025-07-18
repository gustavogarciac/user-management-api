from src.domain.entities.user import User
from src.domain.errors.domain_exceptions import (
    InvalidPageError,
    InvalidPageSizeError,
)
from src.domain.ports.user_repository import UserRepository


class ListUsersUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    MAXIMUM_PAGE_SIZE = 100

    async def execute(self, page: int, page_size: int) -> list[User]:
        if page <= 0 or page_size <= 0:
            raise InvalidPageError('Page and page_size must be greater than 0')

        if page_size > self.MAXIMUM_PAGE_SIZE:
            raise InvalidPageSizeError(
                f'Page size must be less than {self.MAXIMUM_PAGE_SIZE}'
            )

        users = await self.user_repository.list_users(page, page_size)

        return users
