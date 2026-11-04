from concurrent.futures import ThreadPoolExecutor

from fashion_store_rag.database.client import get_weaviate_client
from fashion_store_rag.query_understanding.metadata_extractor import ProductMetadata
from fashion_store_rag.retrieval.fusion import reciprocal_rank_fusion
from fashion_store_rag.retrieval.metadata_filters import build_metadata_filters


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
):

    with ThreadPoolExecutor(max_workers=2) as executor:
        dense_future = executor.submit(
            search_products,
            query=query,
            limit=retrieval_limit,
            metadata=metadata,
        )

        bm25_future = executor.submit(
            search_products_bm25,
            query=query,
            limit=retrieval_limit,
            metadata=metadata,
        )

        dense_results = dense_future.result()
        bm25_results = bm25_future.result()

        fused_results = reciprocal_rank_fusion(
            result_lists=[
                dense_results,
                bm25_results,
            ],
            k=60,
            limit=limit,
        )

        return fused_results
