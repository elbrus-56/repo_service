from fastapi import APIRouter, Depends, HTTPException, status

from src.endpoints.add_event.models import Order
from src.endpoints.add_event.depends import (
    get_use_case_with_click,
    get_use_case_with_mongo,
)
from src.endpoints.add_event.use_cases.for_click import (
    AddEventUseCase as AddEventUseCaseClick,
)
from src.endpoints.add_event.use_cases.for_mongo import (
    AddEventUseCase as AddEventUseCaseMongo,
)

router = APIRouter()


@router.post("/add-event-c", tags=["click"])
async def add_event_click(
    use_case: AddEventUseCaseClick = Depends(get_use_case_with_click),
) -> Order:
    try:
        records = await use_case.execute()
        return records
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed add event: {exc},",
        )


@router.post("/add-event-m", tags=["mongo"])
async def add_event_mongo(
    use_case: AddEventUseCaseMongo = Depends(get_use_case_with_mongo),
):
    try:
        records = await use_case.execute()
        return records
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed add event: {exc},",
        )
