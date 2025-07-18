from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.api.dependencies.database import get_db_session
from src.adapters.api.schemas.user import UserCreate, UserResponse
from src.domain.errors.domain_exceptions import UserAlreadyExistsError
from src.factories.create_user_factory import create_user_factory

router = APIRouter(prefix='/users', tags=['users'])


@router.post(
    '/',
    response_model=UserResponse,
    status_code=HTTPStatus.CREATED,
    responses={
        HTTPStatus.CREATED: {'description': 'User created successfully'},
        HTTPStatus.CONFLICT: {'description': 'User already exists'},
        HTTPStatus.INTERNAL_SERVER_ERROR: {
            'description': 'Internal server error',
        },
        HTTPStatus.BAD_REQUEST: {'description': 'Bad request'},
    },
)
async def create_user(
    user: UserCreate,
    session: AsyncSession = Depends(get_db_session),
):
    try:
        create_user = create_user_factory(session)

        user = await create_user.execute(
            user.username,
            user.email,
            user.password,
        )

        return UserResponse.model_validate(user)
    except UserAlreadyExistsError as e:
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
