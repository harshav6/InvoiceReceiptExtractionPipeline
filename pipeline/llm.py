import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from schemas.extraction import InvoiceExtraction

load_dotenv()

NVIDIA_BASE_URL = "https://integrate.api.nvidia.com/v1"
NVIDIA_MODEL = "nvidia/nemotron-3.5-lightning-30b-a3b"


def create_nvidia_client() -> OpenAI:
    api_key = os.getenv("NVIDIA_API_KEY")

    if not api_key:
        raise RuntimeError("NVIDIA_API_KEY not found in .env")

    return OpenAI(
        base_url=NVIDIA_BASE_URL,
        api_key=api_key,
    )


def _extract_json(text: str) -> dict:
    """
    Extract a JSON object from the model response.
    """

    text = text.strip()

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    start = text.find("{")
    end = text.rfind("}")

    if start == -1 or end == -1 or end <= start:
        raise ValueError("Model response does not contain valid JSON")

    return json.loads(text[start : end + 1])


def extract_invoice_with_gemini(text: str) -> InvoiceExtraction:
    """
    Extract structured invoice, receipt, or ticket data using NVIDIA.

    Kept with the old function name temporarily so the existing
    extractor.py does not need to change yet.
    """

    client = create_nvidia_client()

    prompt = f"""
You are a document extraction system for invoices, receipts, and tickets.

Extract structured information from the document below.

Return ONLY valid JSON.
Do not include markdown, explanations, or reasoning.

The JSON must have exactly these top-level fields:

{{
  "document_type": {{
    "value": "invoice",
    "confidence": 0.0
  }},
  "vendor_name": {{
    "value": null,
    "confidence": 0.0
  }},
  "document_number": {{
    "value": null,
    "confidence": 0.0
  }},
  "invoice_date": {{
    "value": null,
    "confidence": 0.0
  }},
  "currency": {{
    "value": null,
    "confidence": 0.0
  }},
  "line_items": [],
  "subtotal": {{
    "value": null,
    "confidence": 0.0
  }},
  "tax": {{
    "value": null,
    "confidence": 0.0
  }},
  "tax_rate": {{
    "value": null,
    "confidence": 0.0
  }},
  "total": {{
    "value": null,
    "confidence": 0.0
  }}
}}

Rules:
- document_type must be exactly one of:
  "invoice", "receipt", or "ticket".
- document_number should contain the primary identifier shown on
  the document, such as an invoice number, receipt number,
  ticket number, or booking ID.
- Return only information explicitly present in the document.
- Do not invent missing values.
- Use null when a value is not available.
- Confidence must be between 0 and 1.
- Preserve monetary values accurately.
- Extract every identifiable purchased item, service, fare, or charge.
- Distinguish the document date from other dates such as booking,
  travel, delivery, or due dates.

DOCUMENT:
{text}
"""

    response = client.chat.completions.create(
        model=NVIDIA_MODEL,
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        temperature=0,
        max_tokens=4096,
    )

    content = response.choices[0].message.content

    if not content:
        raise ValueError("NVIDIA returned an empty response")

    data = _extract_json(content)

    return InvoiceExtraction.model_validate(data)


def extract_invoice_from_images(
    images: list,
    text: str = "",
) -> InvoiceExtraction:
    """
    Vision extraction placeholder.

    NVIDIA's current nemotron-3.5-lightning model is text-only,
    so image extraction will be connected to Nemotron Parse separately.
    """

    raise NotImplementedError(
        "Image extraction will use NVIDIA Nemotron Parse before "
        "the text extraction stage."
    )
