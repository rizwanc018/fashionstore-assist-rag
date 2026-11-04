from fashion_store_rag.query_understanding.metadata_extractor import extract_metadata
from fashion_store_rag.retrieval.product_search import search_products_hybrid
from fashion_store_rag.retrieval.reranker import rerank_products


def retrieve_products(query: str, limit: int = 5, retrieval_limit: int = 5):
    # Extract metadata from original query
    metadata = extract_metadata(query)

    # Perform hybrid retrieval
    candidates = search_products_hybrid(
        query=query,
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
        "metadata": metadata.model_dump(exclude_none=True),
        "products": reranked_products,
    }
