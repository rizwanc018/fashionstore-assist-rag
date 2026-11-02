from pydantic import BaseModel, Field

from fashion_store_rag.services.llm import client


class QueryRewrite(BaseModel):
    rewritten_query: str = Field(description="Then improved search query")


def rewrite_query(query: str) -> QueryRewrite:
    response = client.responses.parse(
        model="gpt-5-mini",
        input=[
            {
                "role": "system",
                "content": """
                You are query rewriting assistant for a fashion store.
                
                Rewrite the customer's qeury into a clear, concise query suitable for semantic product search.
                
                Follow these rules:
                - Preserve the original meaning and intent.
                - Preserve all explicitly mentioned requirements, such as color, size, gender, fabric and usage.
                - Do not invent product attributes or preferences.
                - Expand vague wording only when the meaning is reasonably clear from the query.
                - Do not answer the customer's question.
                """,
            },
            {"role": "user", "content": query},
        ],
        text_format=QueryRewrite,
    )

    return response.output_parsed
