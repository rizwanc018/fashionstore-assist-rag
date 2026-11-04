def precision_at_k(retrieved_ids: list[str], relevant_ids: list[str], k: int) -> float:

    if k <= 0:
        raise ValueError("k must be greater than zero")

    if not retrieved_ids:
        return 0.0

    retrieved_at_k = retrieved_ids[:k]

    relevent_count = sum(
        1 for product_id in retrieved_at_k if product_id in relevant_ids
    )

    return relevent_count / k


def recall_at_k(retrieved_ids: list[str], relevant_ids: list[str], k: int) -> float:

    if k <= 0:
        raise ValueError("k must be greater than zero")

    if not relevant_ids:
        return 0.0

    retrieved_at_k = retrieved_ids[:k]

    relevant_count = sum(
        1 for product_id in retrieved_at_k if product_id in relevant_ids
    )

    return relevant_count / len(relevant_ids)


def reciprocal_rank(retrieved_ids: list[str], relevant_ids: list[str]) -> float:
    for rank, product_id in enumerate(retrieved_ids, start=1):
        if product_id in relevant_ids:
            return 1 / rank
    return 0.0


def mean_reciprocal_rank(
    results: list[list[str]], relevant_ids_list: list[list[str]]
) -> float:
    if len(results) != len(relevant_ids_list):
        raise ValueError("Results and relevant IDs must have the same length")

    if not results:
        return 0.0

    reciprocal_ranks = [
        reciprocal_rank(retrieved_ids, relevant_ids)
        for retrieved_ids, relevant_ids in zip(results, relevant_ids_list)
    ]

    print(reciprocal_ranks)

    return sum(reciprocal_ranks) / len(reciprocal_ranks)
