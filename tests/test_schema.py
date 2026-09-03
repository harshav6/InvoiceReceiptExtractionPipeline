from schemas.invoice import Invoice
from decimal import Decimal


def test_invoice_schema():
    invoice = Invoice(
        vendor_name="ACME GmbH",
        invoice_number="INV-123",
        currency="EUR",
        total=2259.81,
    )

    assert invoice.vendor_name == "ACME GmbH"
    assert invoice.invoice_number == "INV-123"
    assert invoice.total == Decimal("2259.81")
