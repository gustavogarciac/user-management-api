from abc import ABC, abstractmethod
from typing import Optional

from src.domain.entities.user import User


class AuthService(ABC):
    @abstractmethod
    async def authenticate(self, email: str, password: str) -> Optional[str]:
        pass

    @abstractmethod
    async def validate_token(self, token: str) -> Optional[User]:
        pass
