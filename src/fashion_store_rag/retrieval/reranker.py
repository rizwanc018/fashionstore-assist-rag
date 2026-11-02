from sentence_transformers import CrossEncoder

MODEL_NAME = "BAAI/bge-reranker-base"

reranker = CrossEncoder(MODEL_NAME)


def rerank_products(query: str, products: list, limit: int = 5):
    if not products:
        return []

    pairs = [(query, product.properties["searchable_text"]) for product in products]
    scores = reranker.predict(pairs)

    ranked_products = sorted(
        zip(products, scores), key=lambda item: item[1], reverse=True
    )

    return [
        {
            "product": product,
            "score": float(score),
        }
        for product, score in ranked_products[:limit]
    ]
