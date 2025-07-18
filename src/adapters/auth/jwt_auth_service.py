import datetime
from typing import Optional

from jose import JWTError, jwt

from src.domain.ports.auth_service import AuthService
from src.infrastructure.config.settings import settings


class JWTAuthenticationService(AuthService):
    def __init__(self):
        self.secret_key = settings.JWT_SECRET_KEY
        self.algorithm = 'HS256'
        self.token_expiracy_minutes = settings.JWT_EXPIRATION_MINUTES

    async def authenticate(self, email: str, password: str) -> str:
        payload = {
            'sub': email,
            'exp': (
                datetime.datetime.now(datetime.timezone.utc)
                + datetime.timedelta(minutes=self.token_expiracy_minutes)
            ),
        }

        return jwt.encode(
            payload,
            self.secret_key,
            algorithm=self.algorithm,
        )

    async def validate_token(self, token: str) -> Optional[str]:
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
            )

            return payload.get('sub')
        except JWTError:
            return None
