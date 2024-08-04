# FastAPI server.
from . import database, crud
from .routers import v1
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


database.Base.metadata.create_all(bind=database.engine, checkfirst=True)

# Create the default users in the DB.
# One user is user 'admin' with password 'admin', the other is user 'user01' with password 'password'.
crud.add_user_entry(db=database.SessionLocal(), username='admin', hashed_password='$2b$12$KVqTswsUS6R3PaYYaIeIDO7xT0kosyM88cKKUjuYzxqx9c7n7kzuS')
crud.add_user_entry(db=database.SessionLocal(), username='user01', hashed_password='$2b$12$cSZejObNN7sgA0tTvOA3lu9pxYf/xXf5BEL0KC/yTPL1R0w0JkRX6')

app = FastAPI()

origins = [
    "http://localhost:4200",
    "http://127.0.0.1:4200",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

app.include_router(
    v1.auth.router,
    prefix="/v1"
)

app.include_router(
    v1.devices.router,
    prefix="/v1"
)
