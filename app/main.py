from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.document_routes import router as document_router
from app.infrastructure.database import ping_database
from app.infrastructure.mongo_document_repository import MongoDocumentRepository


@asynccontextmanager
async def lifespan(app: FastAPI):
    repository = MongoDocumentRepository()
    await repository.setup_indexes()
    yield


app = FastAPI(
    title="PDF Documents API",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(document_router)


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.get("/health/db")
async def database_health_check():
    await ping_database()
    return {"database": "ok"}
