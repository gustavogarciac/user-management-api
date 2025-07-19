from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.api.dependencies.auth import get_current_user
from src.adapters.api.dependencies.database import get_db_session
from src.adapters.api.schemas.user import UserResponse
from src.domain.errors.domain_exceptions import UserNotFoundError
from src.factories.get_user_factory import get_user_factory

router = APIRouter(prefix='/users', tags=['users'])


@router.get(
    '/{user_id}',
    response_model=UserResponse,
    status_code=HTTPStatus.OK,
    responses={
        HTTPStatus.OK: {'description': 'User retrieved successfully'},
        HTTPStatus.NOT_FOUND: {'description': 'User not found'},
        HTTPStatus.UNAUTHORIZED: {'description': 'Not authenticated'},
        HTTPStatus.INTERNAL_SERVER_ERROR: {
            'description': 'Internal server error',
        },
    },
)
async def get_user(
    user_id: UUID,
    session: AsyncSession = Depends(get_db_session),
    current_user: str = Depends(get_current_user),
):
    try:
        get_user = get_user_factory(session)

        user = await get_user.execute(user_id)

        return UserResponse.model_validate(user)
    except UserNotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
