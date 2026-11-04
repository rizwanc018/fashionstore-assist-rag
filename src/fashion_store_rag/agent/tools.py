from fashion_store_rag.ingestion.products import load_products
from fashion_store_rag.retrieval.faq_search import search_faqs
from fashion_store_rag.retrieval.retrieval_pipeline import retrieve_products


def search_faqs_tool(query: str, limit: int = 3) -> list[dict]:
    results = search_faqs(query, limit)

    return [
        {
            "faq_id": result["faq"]["faq_id"],
            "question": result["faq"]["question"],
            "answer": result["faq"]["answer"],
            "category": result["faq"]["category"],
            "score": result["score"],
        }
        for result in results
    ]


def search_products_tool(
    query: str,
    limit: int = 5,
    retrieval_limit: int = 5,
    timings: dict | None = None,
) -> list[dict]:
    result = retrieve_products(
        query=query, limit=limit, retrieval_limit=retrieval_limit, timings=timings
    )

    return [
        {
            "product_id": item["product"].properties["product_id"],
            "name": item["product"].properties["name"],
            "category": item["product"].properties["category"],
            "sub_category": item["product"].properties["sub_category"],
            "color": item["product"].properties["color"],
            "fabric": item["product"].properties["fabric"],
            "price": item["product"].properties["price"],
            "usage": item["product"].properties["usage"],
            "gender": item["product"].properties["gender"],
            "season": item["product"].properties["season"],
            "sizes": item["product"].properties["sizes"],
            "score": item["score"],
        }
        for item in result["products"]
    ]


def get_product_details_tool(product_id: str):
    products = load_products()

    for product in products:
        if product["product_id"] == product_id:
            return product

    return None


def compare_products_tool(product_ids: list[str]) -> list[dict]:
    products = []

    for product_id in product_ids:
        product = get_product_details_tool(product_id)

        if product is not None:
            products.append(product)

    return products
