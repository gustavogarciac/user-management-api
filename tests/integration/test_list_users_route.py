from http import HTTPStatus
from unittest.mock import patch

import pytest


@pytest.fixture
async def make_users(make_user_api):
    async def _make_users(count: int):
        for i in range(count):
            await make_user_api(
                username=f'testuser{i}',
                email=f'testuser{i}@example.com',
                password_hash='testpassword',
            )

    return _make_users


@pytest.mark.asyncio
async def test_list_users_success(
    async_session,
    client,
    make_users,
    make_token_api,
):
    await make_users(3)

    token = make_token_api('testuser0@example.com', 'testpassword')

    response = client.get(
        '/api/v1/users?page=1&page_size=10',
        headers={'Authorization': f'Bearer {token}'},
    )

    expected_response = {
        'items': [
            {
                'id': 1,
                'username': 'testuser0',
                'email': 'testuser0@example.com',
            },
        ],
        'total_items': 3,
        'page': 1,
        'page_size': 10,
    }

    assert response.status_code == HTTPStatus.OK
    assert response.json()['page'] == expected_response['page']
    assert response.json()['page_size'] == expected_response['page_size']
    assert response.json()['total_items'] == expected_response['total_items']
    assert (
        response.json()['items'][0]['username']
        == (expected_response['items'][0]['username'])
    )
    assert (
        response.json()['items'][0]['email']
        == (expected_response['items'][0]['email'])
    )


@pytest.mark.asyncio
async def test_list_users_success_with_pagination(
    async_session,
    client,
    make_users,
    make_token_api,
):
    await make_users(11)

    token = make_token_api('testuser0@example.com', 'testpassword')

    response = client.get(
        '/api/v1/users?page=2&page_size=10',
        headers={'Authorization': f'Bearer {token}'},
    )

    expected_response = {
        'items': [
            {
                'id': 11,
                'username': 'testuser10',
                'email': 'testuser10@example.com',
            },
        ],
        'total_items': 1,
        'page': 2,
        'page_size': 10,
    }

    assert response.status_code == HTTPStatus.OK
    assert response.json()['page'] == expected_response['page']
    assert response.json()['page_size'] == expected_response['page_size']
    assert response.json()['total_items'] == expected_response['total_items']
    assert (
        response.json()['items'][0]['username']
        == (expected_response['items'][0]['username'])
    )
    assert (
        response.json()['items'][0]['email']
        == (expected_response['items'][0]['email'])
    )


@pytest.mark.asyncio
async def test_list_users_invalid_page_size(
    async_session,
    client,
    make_users,
    make_token_api,
):
    await make_users(3)

    token = make_token_api('testuser0@example.com', 'testpassword')

    response = client.get(
        '/api/v1/users?page=1&page_size=0',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Page size must be greater than 0'


@pytest.mark.asyncio
async def test_list_users_invalid_page(
    async_session,
    client,
    make_users,
    make_token_api,
):
    await make_users(3)

    token = make_token_api('testuser0@example.com', 'testpassword')

    response = client.get(
        '/api/v1/users?page=0&page_size=10',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Page must be greater than 0'


@pytest.mark.asyncio
async def test_list_users_invalid_order_by(
    async_session,
    client,
    make_users,
    make_token_api,
):
    await make_users(3)

    token = make_token_api('testuser0@example.com', 'testpassword')

    response = client.get(
        '/api/v1/users?page=1&page_size=10&order_by=invalid',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == (
        "Order by must be ['username', 'email', 'created_at']"
    )


@pytest.mark.asyncio
async def test_list_users_invalid_order_direction(
    async_session,
    client,
    make_users,
    make_token_api,
):
    await make_users(3)

    token = make_token_api('testuser0@example.com', 'testpassword')

    response = client.get(
        '/api/v1/users?page=1&page_size=10&order_direction=invalid',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == (
        "Order direction must be ['asc', 'desc']"
    )


@pytest.mark.asyncio
async def test_list_users_internal_server_error(
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

    with patch(
        'src.adapters.api.routers.list_users.list_users_factory',
    ) as mock_factory:
        mock_use_case = mock_factory.return_value
        mock_use_case.execute.side_effect = Exception(
            'Database connection failed',
        )

        response = client.get(
            '/api/v1/users?page=1&page_size=10',
            headers={'Authorization': f'Bearer {token}'},
        )

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert response.json()['detail'] == 'Database connection failed'


@pytest.mark.asyncio
async def test_list_users_with_username_filter(
    async_session,
    client,
    make_users,
    make_token_api,
):
    await make_users(5)

    token = make_token_api('testuser0@example.com', 'testpassword')

    response = client.get(
        '/api/v1/users?page=1&page_size=10&username=testuser2',
        headers={'Authorization': f'Bearer {token}'},
    )

    expected_length = 1

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data['items']) == expected_length
    assert data['items'][0]['username'] == 'testuser2'


@pytest.mark.asyncio
async def test_list_users_with_email_filter(
    async_session,
    client,
    make_users,
    make_token_api,
):
    await make_users(5)

    token = make_token_api('testuser0@example.com', 'testpassword')

    response = client.get(
        '/api/v1/users?page=1&page_size=10&email=testuser3@example.com',
        headers={'Authorization': f'Bearer {token}'},
    )

    expected_length = 1

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data['items']) == expected_length
    assert data['items'][0]['email'] == 'testuser3@example.com'


@pytest.mark.asyncio
async def test_list_users_with_multiple_filters(
    async_session,
    client,
    make_users,
    make_token_api,
):
    await make_users(5)

    token = make_token_api('testuser0@example.com', 'testpassword')

    response = client.get(
        '/api/v1/users?page=1&page_size=10&username=testuser1&email=testuser1@example.com',
        headers={'Authorization': f'Bearer {token}'},
    )

    expected_length = 1

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data['items']) == expected_length
    assert data['items'][0]['username'] == 'testuser1'
    assert data['items'][0]['email'] == 'testuser1@example.com'


@pytest.mark.asyncio
async def test_list_users_with_query_search(
    async_session,
    client,
    make_users,
    make_token_api,
):
    await make_users(5)

    token = make_token_api('testuser0@example.com', 'testpassword')

    response = client.get(
        '/api/v1/users?page=1&page_size=10&query=testuser2',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data['items']) >= 1
    found = any(
        'testuser2' in item['username'] or 'testuser2' in item['email']
        for item in data['items']
    )
    assert found


@pytest.mark.asyncio
async def test_list_users_with_empty_query(
    async_session,
    client,
    make_users,
    make_token_api,
):
    await make_users(3)

    token = make_token_api('testuser0@example.com', 'testpassword')

    response = client.get(
        '/api/v1/users?page=1&page_size=10&query=',
        headers={'Authorization': f'Bearer {token}'},
    )

    expected_length = 3

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data['items']) == expected_length


@pytest.mark.asyncio
async def test_list_users_with_query_no_results(
    async_session,
    client,
    make_users,
    make_token_api,
):
    await make_users(3)

    token = make_token_api('testuser0@example.com', 'testpassword')

    response = client.get(
        '/api/v1/users?page=1&page_size=10&query=nonexistent',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data['items']) == 0
    assert data['total_items'] == 0


@pytest.mark.asyncio
async def test_list_users_ordered_by_username_asc(
    async_session,
    client,
    make_users,
    make_token_api,
):
    await make_users(3)

    token = make_token_api('testuser0@example.com', 'testpassword')

    response = client.get(
        '/api/v1/users?page=1&page_size=10&order_by=username&order_direction=asc',
        headers={'Authorization': f'Bearer {token}'},
    )

    expected_length = 3

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data['items']) == expected_length
    usernames = [item['username'] for item in data['items']]
    assert usernames == sorted(usernames)


@pytest.mark.asyncio
async def test_list_users_ordered_by_username_desc(
    async_session,
    client,
    make_users,
    make_token_api,
):
    await make_users(3)

    token = make_token_api('testuser0@example.com', 'testpassword')

    response = client.get(
        '/api/v1/users?page=1&page_size=10&order_by=username&order_direction=desc',
        headers={'Authorization': f'Bearer {token}'},
    )

    expected_length = 3

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data['items']) == expected_length
    usernames = [item['username'] for item in data['items']]
    assert usernames == sorted(usernames, reverse=True)


@pytest.mark.asyncio
async def test_list_users_ordered_by_email_asc(
    async_session,
    client,
    make_users,
    make_token_api,
):
    await make_users(3)

    token = make_token_api('testuser0@example.com', 'testpassword')

    response = client.get(
        '/api/v1/users?page=1&page_size=10&order_by=email&order_direction=asc',
        headers={'Authorization': f'Bearer {token}'},
    )

    expected_length = 3

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data['items']) == expected_length
    emails = [item['email'] for item in data['items']]
    assert emails == sorted(emails)


@pytest.mark.asyncio
async def test_list_users_ordered_by_email_desc(
    async_session,
    client,
    make_users,
    make_token_api,
):
    await make_users(3)

    token = make_token_api('testuser0@example.com', 'testpassword')

    response = client.get(
        '/api/v1/users?page=1&page_size=10&order_by=email&order_direction=desc',
        headers={'Authorization': f'Bearer {token}'},
    )

    expected_length = 3

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data['items']) == expected_length
    emails = [item['email'] for item in data['items']]
    assert emails == sorted(emails, reverse=True)


@pytest.mark.asyncio
async def test_list_users_ordered_by_created_at_asc(
    async_session,
    client,
    make_users,
    make_token_api,
):
    await make_users(3)

    token = make_token_api('testuser0@example.com', 'testpassword')

    response = client.get(
        '/api/v1/users?page=1&page_size=10&order_by=created_at&order_direction=asc',
        headers={'Authorization': f'Bearer {token}'},
    )

    expected_length = 3

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data['items']) == expected_length


@pytest.mark.asyncio
async def test_list_users_ordered_by_created_at_desc(
    async_session,
    client,
    make_users,
    make_token_api,
):
    await make_users(3)

    token = make_token_api('testuser0@example.com', 'testpassword')

    response = client.get(
        '/api/v1/users?page=1&page_size=10&order_by=created_at&order_direction=desc',
        headers={'Authorization': f'Bearer {token}'},
    )

    expected_length = 3

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data['items']) == expected_length


@pytest.mark.asyncio
async def test_list_users_page_size_exceeds_maximum(
    async_session,
    client,
    make_users,
    make_token_api,
):
    await make_users(3)

    token = make_token_api('testuser0@example.com', 'testpassword')

    response = client.get(
        '/api/v1/users?page=1&page_size=101',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json()['detail'] == 'Page size must be less than 100'


@pytest.mark.asyncio
async def test_list_users_empty_list(
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

    delete_user = client.delete(
        f'/api/v1/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert delete_user.status_code == HTTPStatus.OK

    response = client.get(
        '/api/v1/users?page=1&page_size=10',
        headers={'Authorization': f'Bearer {token}'},
    )

    expected_response = {
        'items': [],
        'total_items': 0,
        'page': 1,
        'page_size': 10,
    }

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data['items']) == len(expected_response['items'])
    assert data['total_items'] == expected_response['total_items']
    assert data['page'] == expected_response['page']
    assert data['page_size'] == expected_response['page_size']


@pytest.mark.asyncio
async def test_list_users_with_default_parameters(
    async_session,
    client,
    make_users,
    make_token_api,
):
    await make_users(3)

    token = make_token_api('testuser0@example.com', 'testpassword')

    response = client.get(
        '/api/v1/users',
        headers={'Authorization': f'Bearer {token}'},
    )

    expected_response = {
        'items': [
            {
                'id': 1,
                'username': 'testuser0',
                'email': 'testuser0@example.com',
            },
            {
                'id': 2,
                'username': 'testuser1',
                'email': 'testuser1@example.com',
            },
            {
                'id': 3,
                'username': 'testuser2',
                'email': 'testuser2@example.com',
            },
        ],
        'total_items': 3,
        'page': 1,
        'page_size': 10,
    }

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data['items']) == len(expected_response['items'])
    assert data['total_items'] == expected_response['total_items']
    assert data['page'] == expected_response['page']
    assert data['page_size'] == expected_response['page_size']


@pytest.mark.asyncio
async def test_list_users_pagination_exceeds_total(
    async_session,
    client,
    make_users,
    make_token_api,
):
    await make_users(5)

    token = make_token_api('testuser0@example.com', 'testpassword')

    response = client.get(
        '/api/v1/users?page=10&page_size=10',
        headers={'Authorization': f'Bearer {token}'},
    )

    expected_response = {
        'items': [],
        'total_items': 0,
        'page': 10,
        'page_size': 10,
    }

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data['items']) == len(expected_response['items'])
    assert data['total_items'] == expected_response['total_items']
    assert data['page'] == expected_response['page']
    assert data['page_size'] == expected_response['page_size']


@pytest.mark.asyncio
async def test_list_users_combined_filters_and_ordering(
    async_session,
    client,
    make_users,
    make_token_api,
):
    await make_users(5)

    token = make_token_api('testuser0@example.com', 'testpassword')

    query_params = {
        'page': 1,
        'page_size': 10,
        'username': 'testuser',
        'order_by': 'username',
        'order_direction': 'asc',
    }

    response = client.get(
        '/api/v1/users',
        params=query_params,
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    for item in data['items']:
        assert 'testuser' in item['username']


@pytest.mark.asyncio
async def test_list_users_combined_query_and_ordering(
    async_session,
    client,
    make_users,
    make_token_api,
):
    await make_users(5)

    token = make_token_api('testuser0@example.com', 'testpassword')

    response = client.get(
        '/api/v1/users?page=1&page_size=10&query=testuser&order_by=email&order_direction=desc',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    assert len(data['items']) >= 1


@pytest.mark.asyncio
async def test_list_users_combined_filters_query_and_ordering(
    async_session,
    client,
    make_users,
    make_token_api,
):
    await make_users(5)

    token = make_token_api('testuser0@example.com', 'testpassword')

    response = client.get(
        '/api/v1/users?page=1&page_size=10&username=testuser&query=testuser&order_by=username&order_direction=asc',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.OK
    data = response.json()
    for item in data['items']:
        assert 'testuser' in item['username']


@pytest.mark.asyncio
async def test_list_users_invalid_filter_error(
    async_session,
    client,
    make_users,
    make_token_api,
):
    await make_users(3)

    token = make_token_api('testuser0@example.com', 'testpassword')

    with patch(
        'src.adapters.api.routers.list_users.list_users_factory',
    ) as mock_factory:
        mock_use_case = mock_factory.return_value
        mock_use_case.execute.side_effect = Exception('Invalid filter')

        response = client.get(
            '/api/v1/users?page=1&page_size=10&invalid_filter=value',
            headers={'Authorization': f'Bearer {token}'},
        )

        assert response.status_code == HTTPStatus.INTERNAL_SERVER_ERROR
        assert response.json()['detail'] == 'Invalid filter'
