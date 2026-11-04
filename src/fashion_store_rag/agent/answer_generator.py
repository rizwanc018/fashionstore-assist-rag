import time

from fashion_store_rag.services.llm import client


def generate_agent_answer(query: str, context, timings: dict | None = None) -> str:
    start = time.perf_counter()

    response = client.responses.create(
        model="gpt-5-mini",
        instructions="""
        You are a helpful and professional fashion store assistant.

        Your responsibility is to answer customer questions
        accurately using only the information provided in
        the retrieved context.

        Follow these rules:

        1. Use only the supplied context to answer questions.
        2. Never invent product attributes, prices, sizes,
           availability, return policies, or other store policies.
        3. If the context does not contain enough information,
           politely explain that you cannot provide a
           reliable answer.
        4. If only part of the question can be answered,
           answer the available parts and clearly mention
           what information is missing.
        5. For product comparisons, compare only attributes
           explicitly available in the context.
        6. Keep responses concise, friendly, and easy to understand.
        7. Do not mention internal implementation details,
           retrieval systems, or the supplied context.
        """,
        input=f"""
        Customer question:
        {query}

        Retrieved information:
        {context}
        """,
    )

    elapsed_ms = (time.perf_counter() - start) * 1000

    if timings is not None:
        timings["llm_generation_ms"] = round(elapsed_ms, 2)

    return response.output_text
