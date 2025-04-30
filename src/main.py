from fastapi import FastAPI
from src.endpoints.add_event.handler import router as add_event_router


app = FastAPI(title="Pet service")
app.include_router(add_event_router)


@app.get("/", tags=["root"])
async def root():
    return {"message": "Welcome pet service"}
