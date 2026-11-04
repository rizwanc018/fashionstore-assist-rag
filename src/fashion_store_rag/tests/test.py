from fashion_store_rag.evaluation.benchmark import extract_product_ids
from fashion_store_rag.query_understanding.metadata_extractor import extract_metadata
from fashion_store_rag.retrieval.product_search import (
    search_products,
    search_products_bm25,
    search_products_hybrid,
)
from fashion_store_rag.retrieval.reranker import rerank_products

query = "Show me blue jeans"
metadata = extract_metadata(query)

# 1. Dense retrieval
dense_results = search_products(
    query=query,
    metadata=metadata,
    limit=5,
)

# 2. BM25 retrieval
bm25_results = search_products_bm25(
    query=query,
    metadata=metadata,
    limit=5,
)

# 3. Hybrid retrieval — retrieve 15 candidates
hybrid_candidates = search_products_hybrid(
    query=query,
    metadata=metadata,
    limit=15,
    retrieval_limit=15,
)

# 4. Hybrid + reranking — rerank those same 15 candidates
reranked_results = rerank_products(
    query=query,
    products=hybrid_candidates,
    limit=5,
)


print("Dense:", extract_product_ids(dense_results, "dense"))
print("BM25:", extract_product_ids(bm25_results, "bm25"))
print("Hybrid:", extract_product_ids(hybrid_candidates[:5], "hybrid"))
print("Hybrid + Reranking:", extract_product_ids(reranked_results, "hybrid_reranking"))
