from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.endpoints.get_events.depends import (
    get_events_use_case_with_click,
    get_events_use_case_with_mongo,
)
from src.endpoints.get_events.models import Order
from src.endpoints.get_events.use_cases.for_click import (
    GetEventsUseCase as GetEventsUseCaseWithClick,
)
from src.endpoints.get_events.use_cases.for_mongo import (
    GetEventsUseCase as GetEventsUseCaseWithMongo,
)

router = APIRouter()


@router.get("/get-events-c", tags=["click"])
async def get_events_click(
    limit: int = Query(default=100, ge=1),
    offset: int | None = Query(default=None, ge=0),
    order_by: str | None = Query(
        default=None, description="Сортировка по нужному полю"
    ),
    sort: Literal["ASC", "DESC"] = "ASC",
    use_case: GetEventsUseCaseWithClick = Depends(get_events_use_case_with_click),
) -> list[Order]:
    try:
        records = await use_case.execute(
            limit=limit,
            offset=offset,
            order_by=order_by,
            sort=sort,
        )
        return records
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed get events: {exc},",
        )


@router.get("/get-events-m", tags=["mongo"])
async def get_events_mongo(
    limit: int = Query(default=100, ge=1),
    offset: int = 0,
    use_case: GetEventsUseCaseWithMongo = Depends(get_events_use_case_with_mongo),
) -> list[Order]:
    try:
        records = await use_case.execute(limit=limit, offset=offset)
        return records
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed get events: {exc},",
        )
