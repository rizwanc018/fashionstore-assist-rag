from fashion_store_rag.query_understanding.metadata_extractor import extract_metadata
from fashion_store_rag.retrieval.product_search import (
    search_products,
    search_products_bm25,
    search_products_with_filters,
)


def compare_retrievers(query: str, limit: int = 5):
    print(f"\nQuery: {query}")
    print("=" * 60)

    # Dense search
    dense_response = search_products(query, limit=limit)

    print("\nDENSE SEARCH")
    for rank, obj in enumerate(dense_response, start=1):
        print(f"{rank}. {obj.properties['name']}")

    metadata = extract_metadata(query)
    metadata_response = search_products_with_filters(
        query, metadata=metadata, limit=limit
    )

    print("\nMETADATA SEARCH")
    for rank, obj in enumerate(metadata_response, start=1):
        print(f"{rank}. {obj.properties['name']}")

    # BM25 search
    bm25_products = search_products_bm25(query, limit=limit)

    print("\nBM25 SEARCH")
    for rank, obj in enumerate(bm25_products, start=1):
        print(f"{rank}. {obj.properties['name']}")


if __name__ == "__main__":
    queries = [
        "black cotton T-shirts for men",
        "comfortable clothes for hot weather",
        "blue jeans",
        "breathable summer clothing",
    ]

    for query in queries:
        compare_retrievers(query)
