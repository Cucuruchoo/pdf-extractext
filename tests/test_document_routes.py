from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.api.document_routes import get_document_service, router
from app.domain.document import Document


class FakeDocumentService:
    def __init__(self):
        self.document = Document(
            id="doc-id",
            filename="demo.pdf",
            content_text="Texto extraido",
            checksum="abc123",
            size_bytes=100,
        )

    async def create_from_pdf(
        self,
        filename: str,
        content: bytes,
        max_size_mb: float,
    ) -> Document:
        return Document(
            id="created-id",
            filename=filename,
            content_text="Texto extraido",
            checksum="created-checksum",
            size_bytes=len(content),
        )

    async def list_documents(self) -> list[Document]:
        return [self.document]

    async def get_document(self, document_id: str) -> Document | None:
        if document_id == "doc-id":
            return self.document

        return None

    async def update_document(
        self,
        document_id: str,
        filename: str | None = None,
        content_text: str | None = None,
    ) -> Document | None:
        if document_id != "doc-id":
            return None

        return Document(
            id="doc-id",
            filename=filename or "demo.pdf",
            content_text=content_text or "Texto extraido",
            checksum="abc123",
            size_bytes=100,
        )

    async def delete_document(self, document_id: str) -> bool:
        return document_id == "doc-id"


def create_test_client() -> TestClient:
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_document_service] = FakeDocumentService
    return TestClient(app)


def test_create_document_endpoint():
    client = create_test_client()

    response = client.post(
        "/documents",
        files={
            "file": (
                "demo.pdf",
                b"%PDF-1.4 fake pdf content",
                "application/pdf",
            ),
        },
    )

    assert response.status_code == 201
    data = response.json()
    assert data["id"] == "created-id"
    assert data["filename"] == "demo.pdf"
    assert data["content_text"] == "Texto extraido"
    assert data["checksum"] == "created-checksum"


def test_list_documents_endpoint():
    client = create_test_client()

    response = client.get("/documents")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == "doc-id"


def test_get_document_endpoint():
    client = create_test_client()

    response = client.get("/documents/doc-id")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "doc-id"
    assert data["filename"] == "demo.pdf"


def test_get_document_endpoint_returns_404_when_not_found():
    client = create_test_client()

    response = client.get("/documents/not-found")

    assert response.status_code == 404
    assert response.json()["detail"] == "Document not found"


def test_update_document_endpoint():
    client = create_test_client()

    response = client.put(
        "/documents/doc-id",
        json={
            "filename": "updated.pdf",
            "content_text": "Texto actualizado",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "doc-id"
    assert data["filename"] == "updated.pdf"
    assert data["content_text"] == "Texto actualizado"


def test_delete_document_endpoint():
    client = create_test_client()

    response = client.delete("/documents/doc-id")

    assert response.status_code == 204


def test_delete_document_endpoint_returns_404_when_not_found():
    client = create_test_client()

    response = client.delete("/documents/not-found")

    assert response.status_code == 404
    assert response.json()["detail"] == "Document not found"
