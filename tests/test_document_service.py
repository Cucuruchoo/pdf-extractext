from dataclasses import replace

import pytest

import app.application.document_service as service_module
from app.application.document_service import DocumentService
from app.domain.document import Document


class FakeDocumentRepository:
    def __init__(self):
        self.documents_by_checksum = {}
        self.documents_by_id = {}

    async def create(self, document: Document) -> Document:
        created_document = replace(document, id="generated-id")
        self.documents_by_checksum[created_document.checksum] = created_document
        self.documents_by_id[created_document.id] = created_document
        return created_document

    async def find_by_checksum(self, checksum: str) -> Document | None:
        return self.documents_by_checksum.get(checksum)

    async def find_by_id(self, document_id: str) -> Document | None:
        return self.documents_by_id.get(document_id)

    async def list_all(self) -> list[Document]:
        return list(self.documents_by_id.values())

    async def delete(self, document_id: str) -> bool:
        document = self.documents_by_id.pop(document_id, None)

        if document is None:
            return False

        self.documents_by_checksum.pop(document.checksum, None)
        return True


@pytest.mark.asyncio
async def test_create_from_pdf_validates_extracts_and_saves_document(monkeypatch):
    repository = FakeDocumentRepository()
    service = DocumentService(repository=repository)

    monkeypatch.setattr(
        service_module,
        "extract_text_from_pdf",
        lambda content: "Texto extraido del PDF",
    )

    created_document = await service.create_from_pdf(
        filename="demo.pdf",
        content=b"%PDF-1.4 fake pdf content",
        max_size_mb=10,
    )

    assert created_document.id == "generated-id"
    assert created_document.filename == "demo.pdf"
    assert created_document.content_text == "Texto extraido del PDF"
    assert created_document.size_bytes == len(b"%PDF-1.4 fake pdf content")


@pytest.mark.asyncio
async def test_create_from_pdf_rejects_duplicate_checksum(monkeypatch):
    repository = FakeDocumentRepository()
    service = DocumentService(repository=repository)

    monkeypatch.setattr(
        service_module,
        "extract_text_from_pdf",
        lambda content: "Texto extraido",
    )

    content = b"%PDF-1.4 same content"

    await service.create_from_pdf(
        filename="first.pdf",
        content=content,
        max_size_mb=10,
    )

    with pytest.raises(ValueError, match="Document already exists"):
        await service.create_from_pdf(
            filename="second.pdf",
            content=content,
            max_size_mb=10,
        )


@pytest.mark.asyncio
async def test_get_document_returns_document_by_id():
    repository = FakeDocumentRepository()
    service = DocumentService(repository=repository)

    document = Document(
        id="doc-id",
        filename="demo.pdf",
        content_text="Texto",
        checksum="abc123",
        size_bytes=100,
    )
    repository.documents_by_id["doc-id"] = document

    found_document = await service.get_document("doc-id")

    assert found_document == document


@pytest.mark.asyncio
async def test_list_documents_returns_all_documents():
    repository = FakeDocumentRepository()
    service = DocumentService(repository=repository)

    repository.documents_by_id["1"] = Document(
        id="1",
        filename="first.pdf",
        content_text="Primer texto",
        checksum="checksum-1",
        size_bytes=100,
    )
    repository.documents_by_id["2"] = Document(
        id="2",
        filename="second.pdf",
        content_text="Segundo texto",
        checksum="checksum-2",
        size_bytes=200,
    )

    documents = await service.list_documents()

    assert len(documents) == 2


@pytest.mark.asyncio
async def test_delete_document_returns_true_when_deleted():
    repository = FakeDocumentRepository()
    service = DocumentService(repository=repository)

    document = Document(
        id="doc-id",
        filename="delete.pdf",
        content_text="Texto",
        checksum="delete-checksum",
        size_bytes=100,
    )
    repository.documents_by_id["doc-id"] = document
    repository.documents_by_checksum["delete-checksum"] = document

    was_deleted = await service.delete_document("doc-id")

    assert was_deleted is True
