from datetime import datetime, timedelta, timezone
from typing import Optional
from src.domain.ports.auth_service import AuthService
from jose import jwt, JWTError
from src.infrastructure.config.settings import settings

class JWTAuthenticationService(AuthService):
    def __init__(self):
        self.secret_key = settings.JWT_SECRET_KEY
        self.algorithm = "HS256"
        self.token_expiracy_minutes = settings.JWT_EXPIRATION_MINUTES
    
    async def authenticate(self, email: str, password: str) -> str:
        payload = {
            "sub": email,
            "exp": (
                datetime.now(timezone.utc) 
                + timedelta(minutes=self.token_expiracy_minutes)
            ),
        }

        return jwt.encode(
            payload,
            self.secret_key,
            algorithm=self.algorithm,
        )
    
    async def verify_token(self, token: str) -> Optional[str]:
        try:
            payload = jwt.decode(
                token,
                self.secret_key,
                algorithms=[self.algorithm],
            )

            return payload.get('sub')
        except JWTError:
            return None
