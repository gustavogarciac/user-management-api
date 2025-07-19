from http import HTTPStatus
from unittest.mock import patch
from uuid import uuid4

import pytest


@pytest.mark.asyncio
async def test_get_user_success(
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

    response = client.get(
        f'/api/v1/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json()['username'] == 'testuser'
    assert response.json()['email'] == 'testuser@example.com'

    assert 'id' in response.json()
    assert 'created_at' in response.json()
    assert 'updated_at' in response.json()


@pytest.mark.asyncio
async def test_get_user_not_found(
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

    random_id = uuid4()

    token = make_token_api('testuser@example.com', 'testpassword')

    response = client.get(
        f'/api/v1/users/{random_id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == f'User with id {random_id} not found'


@pytest.mark.asyncio
async def test_get_user_internal_server_error(
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

    random_id = uuid4()

    token = make_token_api('testuser@example.com', 'testpassword')

    with patch(
        'src.adapters.api.routers.get_user.get_user_factory',
    ) as mock_factory:
        mock_use_case = mock_factory.return_value
        mock_use_case.execute.side_effect = Exception(
            'Database connection failed',
        )

        response = client.get(
            f'/api/v1/users/{random_id}',
            headers={'Authorization': f'Bearer {token}'},
        )

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert response.json()['detail'] == 'Database connection failed'
