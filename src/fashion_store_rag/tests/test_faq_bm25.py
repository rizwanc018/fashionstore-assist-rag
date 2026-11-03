from fashion_store_rag.retrieval.faq_search import search_faqs

test_queries = [
    "How long do I have to return an item?",
    # "When will my refund arrive?",
    # "Is shipping free?",
    # "Can I pay using UPI?",
    # "How can I track my order?",
]

for query in test_queries:
    print(f"\nQUERY: {query}")

    results = search_faqs(query, limit=3)

    for result in results:
        faq = result["faq"]
        print(
            faq["faq_id"],
            "|",
            faq["question"],
            "| Score:",
            round(result["score"], 4),
        )
