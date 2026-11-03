from fashion_store_rag.agent.answer_generator import generate_agent_answer
from fashion_store_rag.agent.router import route_query
from fashion_store_rag.agent.tools import (
    compare_products_tool,
    get_product_details_tool,
    search_faqs_tool,
    search_products_tool,
)


def execute_tool(route: str, query: str, **kwargs):
    if route == "search_products":
        return search_products_tool(query)

    if route == "search_faqs":
        return search_faqs_tool(query)

    if route == "get_product_details":
        product_id = kwargs.get("product_id")

        if not product_id:
            return {"message": "A product ID is required to retrieve product details."}

        return get_product_details_tool(product_id)

    if route == "compare_products":
        product_ids = kwargs.get("product_ids", [])

        if len(product_ids) < 2:
            return {"message": "At least two product IDs are required for comparison."}

        return compare_products_tool(product_ids)

    if route == "out_of_scope":
        return {"message": "This question is outside the fashion store scope."}

    raise ValueError(f"Unknown route: {route}")


def run_agent(query: str, **kwargs):
    route = route_query(query)

    tool_result = execute_tool(
        route=route,
        query=query,
        **kwargs,
    )

    answer = generate_agent_answer(query=query, context=tool_result)

    return {"route": route, "tool_result": tool_result, "answer": answer}
