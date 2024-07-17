# FastAPI server.
from . import database
from .routers import v1
from fastapi import FastAPI #, Depends


database.Base.metadata.create_all(bind=database.engine, checkfirst=True)

app = FastAPI()

app.include_router(
    v1.devices.router,
    prefix="/v1"
)

@app.get("/")
async def root():
    return {"message": "The root path. It will return the list of all API versions in the future. "}

@app.get("/v1")
async def api_version_1():
    return {"message": "The API v1 path. It will return the description of this API version in the future. "}

@app.get("/health")
async def health_check():
    return {"message": "Healthy."}
