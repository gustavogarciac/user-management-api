from abc import ABC, abstractmethod
from typing import List, Optional
from uuid import UUID

from pydantic import EmailStr

from src.domain.entities.user import User


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
    async def update_user(self, user: User) -> User:
        pass

    @abstractmethod
    async def delete_user(self, user_id: UUID) -> None:
        pass

    @abstractmethod
    async def list_users(self, page: int, page_size: int) -> List[User]:
        pass
