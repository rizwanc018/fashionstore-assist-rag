from unittest.mock import patch

from fashion_store_rag.agent.evaluator import RetrievalEvaluation
from fashion_store_rag.agent.orchestrator import run_agent
from fashion_store_rag.agent.query_refiner import QueryRefinement

with (
    patch("fashion_store_rag.agent.orchestrator.evaluate_retrieval") as mock_evaluator,
    patch("fashion_store_rag.agent.orchestrator.refine_query") as mock_refiner,
):
    mock_evaluator.side_effect = [
        RetrievalEvaluation(
            relevant=False,
            score=1,
            reasoning="Results are not sufficiently relevant.",
            decision="retry",
        ),
        RetrievalEvaluation(
            relevant=True,
            score=5,
            reasoning="Relevant products found.",
            decision="accept",
        ),
    ]

    mock_refiner.return_value = QueryRefinement(
        refined_query="Blue denim jeans",
        reasoning="Clarified the requested product type and color.",
    )

    result = run_agent("Show me blue jeans")

    print("Attempts:", result["attempts"])
    print("Refiner calls:", mock_refiner.call_count)
    print("Evaluation:", result["evaluation"])
    print("Answer:", result["answer"])
