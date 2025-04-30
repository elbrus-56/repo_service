from fastapi import APIRouter


router = APIRouter()


@router.post("/add_event")
async def add_event():
    pass
