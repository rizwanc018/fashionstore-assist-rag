import bm25s

from fashion_store_rag.ingestion.faq import load_faq_index


def search_faqs(query: str, limit: int = 3) -> list[dict]:
    retriever, faqs = load_faq_index()

    query_tokens = bm25s.tokenize(query, stopwords="en", show_progress=False)

    results, scores = retriever.retrieve(query_tokens, k=limit, show_progress=False)

    return [
        {
            "faq": faqs[int(index)],
            "score": float(score),
        }
        for index, score in zip(results[0], scores[0])
    ]
