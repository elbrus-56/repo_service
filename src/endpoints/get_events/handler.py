from typing import Literal

from fastapi import APIRouter, Depends, HTTPException, Query, status

from src.endpoints.get_events.depends import (
    get_use_case_with_click,
    get_use_case_with_mongo,
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
    limit: int = Query(default=100, ge=1, description="Ограничение на вывод записей"),
    offset: int | None = Query(
        default=None, ge=0, description="Смещение при выводе записей"
    ),
    order_by: str | None = Query(
        default=None, description="Сортировка по нужному полю"
    ),
    sort: Literal["ASC", "DESC"] = Query(
        default="ASC", description="Сортировка по убывания или возрастанию"
    ),
    use_case: GetEventsUseCaseWithClick = Depends(get_use_case_with_click),
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
    order_by: str | None = Query(
        default=None, description="Сортировка по нужному полю"
    ),
    sort: Literal["1", "-1"] = Query(
        default="1", description="Сортировка по убывания или возрастанию"
    ),
    use_case: GetEventsUseCaseWithMongo = Depends(get_use_case_with_mongo),
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
