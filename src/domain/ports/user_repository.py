from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from pydantic import EmailStr

from src.domain.entities.user import User


@dataclass
class ListUsersConfig:
    page: int
    page_size: int
    query: str | None = None
    order_by: str | None = None
    order_direction: str | None = None
    filters: dict[str, str] | None = None


class UserRepository(ABC):
    @abstractmethod
    async def create_user(self, user: User) -> User:
        pass

    @abstractmethod
    async def get_user_by_id(self, user_id: UUID) -> Optional[User]:
        pass

    @abstractmethod
    async def get_user_by_email(self, email: EmailStr) -> Optional[User]:
        pass

    @abstractmethod
    async def get_user_by_username(self, username: str) -> Optional[User]:
        pass

    @abstractmethod
    async def update_user(self, user: User) -> User:
        pass

    @abstractmethod
    async def delete_user(self, user_id: UUID) -> None:
        pass

    @abstractmethod
    async def list_users(
        self,
        config: ListUsersConfig,
    ) -> list[User]:
        pass
