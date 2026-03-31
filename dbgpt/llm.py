import os
from openai import OpenAI
from dbgpt.utils import get_llm

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def get_response(text: str, temperature: float):
    response = client.chat.completions.create(
        model=get_llm(),
        messages=[
            {"role": "system", "content": "You are a helpful Database Administrator."},
            {"role": "user", "content": text}
        ],
        temperature=temperature,
        max_tokens=4096,
    )
    return response
