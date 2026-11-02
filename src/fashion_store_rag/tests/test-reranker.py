from fashion_store_rag.retrieval.product_search import (
    search_products_hybrid,
)
from fashion_store_rag.retrieval.reranker import rerank_products

query = "black cotton T-shirts for men"
print("Query: ", query)
products = search_products_hybrid(
    query=query,
    limit=10,
    retrieval_limit=10,
)
print("Hybrid")
for rank, product in enumerate(products, start=1):
    print(f"{rank}. {product.properties['name']}")

reranked = rerank_products(
    query=query,
    products=products,
    limit=5,
)
print("\nReranked")
for rank, result in enumerate(reranked, start=1):
    product = result["product"]
    print(f"\n{rank}. {product.properties['name']}")
    print(f"Score: {result['score']:.4f}")
