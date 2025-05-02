from typing import Literal

from src.database.repositories import BaseRepo
from src.endpoints.get_events.models import Order


class GetEventsUseCase:

    def __init__(self, repository: BaseRepo):
        """Инициализирует UseCase с репозиторием."""
        self.repository = repository

    async def execute(
        self,
        limit: int,
        offset: int | None,
        order_by: str | None,
        sort: Literal["ASC", "DESC"],
    ) -> list[Order]:
        """Функция получает список записей из базы"""
        return [
            Order(**order)
            for order in await self.repository.get(
                target="events.orders",
                limit=limit,
                offset=offset,
                order_by=order_by,
                sort=sort,
            )
        ]
