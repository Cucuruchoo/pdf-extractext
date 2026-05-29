from fastapi import FastAPI

from app.infrastructure.database import ping_database

app = FastAPI(
    title="PDF Documents API",
    version="0.1.0",
)


@app.get("/")
def health_check():
    return {"status": "ok"}


@app.get("/health/db")
async def database_health_check():
    await ping_database()
    return {"database": "ok"}
