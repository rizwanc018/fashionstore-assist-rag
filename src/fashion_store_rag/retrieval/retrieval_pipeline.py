import logging
import time

from fashion_store_rag.query_understanding.metadata_extractor import extract_metadata
from fashion_store_rag.retrieval.product_search import search_products_hybrid
from fashion_store_rag.retrieval.reranker import rerank_products

logger = logging.getLogger(__name__)


def retrieve_products(
    query: str,
    limit: int = 5,
    retrieval_limit: int = 5,
    timings: dict | None = None,
):
    logger.info(
        "Retrieving products for query=%r (limit=%d, retrieval_limit=%d)",
        query,
        limit,
        retrieval_limit,
    )

    extract_metadata_start = time.perf_counter()

    metadata = extract_metadata(query)

    extract_metadata_ms = (time.perf_counter() - extract_metadata_start) * 1000

    if timings is not None:
        timings["extract_metadata_ms"] = round(extract_metadata_ms, 2)
    logger.info(
        "Extracted metadata in %.2f ms: %s",
        extract_metadata_ms,
        metadata.model_dump(exclude_none=True),
    )

    candidates = search_products_hybrid(
        query=query,
        metadata=metadata,
        limit=retrieval_limit,
        retrieval_limit=retrieval_limit,
        timings=timings,
    )
    logger.info("Hybrid search returned %d candidate(s)", len(candidates))

    rerank_start = time.perf_counter()
    reranked_products = rerank_products(
        query=query,
        products=candidates,
        limit=limit,
    )
    reranking_ms = (time.perf_counter() - rerank_start) * 1000
    if timings is not None:
        timings["reranking_ms"] = round(reranking_ms, 2)
    logger.info(
        "Reranked to %d product(s) in %.2f ms",
        len(reranked_products),
        reranking_ms,
    )

    return {
        "metadata": metadata.model_dump(exclude_none=True),
        "products": reranked_products,
    }
