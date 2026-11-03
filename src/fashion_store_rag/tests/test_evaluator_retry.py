from unittest.mock import patch

from fashion_store_rag.agent.evaluator import RetrievalEvaluation
from fashion_store_rag.agent.orchestrator import run_agent

with patch("fashion_store_rag.agent.orchestrator.evaluate_retrieval") as mock_evaluator:
    mock_evaluator.side_effect = [
        RetrievalEvaluation(
            relevant=False,
            score=1,
            reasoning="Insufficient results.",
            decision="unknown",
        ),
        RetrievalEvaluation(
            relevant=False,
            score=1,
            reasoning="Insufficient results.",
            decision="unknown",
        ),
    ]

    # mock_evaluator.side_effect = [
    #     RetrievalEvaluation(
    #         relevant=False,
    #         score=1,
    #         reasoning="Insufficient results.",
    #         decision="retry",
    #     ),
    #     RetrievalEvaluation(
    #         relevant=False,
    #         score=1,
    #         reasoning="Insufficient results.",
    #         decision="retry",
    #     ),
    # ]

    result = run_agent("Show me blue jeans")

    print("Attempts:", result["attempts"])
    print("Evaluation:", result["evaluation"])
    print("Answer:", result["answer"])
