from typing import Literal

from src.database.repositories import BaseRepo


class DelEventUseCase:

    def __init__(self, repository: BaseRepo):
        """Инициализирует UseCase с репозиторием."""
        self.repository = repository

    async def execute(
        self,
        params: dict = {},
    ) -> Literal[True] | None:
        """Функция удаляет запись из базы"""
        where_clause = "order_id = %(order_id)s;"
        try:
            return await self.repository.delete(
                target="events.orders",
                where_clause=where_clause,
                params=params,
            )
        except Exception as exc:
            print(exc)
            return None
