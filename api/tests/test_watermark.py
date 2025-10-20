import sys
from pathlib import Path
from io import BytesIO

import pytest

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.watermark import build_watermarked_pdf, normalize_watermark_text  # noqa: E402
from PyPDF2 import PdfReader  # noqa: E402
from reportlab.pdfgen import canvas  # noqa: E402


def _make_sample_pdf() -> bytes:
    buf = BytesIO()
    c = canvas.Canvas(buf)
    c.drawString(100, 750, "Sample Document")
    c.showPage()
    c.drawString(100, 750, "Second Page")
    c.save()
    buf.seek(0)
    return buf.read()


def test_normalize_watermark_text_trims_and_limits():
    text = "   Case    Reference   123   "
    assert normalize_watermark_text(text) == "Case Reference 123"
    long_text = "A" * 500
    assert len(normalize_watermark_text(long_text)) == 120


def test_build_watermarked_pdf_preserves_page_count():
    base_pdf = _make_sample_pdf()
    watermarked = build_watermarked_pdf(base_pdf, "CONFIDENTIAL")
    assert isinstance(watermarked, bytes)
    reader = PdfReader(BytesIO(watermarked))
    assert len(reader.pages) == 2
