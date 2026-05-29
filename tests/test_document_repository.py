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
    database = client["pdf_documents_test"]

    await database.documents.delete_many({})

    repo = MongoDocumentRepository(database)
    await repo.setup_indexes()

    yield repo

    await database.documents.drop()
    client.close()


@pytest.mark.asyncio
async def test_create_document_and_find_by_id(repository):
    document = Document(
        filename="demo.pdf",
        content_text="Texto extraido",
        checksum="abc123",
        size_bytes=100,
    )

    created_document = await repository.create(document)
    found_document = await repository.find_by_id(created_document.id)

    assert found_document is not None
    assert found_document.id == created_document.id
    assert found_document.filename == "demo.pdf"
    assert found_document.content_text == "Texto extraido"
    assert found_document.checksum == "abc123"
    assert found_document.size_bytes == 100


@pytest.mark.asyncio
async def test_find_by_checksum(repository):
    document = Document(
        filename="checksum.pdf",
        content_text="Contenido",
        checksum="checksum-123",
        size_bytes=200,
    )

    await repository.create(document)
    found_document = await repository.find_by_checksum("checksum-123")

    assert found_document is not None
    assert found_document.filename == "checksum.pdf"


@pytest.mark.asyncio
async def test_list_all_documents(repository):
    first_document = Document(
        filename="first.pdf",
        content_text="Primer documento",
        checksum="checksum-1",
        size_bytes=100,
    )
    second_document = Document(
        filename="second.pdf",
        content_text="Segundo documento",
        checksum="checksum-2",
        size_bytes=200,
    )

    await repository.create(first_document)
    await repository.create(second_document)

    documents = await repository.list_all()

    assert len(documents) == 2


@pytest.mark.asyncio
async def test_delete_document(repository):
    document = Document(
        filename="delete.pdf",
        content_text="Documento a eliminar",
        checksum="delete-123",
        size_bytes=300,
    )

    created_document = await repository.create(document)

    was_deleted = await repository.delete(created_document.id)
    found_document = await repository.find_by_id(created_document.id)

    assert was_deleted is True
    assert found_document is None


@pytest.mark.asyncio
async def test_create_document_rejects_duplicate_checksum(repository):
    first_document = Document(
        filename="first.pdf",
        content_text="Primer documento",
        checksum="duplicated-checksum",
        size_bytes=100,
    )
    second_document = Document(
        filename="second.pdf",
        content_text="Segundo documento",
        checksum="duplicated-checksum",
        size_bytes=200,
    )

    await repository.create(first_document)

    with pytest.raises(ValueError, match="Document already exists"):
        await repository.create(second_document)
