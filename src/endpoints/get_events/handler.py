from fastapi import APIRouter, Depends, HTTPException, Query, status
from src.endpoints.get_events.depends import get_events_use_case_with_click
from src.endpoints.get_events.use_cases.for_click import (
    GetEventsUseCase as GetEventsUseCaseWithClick,
)
from src.endpoints.get_events.use_cases.for_mongo import (
    GetEventsUseCase as GetEventsUseCaseWithMongo,
)
from src.endpoints.get_events.models import Order
from src.core.depends import get_mongo_repo


router = APIRouter()


@router.get("/get-events-c", tags=["click"])
async def get_events_click(
    limit: int = Query(default=100, ge=1),
    use_case: GetEventsUseCaseWithClick = Depends(get_events_use_case_with_click),
) -> list[Order]:
    try:
        records = await use_case.execute(limit=limit)
        return records
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed get events: {exc},",
        )


@router.get("/get-events-m", tags=["mongo"])
async def get_events_mongo(
    limit: int = Query(default=100, ge=1),
    use_case: GetEventsUseCaseWithMongo = Depends(get_mongo_repo),
) -> list[Order]:
    try:
        records = await use_case.execute(limit=limit)
        return records
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed get events: {exc},",
        )
