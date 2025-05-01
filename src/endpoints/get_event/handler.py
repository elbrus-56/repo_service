from fastapi import APIRouter, Depends
from src.endpoints.get_event.models import MongoOrder, Order
from src.database.repositories import ClickHouseRepo, MongoRepo
from src.core.depends import get_click_repo, get_mongo_repo

router = APIRouter()


@router.get("/get-events-c", tags=["click"])
async def get_event_click(
    db: ClickHouseRepo = Depends(get_click_repo),
) -> list[Order]:
    return [
        Order(**order)
        for order in await db.get(
            target="events.orders",
        )
    ]


@router.get("/get-events-m", tags=["mongo"])
async def get_event_mongo(
    db: MongoRepo = Depends(get_mongo_repo),
) -> list[Order] | None:
    return [
        MongoOrder(**order)
        for order in await db.get(
            target="orders",
            filter={"shipping_address_city": ["City 0"]},
        )
    ]
