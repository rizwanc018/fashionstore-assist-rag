from fashion_store_rag.query_understanding.metadata_extractor import extract_metadata
from fashion_store_rag.query_understanding.query_rewriter import rewrite_query
from fashion_store_rag.retrieval.product_search import search_products_hybrid
from fashion_store_rag.retrieval.reranker import rerank_products


def retrieve_products(query: str, limit: int = 5, retrieval_limit: int = 5):
    intent = None

    # # Classify customer query
    # classification = classify_query(query)
    # intent = classification.intent

    # # Handle non-product queries
    # if intent == "faq":
    #     return {
    #         "intent": intent,
    #         "products": [],
    #         "message": "This query should be handled by FAQ retrieval.",
    #     }

    # if intent == "out_of_scope":
    #     return {
    #         "intent": intent,
    #         "products": [],
    #         "message": "This query is outside the fashion store scope.",
    #     }

    # Rewrite query for retrieval
    rewritten_query = rewrite_query(query).rewritten_query

    # Extract metadata from original query
    metadata = extract_metadata(query)

    # Perform hybrid retrieval
    candidates = search_products_hybrid(
        query=rewritten_query,
        metadata=metadata,
        limit=retrieval_limit,
        retrieval_limit=retrieval_limit,
    )

    # 6. Rerank using the original customer query
    reranked_products = rerank_products(
        query=query,
        products=candidates,
        limit=limit,
    )

    return {
        "intent": intent or "search_products",
        "rewritten_query": rewritten_query,
        "metadata": metadata.model_dump(exclude_none=True),
        "products": reranked_products,
    }
