PDF_SIGNATURE = b"%PDF"


def validate_pdf_file(filename: str, content: bytes, max_size_mb: float) -> None:
    if not filename.lower().endswith(".pdf"):
        raise ValueError("Only PDF files are allowed")

    if not content:
        raise ValueError("PDF file is empty")

    max_size_bytes = max_size_mb * 1024 * 1024

    if len(content) > max_size_bytes:
        raise ValueError("PDF file exceeds maximum size")

    if not content.startswith(PDF_SIGNATURE):
        raise ValueError("Invalid PDF format")
