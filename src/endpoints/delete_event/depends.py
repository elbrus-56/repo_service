from fastapi import Depends

from src.core.depends import get_click_repo, get_mongo_repo
from src.database.repositories import ClickHouseRepo, MongoRepo
from src.endpoints.delete_event.use_cases.for_click import (
    DelEventUseCase as DelEventUseCaseClick,
)
from src.endpoints.delete_event.use_cases.for_mongo import (
    DelEventUseCase as DelEventUseCaseMongo,
)


async def get_use_case_with_click(
    repo: ClickHouseRepo = Depends(get_click_repo),
) -> DelEventUseCaseClick:
    return DelEventUseCaseClick(repo)


async def get_use_case_with_mongo(
    repo: MongoRepo = Depends(get_mongo_repo),
) -> DelEventUseCaseMongo:
    return DelEventUseCaseMongo(repo)
