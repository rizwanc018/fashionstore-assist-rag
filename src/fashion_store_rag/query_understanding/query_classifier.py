from typing import Literal

from pydantic import BaseModel, Field

from fashion_store_rag.services.llm import client

# query_classification_description = """
#             Classify the customer's query into exactly one intent:
#             'product_search' when the customer wants to find products matching specific requirements or preferences;
#             'product_question' when the customer asks about a specific product's attributes, such as color, size, fabric, price, or availability; "
#             'product_comparison' when the customer wants to compare two or more products based on their features, prices, or other attributes; "
#             'faq' when the customer asks about store policies or general store information, such as returns, shipping, payments, or refunds; "
#             'out_of_scope' when the query is unrelated to the fashion store or its products.
#             """


class QueryClassification(BaseModel):
    intent: Literal[
        "product_search",
        "product_question",
        "product_comparison",
        "faq",
        "out_of_scope",
    ] = Field(description="The intent of the customer's query")


def classify_query(query: str) -> QueryClassification:
    response = client.responses.parse(
        model="gpt-5-mini",
        input=[
            {
                "role": "system",
                "content": """
                You are a query classifier for a fashion store assistant.

                Classify the customer's query into exactly one category:

                - product_search: Finding products.
                - product_question: Asking about product attributes.
                - product_comparison: Comparing products or alternatives.
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

    return response.output_parsed


if __name__ == "__main__":
    queries = [
        "Show me black T-shirts for men",
        "What fabric is this shirt made of?",
        "Compare these two T-shirts",
        "What is your return policy?",
        "Can you explain quantum physics?",
    ]

    for query in queries:
        result = classify_query(query)

        print(f"\nQuery: {query}")
        print(f"Intent: {result.intent}")
