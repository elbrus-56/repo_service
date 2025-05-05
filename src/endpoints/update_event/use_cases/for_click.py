import datetime
from typing import Literal

from loguru import logger

from src.database.repositories import BaseRepo
from src.endpoints.update_event.models import Order


class UpdateEventUseCase:

    def __init__(self, repository: BaseRepo):
        """Инициализирует UseCase с репозиторием."""
        self.repository = repository

    async def execute(
        self,
        data: Order,
    ) -> Literal[True] | None:
        """Функция обновляет запись из базы"""
        data.updated_at = datetime.datetime.now()
        update_data = data.model_dump(exclude=("order_id",), by_alias=True)
        params = {"order_id": data.order_id}
        where_clause = "order_id = %(order_id)s;"
        try:
            return await self.repository.update(
                target="events.orders",
                update_data=update_data,
                where_clause=where_clause,
                params=params,
            )
        except Exception as exc:
            logger.error(exc)
            return None
