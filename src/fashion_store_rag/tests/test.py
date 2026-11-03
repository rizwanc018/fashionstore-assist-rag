from fashion_store_rag.agent.orchestrator import run_agent

result = run_agent("Show me blue jeans")

print("Attempts:", result["attempts"])
print("Evaluation:", result["evaluation"])
print("Answer:", result["answer"])
