from dataclasses import dataclass

from src.domain.errors.domain_exceptions import (
    InvalidFilterError,
    InvalidOrderByError,
    InvalidOrderDirectionError,
    InvalidPageError,
    InvalidPageSizeError,
)
from src.domain.ports.user_repository import ListUsersConfig, UserRepository


@dataclass
class ListUsersRequest:
    page: int
    page_size: int
    query: str | None = None
    order_by: str | None = None
    order_direction: str | None = None
    filters: dict[str, str] | None = None


class ListUsersUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    MAXIMUM_PAGE_SIZE = 100
    ALLOWED_ORDER_BY = ['username', 'email', 'created_at']
    ALLOWED_ORDER_DIRECTION = ['asc', 'desc']
    ALLOWED_FILTERS = ['username', 'email']

    async def execute(self, request: ListUsersRequest) -> dict:
        self._validate_pagination(request.page, request.page_size)
        self._validate_order_direction(request.order_direction)
        self._validate_order_by(request.order_by)
        self._validate_filters(request.filters)

        config = ListUsersConfig(
            page=request.page,
            page_size=request.page_size,
            query=request.query,
            order_by=request.order_by,
            order_direction=request.order_direction,
            filters=request.filters,
        )

        users = await self.user_repository.list_users(config)
        total_items = await self.user_repository.count_users(config)

        return {
            'items': users,
            'total_items': total_items,
            'page': request.page,
            'page_size': request.page_size,
        }

    def _validate_pagination(self, page: int, page_size: int) -> None:
        if page <= 0:
            raise InvalidPageError('Page must be greater than 0')

        if page_size <= 0:
            raise InvalidPageSizeError('Page size must be greater than 0')

        if page_size > self.MAXIMUM_PAGE_SIZE:
            raise InvalidPageSizeError(
                f'Page size must be less than {self.MAXIMUM_PAGE_SIZE}'
            )

    def _validate_order_direction(self, order_direction: str | None) -> None:
        if (
            order_direction
            and order_direction not in self.ALLOWED_ORDER_DIRECTION
        ):
            allowed = self.ALLOWED_ORDER_DIRECTION
            raise InvalidOrderDirectionError(
                f'Order direction must be {allowed}'
            )

    def _validate_order_by(self, order_by: str | None) -> None:
        if order_by and order_by not in self.ALLOWED_ORDER_BY:
            raise InvalidOrderByError(
                f'Order by must be {self.ALLOWED_ORDER_BY}'
            )

    def _validate_filters(self, filters: dict[str, str] | None) -> None:
        if filters:
            for key, value in filters.items():
                if key not in self.ALLOWED_FILTERS:
                    raise InvalidFilterError(
                        f'Filter must be {self.ALLOWED_FILTERS}'
                    )
