from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel

from src.configs import settings
from src.endpoints.add_event.handler import router as add_event_router
from src.endpoints.get_events.handler import router as get_event_router


async def lifespan(app: FastAPI):
    app.state.mongo_client = AsyncIOMotorClient(settings.mongo_uri)
    yield
    app.state.mongo_client.close()


app = FastAPI(lifespan=lifespan, title="Pet service")
app.include_router(add_event_router)
app.include_router(get_event_router)


class RootResponse(BaseModel):
    message: str = "Welcome pet service"


@app.get("/", tags=["root"])
async def root() -> RootResponse:
    return RootResponse()
