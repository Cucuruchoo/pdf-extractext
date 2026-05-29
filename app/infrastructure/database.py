import os

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "pdf_documents")

client = AsyncIOMotorClient(MONGO_URI)
database = client[MONGO_DB_NAME]


async def ping_database() -> bool:
    await client.admin.command("ping")
    return True
