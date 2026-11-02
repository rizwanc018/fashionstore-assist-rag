from openai import OpenAI

from fashion_store_rag.config.settings import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)


def generate_answer(prompt: str) -> str:
    response = client.responses.create(model="gpt-5-mini", input=prompt)
    return response.output_text
