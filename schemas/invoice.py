from datetime import date
from decimal import Decimal

from pydantic import BaseModel, Field


class LineItem(BaseModel):
    description: str
    quantity: Decimal | None = None
    unit_price: Decimal | None = None
    total: Decimal | None = None


class Invoice(BaseModel):
    vendor_name: str | None = None
    invoice_number: str | None = None
    invoice_date: date | None = None

    currency: str | None = None

    line_items: list[LineItem] = Field(default_factory=list)

    subtotal: Decimal | None = None
    tax: Decimal | None = None
    tax_rate: Decimal | None = None
    total: Decimal | None = None
