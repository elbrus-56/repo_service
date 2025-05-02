from fastapi import Request

from src.configs import settings
from src.database.repositories import ClickHouseRepo, MongoRepo


def get_mongo_repo(request: Request) -> MongoRepo:
    return MongoRepo(request.app.state.mongo_client)


def get_click_repo() -> ClickHouseRepo:
    return ClickHouseRepo(settings)
