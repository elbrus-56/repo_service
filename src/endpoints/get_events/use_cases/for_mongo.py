from src.database.repositories import BaseRepo
from src.endpoints.get_events.models import Order


class GetEventsUseCase:

    def __init__(self, repository: BaseRepo):
        """Инициализирует UseCase с репозиторием."""
        self.repository = repository

    async def execute(self, limit: int, offset: int) -> list[Order]:
        """Функция получает список записей из базы"""
        return [
            Order(**order)
            for order in await self.repository.get(
                target="orders",
                limit=limit,
                offset=offset,
            )
        ]
