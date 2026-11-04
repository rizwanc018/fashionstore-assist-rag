def extract_product_ids(results, strategy: str) -> list[str]:

    if strategy in ("dense", "bm25", "hybrid"):
        return [obj.properties["product_id"] for obj in results]

    if strategy == "hybrid_reranking":
        return [item["product"].properties["product_id"] for item in results]

    raise ValueError(f"Unknown retrieval strategy: {strategy}")
