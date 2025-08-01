from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.api.dependencies.database import get_db_session
from src.adapters.api.schemas.token import TokenRequest, TokenResponse
from src.domain.errors.domain_exceptions import CredentialsError
from src.factories.authenticate_user_factory import authenticate_user_factory

router = APIRouter(prefix='/auth', tags=['auth'])


@router.post(
    '/token',
    response_model=TokenResponse,
    status_code=HTTPStatus.CREATED,
    responses={
        HTTPStatus.CREATED: {'description': 'Token created successfully'},
        HTTPStatus.UNAUTHORIZED: {'description': 'Invalid credentials'},
        HTTPStatus.UNPROCESSABLE_ENTITY: {'description': 'Validation error'},
        HTTPStatus.INTERNAL_SERVER_ERROR: {
            'description': 'Internal server error',
        },
    },
)
async def authenticate_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db_session),
):
    try:
        authenticate_user = authenticate_user_factory(session)

        token_request = TokenRequest(
            email=form_data.username,
            password=form_data.password,
        )

        token = await authenticate_user.execute(
            token_request.email,
            token_request.password,
        )

        return TokenResponse(
            access_token=token,
            token_type='bearer',
        )
    except ValidationError as e:
        raise HTTPException(
            status_code=HTTPStatus.UNPROCESSABLE_ENTITY,
            detail=str(e),
        )
    except CredentialsError as e:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
