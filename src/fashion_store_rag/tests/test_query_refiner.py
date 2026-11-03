from unittest.mock import patch

from fashion_store_rag.agent.evaluator import RetrievalEvaluation
from fashion_store_rag.agent.orchestrator import run_agent
from fashion_store_rag.agent.query_refiner import QueryRefinement


def test_empty_refined_query_uses_original_query():

    with (
        patch(
            "fashion_store_rag.agent.orchestrator.route_query",
            return_value="search_products",
        ),
        patch(
            "fashion_store_rag.agent.orchestrator.search_products_tool",
            return_value=[],
        ) as mock_search,
        patch(
            "fashion_store_rag.agent.orchestrator.evaluate_retrieval",
        ) as mock_evaluator,
        patch(
            "fashion_store_rag.agent.orchestrator.refine_query",
        ) as mock_refiner,
    ):
        mock_evaluator.side_effect = [
            RetrievalEvaluation(
                relevant=False,
                score=1,
                reasoning="Insufficient results.",
                decision="retry",
            ),
            RetrievalEvaluation(
                relevant=False,
                score=1,
                reasoning="Still insufficient.",
                decision="retry",
            ),
        ]

        mock_refiner.return_value = QueryRefinement(
            refined_query="   ",
            reasoning="Empty refinement for testing.",
        )

        result = run_agent("Show me blue jeans")

        assert result["attempts"] == 2
        assert result["evaluation"]["decision"] == "retry"

        # Both retrieval attempts should use the original query.
        assert mock_search.call_args_list[0].kwargs["query"] == "Show me blue jeans"
        assert mock_search.call_args_list[1].kwargs["query"] == "Show me blue jeans"

        assert mock_refiner.call_count == 1

        print("Test passed!")


if __name__ == "__main__":
    test_empty_refined_query_uses_original_query()
