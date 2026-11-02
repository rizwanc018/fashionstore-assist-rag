from fashion_store_rag.database.client import get_weaviate_client
from fashion_store_rag.query_understanding.metadata_extractor import ProductMetadata
from fashion_store_rag.retrieval.metadata_filters import build_metadata_filters


def search_products(
    query: str, metadata: ProductMetadata | None = None, limit: int = 5
):

    with get_weaviate_client() as client:
        collection = client.collections.get("Products")

        response = collection.query.near_text(query=query, limit=limit)

        return response


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

        return response
