from uuid import UUID

from pydantic import EmailStr
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.user import User
from src.domain.errors.domain_exceptions import UserNotFoundError
from src.domain.ports.user_repository import ListUsersConfig, UserRepository
from src.infrastructure.database.sqlite_db import UserORM


class UserRepositoryImplementation(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(self, user: User) -> User:
        user_orm = UserORM(**user.model_dump())
        self.session.add(user_orm)
        await self.session.commit()
        await self.session.refresh(user_orm)
        return User(**user_orm.__dict__)

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        result = await self.session.execute(
            select(UserORM).where(UserORM.id == user_id)
        )
        user_orm = result.scalar_one_or_none()
        if not user_orm:
            return None
        return User(**user_orm.__dict__)

    async def get_user_by_email(self, email: EmailStr) -> User | None:
        result = await self.session.execute(
            select(UserORM).where(UserORM.email == email)
        )
        user_orm = result.scalar_one_or_none()
        if not user_orm:
            return None
        return User(**user_orm.__dict__)

    async def get_user_by_username(self, username: str) -> User | None:
        result = await self.session.execute(
            select(UserORM).where(UserORM.username == username)
        )
        user_orm = result.scalar_one_or_none()
        if not user_orm:
            return None
        return User(**user_orm.__dict__)

    async def update_user(self, user: User) -> User:
        result = await self.session.execute(
            select(UserORM).where(UserORM.id == user.id)
        )
        user_orm = result.scalar_one_or_none()

        if user_orm is None:
            raise UserNotFoundError(f'User with id {user.id} not found')

        for key, value in user.model_dump().items():
            setattr(user_orm, key, value)

        await self.session.commit()
        await self.session.refresh(user_orm)

        return User(**user_orm.__dict__)

    async def delete_user(self, user_id: UUID) -> None:
        result = await self.session.execute(
            select(UserORM).where(UserORM.id == user_id)
        )

        user_orm = result.scalar_one_or_none()

        if user_orm is None:
            raise UserNotFoundError(f'User with id {user_id} not found')

        await self.session.delete(user_orm)
        await self.session.commit()

    async def list_users(self, config: ListUsersConfig) -> list[User]:
        query = select(UserORM)

        if config.query:
            query = query.where(UserORM.username.ilike(f'%{config.query}%'))

        if config.filters:
            for key, value in config.filters.items():
                query = query.where(getattr(UserORM, key) == value)

        if config.order_by:
            order_column = getattr(UserORM, config.order_by)
            if config.order_direction == 'asc':
                query = query.order_by(order_column.asc())
            else:
                query = query.order_by(order_column.desc())

        if config.page and config.page_size:
            offset = (config.page - 1) * config.page_size
            query = query.offset(offset).limit(config.page_size)

        result = await self.session.execute(query)
        users_orm = result.scalars().all()

        return [User(**user.__dict__) for user in users_orm]
