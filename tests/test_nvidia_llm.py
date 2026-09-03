import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def test_nvidia_llm():
    api_key = os.getenv("NVIDIA_API_KEY")

    assert api_key, "NVIDIA_API_KEY not found in .env"

    client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=api_key,
    )

    response = client.chat.completions.create(
        model="nvidia/nemotron-3.5-lightning-30b-a3b",
        messages=[
            {
                "role": "user",
                "content": "Reply with exactly: NVIDIA LLM WORKING",
            }
        ],
        temperature=0,
        max_tokens=32,
    )

    print(response.choices[0].message.content)

    assert response.choices[0].message.content is not None
