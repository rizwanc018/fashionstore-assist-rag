def reciprocal_rank_fusion(result_lists: list, k: int = 60, limit: int = 5):
    scores = {}
    products = {}

    for results in result_lists:
        for rank, product in enumerate(results, start=1):
            product_id = product.properties["product_id"]

            rrf_score = 1 / (k + rank)

            scores[product_id] = scores.get(product_id, 0) + rrf_score
            products[product_id] = product

    ranked_ids = sorted(scores, key=lambda product_id: scores[product_id], reverse=True)

    return [products[product_id] for product_id in ranked_ids[:limit]]
