from pydantic import BaseModel, EmailStr, Field


class TokenRequest(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str = Field(..., description='Token JWT de acesso')
    token_type: str = Field(default='bearer', description='Tipo do token')
