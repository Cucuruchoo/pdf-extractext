from io import BytesIO

import pytest

import app.infrastructure.pdf_text_extractor as extractor_module
from app.infrastructure.pdf_text_extractor import extract_text_from_pdf


class FakePage:
    def __init__(self, text):
        self.text = text

    def extract_text(self):
        return self.text


def test_extract_text_from_pdf_reads_pdf_from_memory(monkeypatch):
    class FakePdfReader:
        def __init__(self, pdf_stream):
            assert isinstance(pdf_stream, BytesIO)
            self.pages = [
                FakePage("Primera pagina"),
                FakePage(None),
                FakePage("Segunda pagina"),
            ]

    monkeypatch.setattr(extractor_module, "PdfReader", FakePdfReader)

    result = extract_text_from_pdf(b"%PDF-1.4 fake pdf content")

    assert result == "Primera pagina\nSegunda pagina"


def test_extract_text_from_pdf_rejects_pdf_without_text(monkeypatch):
    class FakePdfReader:
        def __init__(self, pdf_stream):
            self.pages = [
                FakePage(None),
                FakePage(""),
            ]

    monkeypatch.setattr(extractor_module, "PdfReader", FakePdfReader)

    with pytest.raises(ValueError, match="PDF text could not be extracted"):
        extract_text_from_pdf(b"%PDF-1.4 fake pdf content")
