import pymupdf


def extract_text_from_pdf(file_path: str) -> list[dict]:
    """
    Extract text from each page of a PDF.

    Args:
        file_path: Path to the PDF file.

    Returns:
        A list containing page number and extracted text.
    """
    document = pymupdf.open(file_path)

    try:
        pages = []

        for page_number, page in enumerate(document, start=1):
            text = page.get_text("text").strip()

            pages.append(
                {
                    "page_number": page_number,
                    "text": text,
                }
            )

        return pages

    finally:
        document.close()


def pdf_needs_ocr(file_path: str, min_chars: int = 20) -> bool:
    """
    Determine whether a PDF likely needs OCR.

    Args:
        file_path: Path to the PDF file.
        min_chars: Minimum number of extracted characters
                   required to consider the PDF text-readable.

    Returns:
        True if OCR is likely needed, otherwise False.
    """
    pages = extract_text_from_pdf(file_path)

    total_characters = sum(len(page["text"]) for page in pages)

    return total_characters < min_chars
