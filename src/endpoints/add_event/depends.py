from fastapi import Depends

from src.core.depends import get_click_repo, get_mongo_repo
from src.database.repositories import ClickHouseRepo, MongoRepo
from src.endpoints.add_event.use_cases.for_click import (
    AddEventUseCase as AddEventUseCaseClick,
)


async def add_event_use_case_with_click(
    repo: ClickHouseRepo = Depends(get_click_repo),
) -> AddEventUseCaseClick:
    return AddEventUseCaseClick(repo)
