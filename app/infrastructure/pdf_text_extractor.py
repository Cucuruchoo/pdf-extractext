from io import BytesIO

from pypdf import PdfReader


def extract_text_from_pdf(content: bytes) -> str:
    pdf_stream = BytesIO(content)
    reader = PdfReader(pdf_stream)

    extracted_pages: list[str] = []

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            extracted_pages.append(page_text.strip())

    text = "\n".join(extracted_pages).strip()

    if not text:
        raise ValueError("PDF text could not be extracted")

    return text
