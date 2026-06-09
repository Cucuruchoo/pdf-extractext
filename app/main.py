from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI

from app.api.document_routes import router as document_router
from app.infrastructure.database import ping_database
from app.infrastructure.logging_config import configure_logging
from app.infrastructure.mongo_document_repository import MongoDocumentRepository
from app.infrastructure.security_headers import SecurityHeadersMiddleware

configure_logging()

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting PDF Documents API")
    repository = MongoDocumentRepository()
    await repository.setup_indexes()
    logger.info("MongoDB indexes configured")
    yield
    logger.info("Stopping PDF Documents API")


app = FastAPI(
    title="PDF Documents API",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(SecurityHeadersMiddleware)

app.include_router(document_router)


@app.get("/")
def health_check():
    logger.info("Health check requested")
    return {"status": "ok"}


@app.get("/health/db")
async def database_health_check():
    logger.info("Database health check requested")
    await ping_database()
    logger.info("Database health check succeeded")
    return {"database": "ok"}
