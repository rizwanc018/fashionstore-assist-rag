from fashion_store_rag.database.client import get_weaviate_client
from fashion_store_rag.query_understanding.metadata_extractor import ProductMetadata
from fashion_store_rag.retrieval.fusion import reciprocal_rank_fusion
from fashion_store_rag.retrieval.metadata_filters import build_metadata_filters


def search_products(query: str, limit: int = 5):

    with get_weaviate_client() as client:
        collection = client.collections.get("Products")

        response = collection.query.near_text(query=query, limit=limit)

        return response.objects


def search_products_with_filters(
    query: str,
    metadata: ProductMetadata,
    limit: int = 5,
):
    metadata_filter = build_metadata_filters(metadata)

    with get_weaviate_client() as client:
        collection = client.collections.get("Products")

        if metadata_filter is None:
            response = collection.query.near_text(
                query=query,
                limit=limit,
            )
        else:
            response = collection.query.near_text(
                query=query,
                filters=metadata_filter,
                limit=limit,
            )

        return response.objects


def search_products_bm25(query: str, limit: int = 5):
    with get_weaviate_client() as client:
        collection = client.collections.get("Products")

        response = collection.query.bm25(
            query=query, query_properties=["searchable_text"], limit=5
        )
        return response.objects


def search_products_hybrid(
    query: str,
    limit: int = 5,
    retrieval_limit: int = 10,
):
    dense_results = search_products(
        query=query,
        limit=retrieval_limit,
    )

    bm25_results = search_products_bm25(
        query=query,
        limit=retrieval_limit,
    )

    fused_results = reciprocal_rank_fusion(
        result_lists=[
            dense_results,
            bm25_results,
        ],
        k=60,
        limit=limit,
    )

    return fused_results
