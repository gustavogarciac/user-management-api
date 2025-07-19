from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.adapters.api.dependencies.database import get_db_session
from src.adapters.api.schemas.user import (
    UserListQueryParams,
    UserListResponse,
    UserResponse,
)
from src.application.use_cases.list_users import ListUsersRequest
from src.domain.errors.domain_exceptions import (
    InvalidFilterError,
    InvalidOrderByError,
    InvalidOrderDirectionError,
    InvalidPageError,
    InvalidPageSizeError,
)
from src.factories.list_users_factory import list_users_factory

router = APIRouter(prefix='/users', tags=['users'])


@router.get(
    '/',
    status_code=HTTPStatus.OK,
    response_model=UserListResponse,
    responses={
        HTTPStatus.OK: {'description': 'Users retrieved successfully'},
        HTTPStatus.BAD_REQUEST: {'description': 'Invalid parameters'},
        HTTPStatus.INTERNAL_SERVER_ERROR: {
            'description': 'Internal server error',
        },
    },
)
async def list_users(
    session: AsyncSession = Depends(get_db_session),
    params: UserListQueryParams = Depends(),
):
    try:
        list_users = list_users_factory(session)

        # Convert individual filter parameters to a dictionary
        filters = {}
        if params.username:
            filters['username'] = params.username
        if params.email:
            filters['email'] = params.email

        list_users_request = ListUsersRequest(
            page=params.page,
            page_size=params.page_size,
            query=params.query,
            order_by=params.order_by,
            order_direction=params.order_direction,
            filters=filters if filters else None,
        )

        response = await list_users.execute(list_users_request)

        return UserListResponse(
            items=[
                UserResponse.model_validate(user) for user in response['items']
            ],
            total_items=response['total_items'],
            page=response['page'],
            page_size=response['page_size'],
        )
    except InvalidPageSizeError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))
    except InvalidOrderDirectionError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))
    except InvalidPageError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))
    except InvalidFilterError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))
    except InvalidOrderByError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail=str(e),
        )
