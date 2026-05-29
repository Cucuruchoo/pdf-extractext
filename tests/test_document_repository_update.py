import os

import pytest
import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient

from app.domain.document import Document
from app.infrastructure.mongo_document_repository import MongoDocumentRepository


@pytest_asyncio.fixture
async def repository():
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    client = AsyncIOMotorClient(mongo_uri)
    database = client["pdf_documents_test_update"]

    await database.documents.delete_many({})

    repo = MongoDocumentRepository(database)
    await repo.setup_indexes()

    yield repo

    await database.documents.drop()
    client.close()


@pytest.mark.asyncio
async def test_update_document_changes_filename_and_content_text(repository):
    document = Document(
        filename="original.pdf",
        content_text="Texto original",
        checksum="update-checksum",
        size_bytes=100,
    )

    created_document = await repository.create(document)

    updated_document = await repository.update(
        document_id=created_document.id,
        filename="updated.pdf",
        content_text="Texto actualizado",
    )

    assert updated_document is not None
    assert updated_document.id == created_document.id
    assert updated_document.filename == "updated.pdf"
    assert updated_document.content_text == "Texto actualizado"
    assert updated_document.checksum == "update-checksum"

    found_document = await repository.find_by_id(created_document.id)

    assert found_document is not None
    assert found_document.filename == "updated.pdf"
    assert found_document.content_text == "Texto actualizado"
