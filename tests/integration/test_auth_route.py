from http import HTTPStatus
from unittest.mock import patch

import pytest


@pytest.mark.asyncio
async def test_authenticate_user_success(async_session, client, make_user_api):
    await make_user_api(
        username='testuser',
        email='testuser@example.com',
        password_hash='testpassword123',
    )

    response = client.post(
        '/api/v1/auth/token',
        json={
            'email': 'testuser@example.com',
            'password': 'testpassword123',
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    data = response.json()
    assert 'access_token' in data
    assert 'token_type' in data
    assert data['token_type'] == 'bearer'


@pytest.mark.asyncio
async def test_authenticate_user_invalid_credentials(
    async_session,
    client,
    make_user_api,
):
    await make_user_api(
        username='testuser',
        email='testuser@example.com',
        password_hash='testpassword123',
    )

    response = client.post(
        '/api/v1/auth/token',
        json={
            'email': 'testuser@example.com',
            'password': 'wrongpassword',
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()['detail'] == 'Invalid credentials'


@pytest.mark.asyncio
async def test_authenticate_user_user_not_found(
    async_session,
    client,
):
    response = client.post(
        '/api/v1/auth/token',
        json={
            'email': 'nonexistent@example.com',
            'password': 'testpassword123',
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()['detail'] == 'Invalid credentials'


@pytest.mark.asyncio
async def test_authenticate_user_invalid_email_format(
    async_session,
    client,
):
    response = client.post(
        '/api/v1/auth/token',
        json={
            'email': 'invalid-email',
            'password': 'testpassword123',
        },
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_authenticate_user_missing_email(
    async_session,
    client,
):
    response = client.post(
        '/api/v1/auth/token',
        json={
            'password': 'testpassword123',
        },
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_authenticate_user_missing_password(
    async_session,
    client,
):
    response = client.post(
        '/api/v1/auth/token',
        json={
            'email': 'testuser@example.com',
        },
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_authenticate_user_empty_request(
    async_session,
    client,
):
    response = client.post(
        '/api/v1/auth/token',
        json={},
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_authenticate_user_internal_server_error(
    async_session,
    client,
    make_user_api,
):
    await make_user_api(
        username='testuser',
        email='testuser@example.com',
        password_hash='testpassword123',
    )

    with patch(
        'src.adapters.api.routers.auth.authenticate_user_factory',
    ) as mock_factory:
        mock_use_case = mock_factory.return_value
        mock_use_case.execute.side_effect = Exception(
            'Database connection failed',
        )

        response = client.post(
            '/api/v1/auth/token',
            json={
                'email': 'testuser@example.com',
                'password': 'testpassword123',
            },
        )

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert response.json()['detail'] == 'Database connection failed'


@pytest.mark.asyncio
async def test_authenticate_user_with_empty_password(
    async_session,
    client,
    make_user_api,
):
    await make_user_api(
        username='testuser',
        email='testuser@example.com',
        password_hash='testpassword123',
    )

    response = client.post(
        '/api/v1/auth/token',
        json={
            'email': 'testuser@example.com',
            'password': '',
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()['detail'] == 'Invalid credentials'


@pytest.mark.asyncio
async def test_authenticate_user_with_empty_email(
    async_session,
    client,
    make_user_api,
):
    await make_user_api(
        username='testuser',
        email='testuser@example.com',
        password_hash='testpassword123',
    )

    response = client.post(
        '/api/v1/auth/token',
        json={
            'email': '',
            'password': 'testpassword123',
        },
    )

    assert response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_authenticate_user_case_sensitive_email(
    async_session,
    client,
    make_user_api,
):
    await make_user_api(
        username='testuser',
        email='testuser@example.com',
        password_hash='testpassword123',
    )

    response = client.post(
        '/api/v1/auth/token',
        json={
            'email': 'TESTUSER@EXAMPLE.COM',
            'password': 'testpassword123',
        },
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json()['detail'] == 'Invalid credentials'
