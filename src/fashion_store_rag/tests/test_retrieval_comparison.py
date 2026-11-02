from fashion_store_rag.query_understanding.metadata_extractor import extract_metadata
from fashion_store_rag.retrieval.fusion import reciprocal_rank_fusion
from fashion_store_rag.retrieval.product_search import (
    search_products,
    search_products_bm25,
    search_products_with_filters,
)
from fashion_store_rag.retrieval.reranker import rerank_products


def compare_retrievers(query: str, limit: int = 5):
    print(f"\nQuery: {query}")
    print("=" * 60)

    # Dense search
    dense_response = search_products(query, limit=limit)

    print("\nDENSE SEARCH")
    for rank, obj in enumerate(dense_response, start=1):
        print(f"{rank}. {obj.properties['name']}")

    # metadata = extract_metadata(query)
    # metadata_response = search_products_with_filters(
    #     query, metadata=metadata, limit=limit
    # )

    # print("\nMETADATA SEARCH")
    # for rank, obj in enumerate(metadata_response, start=1):
    #     print(f"{rank}. {obj.properties['name']}")

    # BM25 search
    bm25_products = search_products_bm25(query, limit=limit)

    print("\nBM25 SEARCH")
    for rank, obj in enumerate(bm25_products, start=1):
        print(f"{rank}. {obj.properties['name']}")

    fused_results = reciprocal_rank_fusion(
        result_lists=[
            dense_response,
            bm25_products,
        ],
        k=60,
        limit=limit,
    )
    print("\nRRF SEARCH")
    for rank, product in enumerate(fused_results, start=1):
        print(f"{rank}. {product.properties['name']}")

    reranked = rerank_products(
        query=query,
        products=fused_results,
        limit=5,
    )
    print("\nRERANKER SEARCH")
    for rank, result in enumerate(reranked, start=1):
        product = result["product"]
        print(f"{rank}. {product.properties['name']}, Score: {result['score']:.4f} ")


if __name__ == "__main__":
    queries = [
        "black cotton T-shirts for men",
        "comfortable clothes for hot weather",
        "blue jeans",
        # "breathable summer clothing",
    ]

    for query in queries:
        compare_retrievers(query, limit=15)
