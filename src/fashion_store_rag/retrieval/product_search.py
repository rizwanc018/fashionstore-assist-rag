import time
from concurrent.futures import ThreadPoolExecutor

from fashion_store_rag.database.client import get_weaviate_client
from fashion_store_rag.query_understanding.metadata_extractor import ProductMetadata
from fashion_store_rag.retrieval.fusion import reciprocal_rank_fusion
from fashion_store_rag.retrieval.metadata_filters import build_metadata_filters
from fashion_store_rag.utils.timig import timed_search


def search_products(
    query: str, metadata: ProductMetadata | None = None, limit: int = 5
):

    metadata_filter = build_metadata_filters(metadata) if metadata is not None else None

    with get_weaviate_client() as client:
        collection = client.collections.get("Products")

        response = collection.query.near_text(
            query=query,
            filters=metadata_filter,
            limit=limit,
        )

        return response.objects


def search_products_bm25(
    query: str, metadata: ProductMetadata | None = None, limit: int = 5
):
    metadata_filter = build_metadata_filters(metadata) if metadata is not None else None

    with get_weaviate_client() as client:
        collection = client.collections.get("Products")

        response = collection.query.bm25(
            query=query,
            query_properties=["searchable_text"],
            filters=metadata_filter,
            limit=limit,
        )
        return response.objects


def search_products_hybrid(
    query: str,
    limit: int = 5,
    retrieval_limit: int = 10,
    metadata: ProductMetadata | None = None,
    timings: dict | None = None,
):

    total_start = time.perf_counter()

    with ThreadPoolExecutor(max_workers=2) as executor:
        dense_future = executor.submit(
            timed_search,
            search_products,
            query=query,
            limit=retrieval_limit,
            metadata=metadata,
        )

        bm25_future = executor.submit(
            timed_search,
            search_products_bm25,
            query=query,
            limit=retrieval_limit,
            metadata=metadata,
        )

        dense_results, dense_ms = dense_future.result()
        bm25_results, bm25_ms = bm25_future.result()

        fusion_start = time.perf_counter()

        fused_results = reciprocal_rank_fusion(
            result_lists=[
                dense_results,
                bm25_results,
            ],
            k=60,
            limit=limit,
        )

        fusion_ms = (time.perf_counter() - fusion_start) * 1000
        retrieval_ms = (time.perf_counter() - total_start) * 1000

        if timings is not None:
            timings["dense_search_ms"] = round(dense_ms, 2)
            timings["bm25_search_ms"] = round(bm25_ms, 2)
            timings["fusion_ms"] = round(fusion_ms, 2)
            timings["retrieval_ms"] = round(retrieval_ms, 2)

        return fused_results
