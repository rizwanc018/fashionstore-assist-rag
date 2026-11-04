from fashion_store_rag.evaluation.dataset import load_evaluation_dataset
from fashion_store_rag.evaluation.metrics import (
    precision_at_k,
    recall_at_k,
    reciprocal_rank,
)
from fashion_store_rag.query_understanding.metadata_extractor import (
    extract_metadata,
)
from fashion_store_rag.retrieval.product_search import (
    search_products,
    search_products_bm25,
    search_products_hybrid,
)
from fashion_store_rag.retrieval.reranker import rerank_products


def extract_product_ids(results: list) -> list[str]:
    """Extract product IDs from Weaviate objects or reranker dictionaries."""
    product_ids = []

    for item in results:
        if isinstance(item, dict):
            product = item.get("product")

            if product is not None:
                product_ids.append(product.properties["product_id"])
            elif "product_id" in item:
                product_ids.append(item["product_id"])
        else:
            product_ids.append(item.properties["product_id"])

    return product_ids


def run_benchmark(k: int = 5, candidate_limit: int = 15) -> dict:
    dataset = load_evaluation_dataset()

    strategies = {
        "Dense": [],
        "BM25": [],
        "Hybrid": [],
        "Hybrid + Reranking": [],
    }

    relevant_ids_list = []
    per_query_results = []

    for index, item in enumerate(dataset, start=1):
        query = item["query"]
        relevant_ids = item["relevant_product_ids"]

        print(f"\nEvaluating query {index}/{len(dataset)}: {query}")

        # Extract metadata once and reuse it across strategies.
        metadata = extract_metadata(query)

        # 1. Dense retrieval
        dense_results = search_products(
            query=query,
            metadata=metadata,
            limit=k,
        )

        # 2. BM25 retrieval
        bm25_results = search_products_bm25(
            query=query,
            metadata=metadata,
            limit=k,
        )

        # 3. Hybrid retrieval
        hybrid_candidates = search_products_hybrid(
            query=query,
            metadata=metadata,
            limit=candidate_limit,
            retrieval_limit=candidate_limit,
        )

        hybrid_results = hybrid_candidates[:k]

        # 4. Hybrid + Reranking
        reranked_results = rerank_products(
            query=query,
            products=hybrid_candidates,
            limit=k,
        )

        # Extract product IDs
        retrieved_by_strategy = {
            "Dense": extract_product_ids(dense_results),
            "BM25": extract_product_ids(bm25_results),
            "Hybrid": extract_product_ids(hybrid_results),
            "Hybrid + Reranking": extract_product_ids(reranked_results),
        }

        # Store results for aggregate calculations.
        for strategy, retrieved_ids in retrieved_by_strategy.items():
            strategies[strategy].append(retrieved_ids)

        relevant_ids_list.append(relevant_ids)

        # Calculate individual query metrics.
        query_result = {
            "query": query,
            "relevant_product_ids": relevant_ids,
            "strategies": {},
        }

        for strategy, retrieved_ids in retrieved_by_strategy.items():
            query_result["strategies"][strategy] = {
                "retrieved_product_ids": retrieved_ids,
                f"Precision@{k}": precision_at_k(retrieved_ids, relevant_ids, k),
                f"Recall@{k}": recall_at_k(retrieved_ids, relevant_ids, k),
                "RR": reciprocal_rank(retrieved_ids[:k], relevant_ids),
            }

        per_query_results.append(query_result)

    # Calculate aggregate metrics.
    benchmark_summary = {}

    for strategy, results in strategies.items():
        precision_scores = [
            precision_at_k(ids, relevant, k)
            for ids, relevant in zip(results, relevant_ids_list)
        ]

        recall_scores = [
            recall_at_k(ids, relevant, k)
            for ids, relevant in zip(results, relevant_ids_list)
        ]

        reciprocal_ranks = [
            reciprocal_rank(ids[:k], relevant)
            for ids, relevant in zip(results, relevant_ids_list)
        ]

        benchmark_summary[strategy] = {
            f"Precision@{k}": (
                sum(precision_scores) / len(precision_scores)
                if precision_scores
                else 0.0
            ),
            f"Recall@{k}": (
                sum(recall_scores) / len(recall_scores) if recall_scores else 0.0
            ),
            f"MRR@{k}": (
                sum(reciprocal_ranks) / len(reciprocal_ranks)
                if reciprocal_ranks
                else 0.0
            ),
        }

    return {
        "summary": benchmark_summary,
        "per_query": per_query_results,
    }
