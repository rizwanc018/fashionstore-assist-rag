import time

from fashion_store_rag.query_understanding.metadata_extractor import extract_metadata
from fashion_store_rag.retrieval.product_search import search_products_hybrid
from fashion_store_rag.retrieval.reranker import rerank_products


def retrieve_products(
    query: str,
    limit: int = 5,
    retrieval_limit: int = 5,
    timings: dict | None = None,
):
    extract_metadata_start = time.perf_counter()

    metadata = extract_metadata(query)

    extract_metadata_ms = (time.perf_counter() - extract_metadata_start) * 1000
    timings["extract_metadata_ms"] = round(extract_metadata_ms, 2)

    candidates = search_products_hybrid(
        query=query,
        metadata=metadata,
        limit=retrieval_limit,
        retrieval_limit=retrieval_limit,
        timings=timings,
    )

    rerank_start = time.perf_counter()
    reranked_products = rerank_products(
        query=query,
        products=candidates,
        limit=limit,
    )
    reranking_ms = (time.perf_counter() - rerank_start) * 1000
    timings["reranking_ms"] = round(reranking_ms, 2)

    return {
        "metadata": metadata.model_dump(exclude_none=True),
        "products": reranked_products,
    }
