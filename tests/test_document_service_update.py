import pytest

from app.application.document_service import DocumentService
from app.domain.document import Document


class FakeUpdateDocumentRepository:
    async def update(
        self,
        document_id: str,
        filename: str | None = None,
        content_text: str | None = None,
    ) -> Document:
        return Document(
            id=document_id,
            filename=filename or "original.pdf",
            content_text=content_text or "Texto original",
            checksum="abc123",
            size_bytes=100,
        )


@pytest.mark.asyncio
async def test_update_document_returns_updated_document():
    service = DocumentService(repository=FakeUpdateDocumentRepository())

    updated_document = await service.update_document(
        document_id="doc-id",
        filename="updated.pdf",
        content_text="Texto actualizado",
    )

    assert updated_document.id == "doc-id"
    assert updated_document.filename == "updated.pdf"
    assert updated_document.content_text == "Texto actualizado"
