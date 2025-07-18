from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.infrastructure.database.sqlite_db import UserORM

# ---------------------------
# Banco e estrutura básica
# ---------------------------


@pytest.mark.asyncio
async def test_database_initialization(
    async_session: AsyncSession,
    make_user_orm,
):
    await make_user_orm(
        'testuser',
        'test@example.com',
        'hashed_password',
    )
    result = await async_session.execute(select(UserORM).limit(1))
    assert result is not None


# ---------------------------
# CRUD
# ---------------------------


@pytest.mark.asyncio
async def test_crud_user(async_session: AsyncSession, make_user_orm):
    user = await make_user_orm(
        'testuser',
        'test@example.com',
        'hashed_password',
    )
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    # Read
    stmt = select(UserORM).where(UserORM.id == user.id)
    result = await async_session.execute(stmt)
    fetched = result.scalar_one()
    assert fetched.username == 'testuser'

    # Update
    fetched.username = 'updateduser'
    fetched.email = 'updated@example.com'
    await async_session.commit()
    await async_session.refresh(fetched)
    assert fetched.username == 'updateduser'

    # Delete
    await async_session.delete(fetched)
    await async_session.commit()
    result = await async_session.execute(
        select(UserORM).where(UserORM.id == user.id),
    )
    assert result.scalar_one_or_none() is None


# ---------------------------
# Constraints
# ---------------------------


@pytest.mark.asyncio
async def test_unique_constraints(async_session, make_user_orm):
    await make_user_orm('uniqueuser', 'unique@example.com', 'hash1')

    with pytest.raises(IntegrityError):
        await make_user_orm('uniqueuser', 'other@example.com', 'hash2')


# ---------------------------
# Índices e buscas
# ---------------------------


@pytest.mark.asyncio
async def test_index_lookup(async_session: AsyncSession, make_user_orm):
    users = [
        await make_user_orm(f'user{i}', f'user{i}@example.com', f'hash{i}')
        for i in range(5)
    ]
    async_session.add_all(users)
    await async_session.commit()

    for i in [2, 3]:
        second_position = 2

        attr = 'username' if i == second_position else 'email'
        value = f'user{i}' if i == second_position else f'user{i}@example.com'

        stmt = select(UserORM).where(getattr(UserORM, attr) == value)
        result = await async_session.execute(stmt)
        user = result.scalar_one()

        assert user.username == f'user{i}'


# ---------------------------
# UUID
# ---------------------------


@pytest.mark.asyncio
async def test_uuid_primary_key(make_user_orm):
    user1 = await make_user_orm(
        username='uuiduser1',
        email='uuid1@example.com',
        password_hash='hash1',
    )
    assert isinstance(user1.id, uuid4().__class__)

    specific_id = uuid4()
    user2 = await make_user_orm(
        username='uuiduser2',
        email='uuid2@example.com',
        password_hash='hash2',
        id=specific_id,
    )
    assert user2.id == specific_id


# ---------------------------
# Sessão / transação
# ---------------------------


@pytest.mark.asyncio
async def test_session_rollback(async_session: AsyncSession, make_user_orm):
    user = UserORM(
        username='rollbackuser',
        email='rollback@example.com',
        password_hash='hash',
    )
    async_session.add(user)
    await async_session.rollback()

    result = await async_session.execute(
        select(UserORM).where(UserORM.username == 'rollbackuser'),
    )
    assert result.scalar_one_or_none() is None


# ---------------------------
# Concorrência
# ---------------------------


@pytest.mark.asyncio
async def test_concurrent_user_creation(async_session: AsyncSession):
    users = [
        UserORM(
            username=f'concurrent{i}',
            email=f'concurrent{i}@example.com',
            password_hash=f'hash{i}',
        )
        for i in range(10)
    ]
    async_session.add_all(users)
    await async_session.commit()

    for i, user in enumerate(users):
        await async_session.refresh(user)
        assert user.username == f'concurrent{i}'
