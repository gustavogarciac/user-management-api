from datetime import datetime, timedelta, timezone
from unittest.mock import patch

import pytest
from jose import jwt

from src.adapters.auth.jwt_auth_service import JWTAuthenticationService


@pytest.fixture
def mock_datetime():
    fixed_time = datetime(2025, 1, 1, 12, 0, 0, tzinfo=timezone.utc)
    with patch('src.adapters.auth.jwt_auth_service.datetime') as mock_datetime:
        mock_datetime.datetime.now.return_value = fixed_time
        mock_datetime.timedelta = timedelta
        mock_datetime.timezone.utc = timezone.utc
        yield fixed_time


@pytest.fixture
def mock_settings():
    with patch(
        'src.adapters.auth.jwt_auth_service.settings',
        autospec=True,
    ) as mock_settings:
        mock_settings.JWT_SECRET_KEY = 'test_secret_key'
        mock_settings.JWT_EXPIRATION_MINUTES = 30
        yield mock_settings


@pytest.mark.asyncio
async def test_authenticate_success(mock_datetime, mock_settings):
    email = 'test@example.com'

    service = JWTAuthenticationService()

    token = await service.authenticate(email, 'password123')

    expected_exp = int(
        (
            mock_datetime + (timedelta(minutes=service.token_expiracy_minutes))
        ).timestamp(),
    )
    expected_payload = {
        'sub': email,
        'exp': expected_exp,
    }

    # Decode without expiration validation
    decoded_token = jwt.decode(
        token,
        mock_settings.JWT_SECRET_KEY,
        algorithms=[service.algorithm],
        options={'verify_exp': False},
    )

    assert decoded_token == expected_payload


@pytest.mark.asyncio
async def test_validate_token_success(mock_settings):
    service = JWTAuthenticationService()

    email = 'test@example.com'

    with patch.object(service, 'token_expiracy_minutes', 60 * 24 * 365):
        token = await service.authenticate(email, 'password123')

    result = await service.validate_token(token)

    assert result == email


@pytest.mark.asyncio
async def test_validate_token_invalid_token(mock_settings):
    service = JWTAuthenticationService()

    result = await service.validate_token('invalid_token')

    assert result is None


@pytest.mark.asyncio
async def test_validate_token_wrong_secret(mock_settings):
    service = JWTAuthenticationService()

    email = 'test@example.com'

    with patch.object(service, 'token_expiracy_minutes', 60 * 24 * 365):
        token = await service.authenticate(email, 'password123')

    with patch.object(service, 'secret_key', 'different_secret'):
        result = await service.validate_token(token)

    assert result is None
