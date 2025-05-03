from src.database.repositories import BaseRepo


class DelEventUseCase:

    def __init__(self, repository: BaseRepo):
        """Инициализирует UseCase с репозиторием."""
        self.repository = repository

    async def execute(
        self,
        filter: dict = {},
    ):
        """Функция удаляет запись из базы"""

        try:
            await self.repository.delete(
                target="orders",
                filter=filter,
            )
            return True
        except Exception as exc:
            print(exc)
            return None
