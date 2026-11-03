from typing import Literal

from pydantic import BaseModel, Field

from fashion_store_rag.services.llm import client


class RetrievalEvaluation(BaseModel):
    relevant: bool = Field(
        description="Whether the retrieved products are relevant to customers query."
    )
    score: int = Field(ge=0, le=5, description="Overall relevance score from 0 to 5.")
    reasoning: str = Field(
        description="Brief explanation of why the retrieved products are or are not relevant."
    )
    decision: Literal["accept", "retry"] = Field(
        description="Accept the retrieved results or retry retrieval."
    )


def evaluate_retrieval(query: str, products: list[dict]) -> RetrievalEvaluation:
    if not products:
        return RetrievalEvaluation(
            relevant=False,
            score=0,
            reasoning="No products were retrieved.",
            decision="retry",
        )

    response = client.responses.parse(
        model="gpt-5-mini",
        instructions="""
        You are a retrieval evaluation agent for a fashion store.

        Your task is to evaluate whether retrieved products satisfy
        the customer's query.

        Evaluation criteria:

        1. Check whether products match the requested product type.
        2. Check explicit constraints such as color, fabric, gender,
           size, season, and price.
        3. Prioritize explicit customer requirements over general
           semantic similarity.
        4. Do not assume product attributes that are not provided.

        Scoring:
        - 0: Completely irrelevant.
        - 1: Very poor relevance.
        - 2: Partially relevant, but important requirements are missing.
        - 3: Moderately relevant.
        - 4: Highly relevant, with minor limitations.
        - 5: Fully satisfies the customer's requirements.

        Decision:
        - accept: Results sufficiently satisfy the query.
        - retry: Results are irrelevant or insufficient.

        Return an evaluation using the provided structured output schema.
        """,
        input=f"""
        Customer query:
        {query}

        Retrieved products:
        {products}
        """,
        text_format=RetrievalEvaluation,
    )
    return response.output_parsed
