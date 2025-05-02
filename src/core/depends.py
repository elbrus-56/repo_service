from fastapi import Request
from src.database.repositories import MongoRepo, ClickHouseRepo


def get_mongo_repo(request: Request) -> MongoRepo:
    return MongoRepo(request.app.state.mongo_client)


def get_click_repo(request: Request) -> ClickHouseRepo:
    return ClickHouseRepo(request.app.state.click_pool)


