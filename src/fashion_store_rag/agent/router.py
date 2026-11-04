from typing import Literal

from fashion_store_rag.query_understanding.query_classifier import classify_query

Route = Literal[
    "search_products",
    "get_product_details",
    "compare_products",
    "search_faqs",
    "out_of_scope",
]

ROUTE_MAPPING: dict[str, Route] = {
    "product_search": "search_products",
    "product_question": "get_product_details",
    "product_comparison": "compare_products",
    "faq": "search_faqs",
    "out_of_scope": "out_of_scope",
}


def route_query(query: str, timings: dict | None = None) -> Route:
    classification = classify_query(query, timings=timings)
    return ROUTE_MAPPING[classification.intent]
