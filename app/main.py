from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.db import connect_to_mongo, close_mongo_connection
from app.middleware import TenantHeaderMiddleware
from app.routers import organizations, users, notes


@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    try:
        yield
    finally:
        await close_mongo_connection()

app = FastAPI(title="Multi-Tenant Notes API", version="1.0.0", lifespan=lifespan)

app.add_middleware(TenantHeaderMiddleware)
app.include_router(organizations.router)
app.include_router(users.router)
app.include_router(notes.router)
