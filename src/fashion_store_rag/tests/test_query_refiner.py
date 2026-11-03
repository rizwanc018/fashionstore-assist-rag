from fashion_store_rag.agent.evaluator import RetrievalEvaluation
from fashion_store_rag.agent.query_refiner import refine_query

evaluation = RetrievalEvaluation(
    relevant=False,
    score=1,
    reasoning="Retrieved products were shirts instead of jeans. The requested color blue was also missing.",
    decision="retry",
)

result = refine_query(
    query="Show me blue jeans",
    evaluation=evaluation,
)

print(result.model_dump())
