from typing import Literal

from loguru import logger

from src.database.repositories import BaseRepo
from src.endpoints.get_events.models import Order


class GetEventsUseCase:

    def __init__(self, repository: BaseRepo):
        """Инициализирует UseCase с репозиторием."""
        self.repository = repository

    async def execute(
        self,
        limit: int,
        offset: int,
        order_by: str | None,
        sort: Literal[1, -1],
    ) -> list[Order]:
        """Функция получает список записей из базы"""
        try:
            orders = await self.repository.get(
                target="orders",
                limit=limit,
                offset=offset,
                order_by=order_by,
                sort=sort,
            )
            return [Order(**order) for order in orders]
        except Exception as exc:
            logger.error(exc)
            return []
