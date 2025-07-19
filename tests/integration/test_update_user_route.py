from http import HTTPStatus
from unittest.mock import patch
from uuid import uuid4

import pytest


@pytest.mark.asyncio
async def test_update_user_success(
    async_session,
    client,
    make_user_api,
    make_token_api,
):
    user = await make_user_api(
        username='testuser',
        email='testuser@example.com',
        password_hash='testpassword',
    )

    token = make_token_api('testuser@example.com', 'testpassword')

    user_data = {
        'username': 'testuser2',
        'email': 'testuser2@example.com',
    }

    response = client.put(
        f'/api/v1/users/{user.id}',
        json=user_data,
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['username'] == user_data['username']
    assert response.json()['email'] == user_data['email']

    assert 'id' in response.json()
    assert 'created_at' in response.json()
    assert 'updated_at' in response.json()


@pytest.mark.asyncio
async def test_update_user_not_found(
    async_session,
    client,
    make_user_api,
    make_token_api,
):
    await make_user_api(
        username='testuser',
        email='testuser@example.com',
        password_hash='testpassword',
    )

    token = make_token_api('testuser@example.com', 'testpassword')

    random_id = uuid4()
    user_data = {
        'username': 'testuser2',
        'email': 'testuser2@example.com',
    }

    response = client.put(
        f'/api/v1/users/{random_id}',
        json=user_data,
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == f'User with id {random_id} not found'


@pytest.mark.asyncio
async def test_update_user_duplicate_email(
    async_session,
    client,
    make_user_api,
    make_token_api,
):
    user = await make_user_api(
        username='testuser',
        email='testuser@example.com',
        password_hash='testpassword',
    )

    await make_user_api(
        username='testuser2',
        email='testuser2@example.com',
        password_hash='testpassword2',
    )

    token = make_token_api('testuser@example.com', 'testpassword')

    user_data = {
        'username': 'testuser3',
        'email': 'testuser2@example.com',
    }

    response = client.put(
        f'/api/v1/users/{user.id}',
        json=user_data,
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()['detail'] == (
        'User with email testuser2@example.com already exists'
    )


@pytest.mark.asyncio
async def test_update_user_duplicate_username(
    async_session,
    client,
    make_user_api,
    make_token_api,
):
    user = await make_user_api(
        username='testuser',
        email='testuser@example.com',
        password_hash='testpassword',
    )

    token = make_token_api('testuser@example.com', 'testpassword')

    await make_user_api(
        username='testuser2',
        email='testuser2@example.com',
        password_hash='testpassword2',
    )

    user_data = {
        'username': 'testuser2',
        'email': 'testuser@example.com',
    }

    response = client.put(
        f'/api/v1/users/{user.id}',
        json=user_data,
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json()['detail'] == (
        'User with username testuser2 already exists'
    )


@pytest.mark.asyncio
async def test_update_user_internal_server_error(
    async_session,
    client,
    make_user_api,
    make_token_api,
):
    await make_user_api(
        username='testuser',
        email='testuser@example.com',
        password_hash='testpassword',
    )

    token = make_token_api('testuser@example.com', 'testpassword')

    random_id = uuid4()
    user_data = {
        'username': 'testuser2',
        'email': 'testuser2@example.com',
    }

    with patch(
        'src.adapters.api.routers.update_user.update_user_factory',
    ) as mock_factory:
        mock_use_case = mock_factory.return_value
        mock_use_case.execute.side_effect = Exception(
            'Database connection failed',
        )

        response = client.put(
            f'/api/v1/users/{random_id}',
            json=user_data,
            headers={'Authorization': f'Bearer {token}'},
        )

    assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
    assert response.json()['detail'] == 'Database connection failed'
