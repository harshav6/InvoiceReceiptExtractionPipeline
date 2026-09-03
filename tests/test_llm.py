from decimal import Decimal

from pipeline.llm import extract_invoice_with_gemini


def test_gemini_invoice_extraction():
    text = """
    INVOICE
    Vendor: ACME GmbH
    Invoice Number: INV-123
    Date: 2026-09-03
    Subtotal: EUR 1,899.00
    Tax: EUR 360.81
    Total: EUR 2,259.81
    """

    result = extract_invoice_with_gemini(text)

    assert result.vendor_name.value == "ACME GmbH"
    assert result.document_type.value == "invoice"
    assert result.document_number.value == "INV-123"
    assert result.total.value == Decimal("2259.81")

    assert 0 <= result.vendor_name.confidence <= 1
    assert 0 <= result.total.confidence <= 1
