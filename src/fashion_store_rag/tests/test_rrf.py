from fashion_store_rag.retrieval.fusion import reciprocal_rank_fusion
from fashion_store_rag.retrieval.product_search import (
    search_products,
    search_products_bm25,
)


def test_rrf(query: str, limit: int = 5):
    print(f"\nQuery: {query}")
    print("=" * 60)

    # Dense search
    dense_response = search_products(query, limit=limit)

    print("\nDENSE SEARCH")
    for rank, obj in enumerate(dense_response, start=1):
        print(f"{rank}. {obj.properties['name']}")

    # BM25 search
    bm25_products = search_products_bm25(query, limit=limit)

    print("\nBM25 SEARCH")
    # print("BM25 count:", len(bm25_products))
    for rank, obj in enumerate(bm25_products, start=1):
        print(f"{rank}. {obj.properties['name']}")

    rrf_products = reciprocal_rank_fusion([dense_response, bm25_products])
    print("\nRRF RESULT")
    for rank, obj in enumerate(rrf_products, start=1):
        print(f"{rank}. {obj.properties['name']}")


if __name__ == "__main__":
    queries = [
        "black cotton T-shirts for men",
        "comfortable clothes for hot weather",
        # "blue jeans",
    ]

    for query in queries:
        test_rrf(query)
