from fastapi import Depends

from src.core.depends import get_click_repo, get_mongo_repo
from src.database.repositories import ClickHouseRepo, MongoRepo
from src.endpoints.update_event.use_cases.for_click import (
    UpdateEventUseCase as UpdateEventUseCaseClick,
)
from src.endpoints.update_event.use_cases.for_mongo import (
    UpdateEventUseCase as UpdateEventUseCaseMongo,
)


async def get_use_case_with_click(
    repo: ClickHouseRepo = Depends(get_click_repo),
) -> UpdateEventUseCaseClick:
    return UpdateEventUseCaseClick(repo)


async def get_use_case_with_mongo(
    repo: MongoRepo = Depends(get_mongo_repo),
) -> UpdateEventUseCaseMongo:
    return UpdateEventUseCaseMongo(repo)
