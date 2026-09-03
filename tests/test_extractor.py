from decimal import Decimal

from pipeline.document_processor import process_document
from pipeline.extractor import extract_invoice


def test_extract_invoice_from_image():
    document = process_document("data/sample_invoice_ocr.png")

    result = extract_invoice(document)

    assert result.vendor_name.value == "ACME GmbH"
    assert result.document_number.value == "INV-123"
    assert result.document_type.value == "invoice"
    assert result.currency.value == "EUR"
    assert result.total.value == Decimal("2259.81")

    assert 0 <= result.vendor_name.confidence <= 1
    assert 0 <= result.total.confidence <= 1


def test_extract_invoice_from_scanned_pdf():
    document = process_document("data/uploads/scanned_invoice.pdf")

    assert document["source_type"] == "pdf"
    assert document["ocr_used"] is True

    result = extract_invoice(document)

    assert result.vendor_name.value == "ACME GmbH"
    assert result.document_number.value == "INV-123"
    assert result.document_type.value == "invoice"
    assert result.currency.value == "EUR"
    assert result.total.value == Decimal("2259.81")


def test_extract_ticket_from_text_pdf():
    document = process_document("data/uploads/sample_invoice.pdf")

    assert document["source_type"] == "pdf"
    assert document["ocr_used"] is False

    result = extract_invoice(document)

    assert result.vendor_name.value == "AbhiBus"
    assert result.document_type.value == "ticket"
    assert result.document_number.value == "AZ5951025163"
    assert result.currency.value == "INR"
    assert result.total.value == Decimal("1153.95")

    assert 0 <= result.vendor_name.confidence <= 1
    assert 0 <= result.total.confidence <= 1
