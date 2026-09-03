from pipeline.pdf_parser import extract_text_from_pdf, pdf_needs_ocr


def test_extract_text_from_pdf():
    pages = extract_text_from_pdf("data/uploads/sample_invoice.pdf")

    assert len(pages) == 2

    assert pages[0]["page_number"] == 1
    assert "AbhiBus Ticket" in pages[0]["text"]
    assert "Amount Paid" in pages[0]["text"]

    assert pages[1]["page_number"] == 2
    assert "bus/service is canceled" in pages[1]["text"]


def test_pdf_does_not_need_ocr():
    assert pdf_needs_ocr("data/uploads/sample_invoice.pdf") is False
