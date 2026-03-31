import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_response(text: str, temperature: float):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful Database Administrator."},
            {"role": "user", "content": text}
        ],
        temperature=temperature,
        max_tokens=4096,
    )
    return response
