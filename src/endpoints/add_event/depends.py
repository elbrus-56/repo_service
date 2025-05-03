from fastapi import Depends

from src.core.depends import get_click_repo, get_mongo_repo
from src.database.repositories import ClickHouseRepo, MongoRepo
from src.endpoints.add_event.use_cases.for_click import (
    AddEventUseCase as AddEventUseCaseClick,
)
from src.endpoints.add_event.use_cases.for_mongo import (
    AddEventUseCase as AddEventUseCaseMongo,
)


async def get_use_case_with_click(
    repo: ClickHouseRepo = Depends(get_click_repo),
) -> AddEventUseCaseClick:
    return AddEventUseCaseClick(repo)


async def get_use_case_with_mongo(
    repo: MongoRepo = Depends(get_mongo_repo),
) -> AddEventUseCaseMongo:
    return AddEventUseCaseMongo(repo)
