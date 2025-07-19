from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.api.dependencies.auth import get_current_user
from src.adapters.api.dependencies.database import get_db_session
from src.domain.errors.domain_exceptions import UserNotFoundError
from src.factories.delete_user_factory import delete_user_factory

router = APIRouter(prefix='/users', tags=['users'])


@router.delete(
    '/{user_id}',
    status_code=HTTPStatus.OK,
    responses={
        HTTPStatus.OK: {'description': 'User deleted successfully'},
        HTTPStatus.NOT_FOUND: {'description': 'User not found'},
        HTTPStatus.UNAUTHORIZED: {'description': 'Not authenticated'},
        HTTPStatus.INTERNAL_SERVER_ERROR: {
            'description': 'Internal server error',
        },
    },
)
async def delete_user(
    user_id: UUID,
    session: AsyncSession = Depends(get_db_session),
    current_user: str = Depends(get_current_user),
):
    try:
        delete_user = delete_user_factory(session)

        await delete_user.execute(user_id)

        return {'description': 'User deleted successfully'}
    except UserNotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
