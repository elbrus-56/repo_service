from src.database.repositories import BaseRepo


class AddEventUseCase:

    def __init__(self, repository: BaseRepo):
        """Инициализирует UseCase с репозиторием."""
        self.repository = repository

    async def execute(self, command: dict):
        return True
