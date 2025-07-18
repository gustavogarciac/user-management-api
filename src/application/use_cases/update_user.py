from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from src.domain.entities.user import User
from src.domain.errors.domain_exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
)
from src.domain.ports.user_repository import UserRepository


class UpdateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(
        self,
        user_id: UUID,
        username: Optional[str] = None,
        email: Optional[str] = None,
    ) -> User:
        user = await self._get_existing_user(user_id)

        if email and email != user.email:
            await self._ensure_email_is_unique(email)

        if username and username != user.username:
            await self._ensure_username_is_unique(username)

        updated_user = UpdateUserUseCase._build_updated_user(
            user, username, email
        )
        return await self.user_repository.update_user(updated_user)

    async def _get_existing_user(self, user_id: UUID) -> User:
        user = await self.user_repository.get_user_by_id(user_id)
        if not user:
            raise UserNotFoundError(f'User with id {user_id} not found')
        return user

    async def _ensure_email_is_unique(self, email: str) -> None:
        if await self.user_repository.get_user_by_email(email):
            raise UserAlreadyExistsError(
                f'User with email {email} already exists'
            )

    async def _ensure_username_is_unique(self, username: str) -> None:
        if await self.user_repository.get_user_by_username(username):
            raise UserAlreadyExistsError(
                f'User with username {username} already exists'
            )

    @staticmethod
    def _build_updated_user(
        user: User, username: Optional[str], email: Optional[str]
    ) -> User:
        return User(
            id=user.id,
            username=username or user.username,
            email=email or user.email,
            password_hash=user.password_hash,
            created_at=user.created_at,
            updated_at=datetime.now(timezone.utc),
        )
