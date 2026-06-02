import logging
import os

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from app.application.document_service import DocumentService
from app.domain.document import Document
from app.schemas.document_schema import DocumentResponse, DocumentUpdateRequest

router = APIRouter(prefix="/documents", tags=["documents"])

MAX_PDF_SIZE_MB = float(os.getenv("MAX_PDF_SIZE_MB", "10"))

logger = logging.getLogger(__name__)


def get_document_service() -> DocumentService:
    return DocumentService()


def document_to_response(document: Document) -> DocumentResponse:
    return DocumentResponse(
        id=document.id or "",
        filename=document.filename,
        content_text=document.content_text,
        checksum=document.checksum,
        size_bytes=document.size_bytes,
        created_at=document.created_at,
        updated_at=document.updated_at,
    )


@router.post(
    "",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def create_document(
    file: UploadFile = File(...),
    service: DocumentService = Depends(get_document_service),
):
    content = await file.read()
    filename = file.filename or ""

    logger.info(
        "Creating document from uploaded file: filename=%s size=%s",
        filename,
        len(content),
    )

    try:
        document = await service.create_from_pdf(
            filename=filename,
            content=content,
            max_size_mb=MAX_PDF_SIZE_MB,
        )
    except ValueError as error:
        logger.warning(
            "Document creation failed: filename=%s error=%s",
            filename,
            str(error),
        )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        ) from error

    logger.info(
        "Document created successfully: id=%s checksum=%s",
        document.id,
        document.checksum,
    )

    return document_to_response(document)


@router.get("", response_model=list[DocumentResponse])
async def list_documents(
    service: DocumentService = Depends(get_document_service),
):
    logger.info("Listing documents")
    documents = await service.list_documents()
    logger.info("Documents listed successfully: count=%s", len(documents))
    return [document_to_response(document) for document in documents]


@router.get("/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    service: DocumentService = Depends(get_document_service),
):
    logger.info("Getting document: id=%s", document_id)

    document = await service.get_document(document_id)

    if document is None:
        logger.warning("Document not found: id=%s", document_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    logger.info("Document found: id=%s", document_id)
    return document_to_response(document)


@router.put("/{document_id}", response_model=DocumentResponse)
async def update_document(
    document_id: str,
    payload: DocumentUpdateRequest,
    service: DocumentService = Depends(get_document_service),
):
    logger.info("Updating document: id=%s", document_id)

    document = await service.update_document(
        document_id=document_id,
        filename=payload.filename,
        content_text=payload.content_text,
    )

    if document is None:
        logger.warning("Document update failed, document not found: id=%s", document_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    logger.info("Document updated successfully: id=%s", document.id)
    return document_to_response(document)


@router.delete(
    "/{document_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_document(
    document_id: str,
    service: DocumentService = Depends(get_document_service),
):
    logger.info("Deleting document: id=%s", document_id)

    was_deleted = await service.delete_document(document_id)

    if not was_deleted:
        logger.warning("Document delete failed, document not found: id=%s", document_id)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    logger.info("Document deleted successfully: id=%s", document_id)
