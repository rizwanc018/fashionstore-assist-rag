from fashion_store_rag.prompts.answer_generation import (
    build_rag_prompt,
    format_retrieved_products,
)
from fashion_store_rag.retrieval.product_search import search_products
from fashion_store_rag.services.llm import generate_answer


def answer_question(query: str, limit: int = 5) -> str:
    # 1. Retrieve relevant product details
    products = search_products(query)
    if not products:
        return "I couldn't find any matching products."

    # 2. Format retrieved products
    context = format_retrieved_products(products.objects)

    # 3. Build RAG prompt
    prompt = build_rag_prompt(
        query=query,
        context=context,
    )
    return generate_answer(prompt)
