import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def test_nvidia_connection():
    api_key = os.getenv("NVIDIA_API_KEY")

    assert api_key, "NVIDIA_API_KEY not found in .env"

    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=api_key,
    )

    response = client.chat.completions.create(
        model="nvidia/nemotron-parse",
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": "https://assets.ngc.nvidia.com/products/api-catalog/nemotron-parse/example_2.jpg"
                        },
                    }
                ],
            }
        ],
        max_tokens=256,
    )

    print(response)
