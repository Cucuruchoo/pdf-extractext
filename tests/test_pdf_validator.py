import pytest

from app.domain.pdf_validator import validate_pdf_file


def test_validate_pdf_file_accepts_valid_pdf():
    filename = "documento.pdf"
    content = b"%PDF-1.4 fake pdf content"

    validate_pdf_file(filename=filename, content=content, max_size_mb=10)


def test_validate_pdf_file_rejects_non_pdf_extension():
    filename = "documento.txt"
    content = b"%PDF-1.4 fake pdf content"

    with pytest.raises(ValueError, match="Only PDF files are allowed"):
        validate_pdf_file(filename=filename, content=content, max_size_mb=10)


def test_validate_pdf_file_rejects_invalid_pdf_content():
    filename = "documento.pdf"
    content = b"this is not a pdf"

    with pytest.raises(ValueError, match="Invalid PDF format"):
        validate_pdf_file(filename=filename, content=content, max_size_mb=10)


def test_validate_pdf_file_rejects_empty_file():
    filename = "documento.pdf"
    content = b""

    with pytest.raises(ValueError, match="PDF file is empty"):
        validate_pdf_file(filename=filename, content=content, max_size_mb=10)


def test_validate_pdf_file_rejects_file_larger_than_allowed_size():
    filename = "documento.pdf"
    content = b"%PDF-1.4" + b"a" * 11

    with pytest.raises(ValueError, match="PDF file exceeds maximum size"):
        validate_pdf_file(filename=filename, content=content, max_size_mb=0.00001)
