from unittest.mock import AsyncMock, patch
from uuid import uuid4

import pytest
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from src.infrastructure.database.sqlite_db import (
    AsyncSessionLocal,
    Base,
    UserORM,
    close_db,
    get_db,
    init_db,
)


def test_user_orm_creation():
    user_id = uuid4()

    user = UserORM(
        id=user_id,
        username='testuser',
        email='test@example.com',
        password_hash='hashed_password',
    )

    assert user.id == user_id
    assert user.username == 'testuser'
    assert user.email == 'test@example.com'
    assert user.password_hash == 'hashed_password'


@pytest.mark.asyncio
async def test_user_orm_default_timestamps(make_user_orm):
    user = await make_user_orm(
        username='testuser',
        email='test@example.com',
        password_hash='hashed_password',
    )
    assert user.created_at is not None
    assert user.updated_at is not None


@pytest.mark.asyncio
async def test_user_orm_table_name(make_user_orm):
    await make_user_orm(
        username='testuser',
        email='test@example.com',
        password_hash='hashed_password',
    )
    assert UserORM.__tablename__ == 'users'


@pytest.mark.asyncio
async def test_user_orm_columns_exist(make_user_orm):
    await make_user_orm(
        username='testuser',
        email='test@example.com',
        password_hash='hashed_password',
    )
    columns = UserORM.__table__.columns
    for column in [
        'id',
        'username',
        'email',
        'password_hash',
        'created_at',
        'updated_at',
    ]:
        assert column in columns


@pytest.mark.asyncio
async def test_user_orm_id_is_uuid(make_user_orm):
    await make_user_orm(
        username='testuser',
        email='test@example.com',
        password_hash='hashed_password',
    )
    id_column = UserORM.__table__.columns['id']
    assert 'UUID' in str(id_column.type)


@pytest.mark.asyncio
async def test_user_orm_string_columns_length(make_user_orm):
    await make_user_orm(
        username='testuser',
        email='test@example.com',
        password_hash='hashed_password',
    )

    expected_results = {
        'username': 50,
        'email': None,
        'password_hash': None,
    }

    for column, length in expected_results.items():
        assert UserORM.__table__.columns[column].type.length == length


# --------------------
# Funções auxiliares do banco
# --------------------


@pytest.mark.asyncio
@patch('src.infrastructure.database.sqlite_db.engine')
async def test_init_db(mock_engine, make_user_orm):
    await make_user_orm(
        username='testuser',
        email='test@example.com',
        password_hash='hashed_password',
    )
    mock_conn = AsyncMock()
    mock_engine.begin.return_value.__aenter__.return_value = mock_conn

    await init_db()

    mock_engine.begin.assert_called_once()
    mock_conn.run_sync.assert_called_once_with(Base.metadata.create_all)


@patch('src.infrastructure.database.sqlite_db.AsyncSessionLocal')
async def test_get_db(mock_session_local, make_user_orm):
    await make_user_orm(
        username='testuser',
        email='test@example.com',
        password_hash='hashed_password',
    )
    mock_session = AsyncMock()
    mock_session_local.return_value.__aenter__.return_value = mock_session

    db_gen = get_db()
    session = await anext(db_gen)

    assert session == mock_session
    mock_session_local.assert_called_once()


@patch('src.infrastructure.database.sqlite_db.engine')
async def test_close_db(mock_engine, make_user_orm):
    mock_engine.dispose = AsyncMock()
    await make_user_orm(
        username='testuser',
        email='test@example.com',
        password_hash='hashed_password',
    )
    await close_db()
    mock_engine.dispose.assert_called_once()


@pytest.mark.asyncio
async def test_async_session_local_configuration():
    async with AsyncSessionLocal() as session:
        assert isinstance(session, AsyncSession)


def test_base_class_inheritance():
    assert issubclass(Base, DeclarativeBase)


@pytest.mark.asyncio
async def test_user_orm_database_operations(
    async_session: AsyncSession,
    make_user_orm,
):
    user = await make_user_orm(
        username='testuser',
        email='test@example.com',
        password_hash='hashed_password',
    )
    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    stmt = select(UserORM).where(UserORM.username == 'testuser')
    result = await async_session.execute(stmt)
    fetched = result.scalar_one()

    assert fetched.id == user.id
    assert fetched.email == 'test@example.com'


@pytest.mark.asyncio
async def test_user_orm_unique_constraints(async_session, make_user_orm):
    await make_user_orm(
        username='testuser',
        email='test@example.com',
        password_hash='hashed_password',
    )

    with pytest.raises(IntegrityError):
        await make_user_orm(
            username='testuser',
            email='other@example.com',
            password_hash='hashed_password',
        )


@pytest.mark.asyncio
async def test_user_orm_timestamps_auto_update(
    async_session: AsyncSession,
    make_user_orm,
):
    user = await make_user_orm(
        username='testuser',
        email='test@example.com',
        password_hash='hashed_password',
    )

    created_at = user.created_at
    updated_at = user.updated_at

    async_session.add(user)
    await async_session.commit()
    await async_session.refresh(user)

    assert user.created_at == created_at
    assert user.updated_at == updated_at
