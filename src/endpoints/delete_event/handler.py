from typing import Literal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from src.endpoints.delete_event.depends import (
    get_use_case_with_click,
    get_use_case_with_mongo,
)
from src.endpoints.delete_event.use_cases.for_click import (
    DelEventUseCase as DelEventUseCaseClick,
)
from src.endpoints.delete_event.use_cases.for_mongo import (
    DelEventUseCase as DelEventUseCaseMongo,
)

router = APIRouter()


@router.delete("/delete-event-c", tags=["click"])
async def del_event_click(
    order_id: UUID,
    use_case: DelEventUseCaseClick = Depends(get_use_case_with_click),
) -> None | Literal[True]:
    try:
        return await use_case.execute(params={"order_id": order_id})
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed delete event: {exc},",
        )


@router.delete("/delete-event-m", tags=["mongo"])
async def del_event_mongo(
    order_id: UUID,
    use_case: DelEventUseCaseMongo = Depends(get_use_case_with_mongo),
):
    try:
        return await use_case.execute(filter={"order_id": str(order_id)})
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed delete event: {exc},",
        )
