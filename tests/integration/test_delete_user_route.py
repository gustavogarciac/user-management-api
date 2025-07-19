from http import HTTPStatus
from unittest.mock import patch
from uuid import uuid4

import pytest


@pytest.mark.asyncio
async def test_delete_user_success(async_session, client, make_user_api):
    user = await make_user_api(
        username='testuser',
        email='testuser@example.com',
        password_hash='testpassword',
    )

    response = client.delete(f'/api/v1/users/{user.id}')

    assert response.status_code == HTTPStatus.OK
    assert response.json()['description'] == 'User deleted successfully'


@pytest.mark.asyncio
async def test_delete_user_not_found(
    async_session,
    client,
    make_user_api,
):
    random_id = uuid4()
    response = client.delete(f'/api/v1/users/{random_id}')

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json()['detail'] == f'User with id {random_id} not found'


@pytest.mark.asyncio
async def test_get_user_internal_server_error(
    async_session,
    client,
    make_user_api,
):
    random_id = uuid4()

    with patch(
        'src.adapters.api.routers.delete_user.delete_user_factory',
    ) as mock_factory:
        mock_use_case = mock_factory.return_value
        mock_use_case.execute.side_effect = Exception(
            'Database connection failed',
        )

        response = client.delete(f'/api/v1/users/{random_id}')

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert response.json()['detail'] == 'Database connection failed'
