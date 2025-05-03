from fastapi import Depends

from src.core.depends import get_click_repo, get_mongo_repo
from src.database.repositories import ClickHouseRepo, MongoRepo
from src.endpoints.get_events.use_cases.for_click import (
    GetEventsUseCase as GetEventsUseCaseClick,
)
from src.endpoints.get_events.use_cases.for_mongo import (
    GetEventsUseCase as GetEventsUseCaseMongo,
)


async def get_use_case_with_click(
    repo: ClickHouseRepo = Depends(get_click_repo),
) -> GetEventsUseCaseClick:
    return GetEventsUseCaseClick(repo)


async def get_use_case_with_mongo(
    repo: MongoRepo = Depends(get_mongo_repo),
) -> GetEventsUseCaseMongo:
    return GetEventsUseCaseMongo(repo)
