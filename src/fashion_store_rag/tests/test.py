from fashion_store_rag.agent.orchestrator import run_agent

queries = [
    "Show me blue jeans",
    "What is your return policy?",
    "Explain quantum physics",
]

for query in queries:
    result = run_agent(query)
    print(f"\nQuery: {query}")
    print(f"Route: {result['route']}")
    print(f"Answer: {result['answer']}")
