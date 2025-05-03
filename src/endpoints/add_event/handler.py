from fastapi import APIRouter, Depends, HTTPException, status

from src.endpoints.add_event.models import Order
from src.endpoints.add_event.depends import add_event_use_case_with_click
from src.endpoints.add_event.use_cases.for_click import AddEventUseCase


router = APIRouter()


@router.post("/add-event-c", tags=["click"])
async def add_event_click(
    use_case: AddEventUseCase = Depends(add_event_use_case_with_click),
) -> Order:
    try:
        records = await use_case.execute()
        return records
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed get events: {exc},",
        )


@router.post("/add-event-m", tags=["mongo"])
async def add_event_mongo():
    pass
