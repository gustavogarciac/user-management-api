from http import HTTPStatus
from unittest.mock import patch

import pytest


@pytest.mark.asyncio
async def test_create_user_success(async_session, client):
    user_data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword',
    }

    response = client.post('/api/v1/users', json=user_data)

    # Debug: print response details
    print(f'Response status: {response.status_code}')
    print(f'Response body: {response.json()}')

    assert response.status_code == HTTPStatus.CREATED
    assert response.json()['username'] == user_data['username']
    assert response.json()['email'] == user_data['email']
    assert 'id' in response.json()
    assert 'created_at' in response.json()
    assert 'updated_at' in response.json()
    assert 'password_hash' not in response.json()


@pytest.mark.asyncio
async def test_create_user_duplicate_email(
    async_session,
    client,
    make_user_api,
):
    await make_user_api(
        username='testuser',
        email='testuser@example.com',
        password_hash='testpassword',
    )

    duplicate_user_data = {
        'username': 'testuser2',
        'email': 'testuser@example.com',
        'password': 'testpassword2',
    }

    response = client.post('/api/v1/users', json=duplicate_user_data)

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()['detail'] == (
        'User with email testuser@example.com already exists'
    )


@pytest.mark.asyncio
async def test_create_user_duplicate_username(
    async_session,
    client,
    make_user_api,
):
    await make_user_api(
        username='testuser',
        email='testuser@example.com',
        password_hash='testpassword',
    )

    duplicate_user_data = {
        'username': 'testuser',
        'email': 'testuser2@example.com',
        'password': 'testpassword2',
    }

    response = client.post('/api/v1/users', json=duplicate_user_data)

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()['detail'] == (
        'User with username testuser already exists'
    )


@pytest.mark.asyncio
async def test_create_user_internal_server_error(
    async_session,
    client,
):
    user_data = {
        'username': 'testuser',
        'email': 'testuser@example.com',
        'password': 'testpassword',
    }

    with patch(
        'src.adapters.api.routers.create_user.create_user_factory',
    ) as mock_factory:
        mock_use_case = mock_factory.return_value
        mock_use_case.execute.side_effect = Exception(
            'Database connection failed',
        )

        response = client.post('/api/v1/users', json=user_data)

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json()['detail'] == 'Database connection failed'
