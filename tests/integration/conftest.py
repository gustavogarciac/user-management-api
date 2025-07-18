from datetime import datetime
from typing import Awaitable, Callable
from uuid import UUID, uuid4

import pytest
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.adapters.repositories.user_repository_implementation import (
    UserRepositoryImplementation,
)
from src.infrastructure.database.sqlite_db import Base, UserORM


@pytest.fixture
async def async_session():
    engine = create_async_engine('sqlite+aiosqlite:///:memory:', echo=True)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session

    await engine.dispose()


@pytest.fixture
async def user_repository(
    async_session: AsyncSession,
) -> UserRepositoryImplementation:
    return UserRepositoryImplementation(async_session)


@pytest.fixture
async def make_user(async_session: AsyncSession) -> Callable[[], UserORM]:
    async def _make_user(
        username: str = 'testuser',
        email: str = 'test@example.com',
        password_hash: str = 'hashed_password',
    ) -> UserORM:
        user = UserORM(
            id=uuid4(),
            username=username,
            email=email,
            password_hash=password_hash,
        )
        async_session.add(user)
        await async_session.commit()
        await async_session.refresh(user)
        return user

    return _make_user


@pytest.fixture
async def make_user_orm(
    async_session: AsyncSession,
) -> Callable[[UUID | None, str, str, str], Awaitable[UserORM]]:
    async def _make_user_orm(
        username: str = 'testuser',
        email: str = 'test@example.com',
        password_hash: str = 'hashed_password',
        created_at: datetime | None = None,
        id: UUID | None = None,
    ) -> UserORM:
        user = UserORM(
            id=id,
            username=username,
            email=email,
            password_hash=password_hash,
            created_at=created_at,
        )
        async_session.add(user)
        await async_session.commit()
        await async_session.refresh(user)
        return user

    return _make_user_orm
