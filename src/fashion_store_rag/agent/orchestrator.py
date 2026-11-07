import logging

from weaviate.exceptions import WeaviateBaseError

from fashion_store_rag.agent.answer_generator import generate_agent_answer
from fashion_store_rag.agent.evaluator import evaluate_retrieval
from fashion_store_rag.agent.query_refiner import refine_query
from fashion_store_rag.agent.router import route_query
from fashion_store_rag.agent.tools import (
    compare_products_tool,
    get_product_details_tool,
    search_faqs_tool,
    search_products_tool,
)

logger = logging.getLogger(__name__)


def execute_tool(route: str, query: str, **kwargs):
    # if route == "search_products":
    #     return search_products_tool(query)

    logger.info("Executing tool for route: %s", route)

    if route == "search_faqs":
        return search_faqs_tool(query)

    if route == "get_product_details":
        product_id = kwargs.get("product_id")

        if not product_id:
            logger.warning("get_product_details called without a product_id")
            return {"message": "A product ID is required to retrieve product details."}

        logger.info("Fetching product details for product_id: %s", product_id)
        return get_product_details_tool(product_id)

    if route == "compare_products":
        product_ids = kwargs.get("product_ids", [])

        if len(product_ids) < 2:
            logger.warning(
                "compare_products called with %d product id(s); need at least 2",
                len(product_ids),
            )
            return {"message": "At least two product IDs are required for comparison."}

        logger.info("Comparing products: %s", product_ids)
        return compare_products_tool(product_ids)

    if route == "out_of_scope":
        logger.info("Query classified as out of scope")
        return {"message": "This question is outside the fashion store scope."}

    logger.error("Unknown route encountered: %s", route)
    raise ValueError(f"Unknown route: {route}")


def run_agent(query: str, timings: dict | None = None, **kwargs):

    logger.info("Running agent for query: %r", query)

    route = route_query(query, timings=timings)
    logger.info("Query routed to: %s", route)

    if route != "search_products":
        tool_result = execute_tool(route=route, query=query, **kwargs)
        logger.info("Executed tool for route %s; generating answer", route)

        answer = generate_agent_answer(
            query=query, context=tool_result, timings=timings
        )

        return {
            "route": route,
            "tool_result": tool_result,
            "evaluation": None,
            "attempts": 1,
            "answer": answer,
        }

    max_attempts = 2
    evaluation = None
    tool_result = []
    search_query = query

    for attempt in range(max_attempts):
        retrieval_limit = 5 if attempt == 0 else 15
        logger.info(
            "Product search attempt %d/%d (limit=%d) for query: %r",
            attempt + 1,
            max_attempts,
            retrieval_limit,
            search_query,
        )

        try:
            tool_result = search_products_tool(
                query=search_query, retrieval_limit=retrieval_limit, timings=timings
            )
        except WeaviateBaseError as error:
            logger.error("Retrieval failed: %s", error)
            tool_result = []

        logger.info("Retrieved %d product(s)", len(tool_result))

        evaluation = evaluate_retrieval(
            query=query, products=tool_result, timings=timings
        )

        if evaluation is None:
            raise RuntimeError("Retrieval evaluation was not performed.")

        logger.info("Retrieval evaluation decision: %s", evaluation.decision)

        if evaluation.decision == "accept":
            break

        if attempt < max_attempts - 1:
            refinement = refine_query(
                query=query, evaluation=evaluation, timings=timings
            )
            refined_query = refinement.refined_query.strip()

            if refined_query:
                logger.info("Refined query to: %r", refined_query)
                search_query = refined_query
            else:
                logger.info("Refinement empty; reusing original query")
                search_query = query

    if evaluation.decision == "accept":
        logger.info("Generating answer from %d accepted product(s)", len(tool_result))
        answer = generate_agent_answer(
            query=query, context=tool_result, timings=timings
        )
    else:
        logger.info("No acceptable products found after %d attempt(s)", attempt + 1)
        answer = (
            "I couldn't find sufficiently relevant products "
            "for your request. Could you try different search "
            "criteria?"
        )

    return {
        "route": route,
        "tool_result": tool_result,
        "evaluation": evaluation.model_dump(),
        "attempts": attempt + 1,
        "answer": answer,
    }
