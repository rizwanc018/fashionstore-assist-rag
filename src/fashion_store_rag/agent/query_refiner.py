import time

from pydantic import BaseModel, Field

from fashion_store_rag.agent.evaluator import RetrievalEvaluation
from fashion_store_rag.services.llm import client


class QueryRefinement(BaseModel):
    refined_query: str = Field(
        description="An improved search query that addresses the retrieval failure."
    )

    reasoning: str = Field(description="Explanation of what was changed and why.")


def refine_query(
    query: str, evaluation: RetrievalEvaluation, timings: dict | None = None
) -> QueryRefinement:
    start = time.perf_counter()
    print("Refining query")
    response = client.responses.parse(
        model="gpt-5-mini",
        instructions="""
        You are a search query refinement agent for a fashion store.

        Your task is to improve a customer's search query when
        the previous retrieval attempt returned irrelevant
        or insufficient products.

        Guidelines:
        - Preserve the customer's original intent.
        - Preserve explicit constraints such as color, fabric,
          gender, size, season, and price.
        - Use the evaluator's reasoning to identify what went wrong.
        - Make the query clearer and more specific when appropriate.
        - Do not invent new customer preferences.
        - Do not change the requested product type.
        - Return a concise search query.
        """,
        input=f"""
        Original customer query:
        {query}

        Retrieval evaluation:
        {evaluation.model_dump()}
        """,
        text_format=QueryRefinement,
    )

    elapsed_ms = (time.perf_counter() - start) * 1000

    if timings is not None:
        timings["refine_query_ms"] = round(elapsed_ms, 2)

    return response.output_parsed
