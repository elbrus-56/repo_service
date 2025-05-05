from src.database.repositories import BaseRepo
from src.endpoints.update_event.models import Order


class UpdateEventUseCase:

    def __init__(self, repository: BaseRepo):
        """Инициализирует UseCase с репозиторием."""
        self.repository = repository

    async def execute(
        self,
        data: Order,
    ):
        """Функция обновляет запись из базы"""

        try:
            await self.repository.update(
                target="orders",
                filter={"order_id": data.order_id},
                data=data.model_dump(by_alias=True)
            )
            return True
        except Exception as exc:
            print(exc)
            return None
