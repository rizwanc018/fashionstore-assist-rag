import bm25s

from fashion_store_rag.ingestion.faq import build_faq_index


def search_faqs(query: str, limit: int = 3) -> list[dict]:
    retriever, faqs = build_faq_index()

    query_tokens = bm25s.tokenize(query, stopwords="en")

    results, scores = retriever.retrieve(query_tokens, k=limit)

    return [
        {
            "faq": faqs[int(index)],
            "score": float(score),
        }
        for index, score in zip(results[0], scores[0])
    ]
