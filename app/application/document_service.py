from app.domain.checksum import calculate_sha256
from app.domain.document import Document
from app.domain.pdf_validator import validate_pdf_file
from app.infrastructure.mongo_document_repository import MongoDocumentRepository
from app.infrastructure.pdf_text_extractor import extract_text_from_pdf


class DocumentService:
    def __init__(self, repository: MongoDocumentRepository | None = None) -> None:
        self.repository = repository or MongoDocumentRepository()

    async def create_from_pdf(
        self,
        filename: str,
        content: bytes,
        max_size_mb: float,
    ) -> Document:
        validate_pdf_file(
            filename=filename,
            content=content,
            max_size_mb=max_size_mb,
        )

        checksum = calculate_sha256(content)
        existing_document = await self.repository.find_by_checksum(checksum)

        if existing_document is not None:
            raise ValueError("Document already exists")

        content_text = extract_text_from_pdf(content)

        document = Document(
            filename=filename,
            content_text=content_text,
            checksum=checksum,
            size_bytes=len(content),
        )

        return await self.repository.create(document)

    async def get_document(self, document_id: str) -> Document | None:
        return await self.repository.find_by_id(document_id)

    async def list_documents(self) -> list[Document]:
        return await self.repository.list_all()

    async def delete_document(self, document_id: str) -> bool:
        return await self.repository.delete(document_id)
