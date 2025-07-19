from http import HTTPStatus
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.api.dependencies.database import get_db_session
from src.adapters.api.schemas.user import UserResponse, UserUpdate
from src.domain.errors.domain_exceptions import (
    UserAlreadyExistsError,
    UserNotFoundError,
)
from src.factories.update_user_factory import update_user_factory

router = APIRouter(prefix='/users', tags=['users'])


@router.put(
    '/{user_id}',
    response_model=UserResponse,
    status_code=HTTPStatus.OK,
    responses={
        HTTPStatus.OK: {'description': 'User updated successfully'},
        HTTPStatus.NOT_FOUND: {'description': 'User not found'},
        HTTPStatus.INTERNAL_SERVER_ERROR: {
            'description': 'Internal server error',
        },
        HTTPStatus.BAD_REQUEST: {'description': 'Bad request'},
    },
)
async def update_user(
    user_id: UUID,
    user: UserUpdate,
    session: AsyncSession = Depends(get_db_session),
):
    try:
        update_user = update_user_factory(session)

        user = await update_user.execute(
            user_id,
            user.username,
            user.email,
        )

        return UserResponse.model_validate(user)
    except UserNotFoundError as e:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=str(e))
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
