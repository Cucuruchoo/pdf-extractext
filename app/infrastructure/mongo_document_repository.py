from datetime import UTC, datetime

from bson import ObjectId
from bson.errors import InvalidId
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ReturnDocument
from pymongo.errors import DuplicateKeyError

from app.domain.document import Document
from app.infrastructure.database import database


class MongoDocumentRepository:
    def __init__(
        self,
        mongo_database: AsyncIOMotorDatabase = database,
        collection_name: str = "documents",
    ) -> None:
        self.collection = mongo_database[collection_name]

    async def setup_indexes(self) -> None:
        await self.collection.create_index("checksum", unique=True)

    async def create(self, document: Document) -> Document:
        now = datetime.now(UTC)

        document_data = {
            "filename": document.filename,
            "content_text": document.content_text,
            "checksum": document.checksum,
            "size_bytes": document.size_bytes,
            "created_at": document.created_at or now,
            "updated_at": document.updated_at or now,
        }

        try:
            result = await self.collection.insert_one(document_data)
        except DuplicateKeyError as error:
            raise ValueError("Document already exists") from error

        document_data["_id"] = result.inserted_id
        return self._to_document(document_data)

    async def find_by_id(self, document_id: str | None) -> Document | None:
        object_id = self._to_object_id(document_id)

        if object_id is None:
            return None

        document_data = await self.collection.find_one({"_id": object_id})

        if document_data is None:
            return None

        return self._to_document(document_data)

    async def find_by_checksum(self, checksum: str) -> Document | None:
        document_data = await self.collection.find_one({"checksum": checksum})

        if document_data is None:
            return None

        return self._to_document(document_data)

    async def list_all(self) -> list[Document]:
        cursor = self.collection.find().sort("created_at", -1)
        documents = []

        async for document_data in cursor:
            documents.append(self._to_document(document_data))

        return documents

    async def update(
        self,
        document_id: str | None,
        filename: str | None = None,
        content_text: str | None = None,
    ) -> Document | None:
        object_id = self._to_object_id(document_id)

        if object_id is None:
            return None

        update_data = {}

        if filename is not None:
            update_data["filename"] = filename

        if content_text is not None:
            update_data["content_text"] = content_text

        if not update_data:
            return await self.find_by_id(document_id)

        update_data["updated_at"] = datetime.now(UTC)

        document_data = await self.collection.find_one_and_update(
            {"_id": object_id},
            {"$set": update_data},
            return_document=ReturnDocument.AFTER,
        )

        if document_data is None:
            return None

        return self._to_document(document_data)

    async def delete(self, document_id: str | None) -> bool:
        object_id = self._to_object_id(document_id)

        if object_id is None:
            return False

        result = await self.collection.delete_one({"_id": object_id})
        return result.deleted_count == 1

    def _to_document(self, document_data: dict) -> Document:
        return Document(
            id=str(document_data["_id"]),
            filename=document_data["filename"],
            content_text=document_data["content_text"],
            checksum=document_data["checksum"],
            size_bytes=document_data["size_bytes"],
            created_at=document_data.get("created_at"),
            updated_at=document_data.get("updated_at"),
        )

    def _to_object_id(self, document_id: str | None) -> ObjectId | None:
        if document_id is None:
            return None

        try:
            return ObjectId(document_id)
        except InvalidId:
            return None
