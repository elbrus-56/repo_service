from src.database.repositories import BaseRepo
from src.endpoints.add_event.models import Order


class AddEventUseCase:

    def __init__(self, repository: BaseRepo):
        """Инициализирует UseCase с репозиторием."""
        self.repository = repository

    async def execute(
        self,
    ) -> Order:
        """Функция генерирует и добавляет запись в базу"""
        order = Order()
        doc = await self.repository.post(
            target="orders",
            data=order.model_dump(),
        )
        return order
