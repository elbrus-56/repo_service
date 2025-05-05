from typing import Literal

from fastapi import APIRouter, Body, Depends, HTTPException, Path, status

from src.endpoints.update_event.depends import (
    get_use_case_with_click,
    get_use_case_with_mongo,
)
from src.endpoints.update_event.models import Order
from src.endpoints.update_event.use_cases.for_click import (
    UpdateEventUseCase as UpdateEventUseCaseClick,
)
from src.endpoints.update_event.use_cases.for_mongo import (
    UpdateEventUseCase as UpdateEventUseCaseMongo,
)

router = APIRouter()


@router.patch("/update-event-c", tags=["click"])
async def update_event_click(
    body: Order = Body(),
    use_case: UpdateEventUseCaseClick = Depends(get_use_case_with_click),
) -> None | Literal[True]:
    try:
        return await use_case.execute(data=body)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed update event: {exc},",
        )


@router.patch("/update-event-m", tags=["mongo"])
async def update_event_mongo(
    body: Order = Body(),
    use_case: UpdateEventUseCaseMongo = Depends(get_use_case_with_mongo),
):
    try:
        return await use_case.execute(data=body)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed update event: {exc},",
        )
