import time
from typing import Literal

from pydantic import BaseModel, Field

from fashion_store_rag.services.llm import client

# query_classification_description = """
#             Classify the customer's query into exactly one intent:
#             'product_search' when the customer wants to find products matching specific requirements or preferences;
#             'faq' when the customer asks about store policies or general store information, such as returns, shipping, payments, or refunds; "
#             'out_of_scope' when the query is unrelated to the fashion store or its products.
#             """


class QueryClassification(BaseModel):
    intent: Literal[
        "product_search",
        "faq",
        "out_of_scope",
    ] = Field(description="The intent of the customer's query")


def classify_query(query: str, timings: dict | None = None) -> QueryClassification:
    classification_start = time.perf_counter()

    response = client.responses.parse(
        model="gpt-5-mini",
        input=[
            {
                "role": "system",
                "content": """
                You are a query classifier for a fashion store assistant.

                Classify the customer's query into exactly one category:

                - product_search: Finding products.
                - faq: Asking about store policies, shipping, returns, or payments.
                - out_of_scope: Unrelated to the fashion store.

                Return only the appropriate classification.
                """,
            },
            {
                "role": "user",
                "content": query,
            },
        ],
        text_format=QueryClassification,
    )
    classification_ms = (time.perf_counter() - classification_start) * 1000
    if timings is not None:
        timings["classification_ms"] = round(classification_ms, 2)

    return response.output_parsed
