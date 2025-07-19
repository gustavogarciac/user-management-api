from http import HTTPStatus
from typing import Optional

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from src.adapters.auth.jwt_auth_service import JWTAuthenticationService

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/api/v1/auth/token',
    auto_error=True,
)
oauth2_scheme_optional = OAuth2PasswordBearer(
    tokenUrl='/api/v1/auth/token',
    auto_error=False,
)


async def get_current_user(
    token: str = Depends(oauth2_scheme),
) -> str:
    auth_service = JWTAuthenticationService()
    email = await auth_service.validate_token(token)

    if email is None:
        raise HTTPException(
            status_code=HTTPStatus.UNAUTHORIZED,
            detail='Invalid credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    return email


async def get_current_user_optional(
    token: Optional[str] = Depends(oauth2_scheme_optional),
) -> Optional[str]:
    if token is None:
        return None

    auth_service = JWTAuthenticationService()
    email = await auth_service.validate_token(token)

    return email
