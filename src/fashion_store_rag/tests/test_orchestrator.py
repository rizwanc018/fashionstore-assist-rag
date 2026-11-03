from fashion_store_rag.agent.orchestrator import run_agent

# Product search
print(run_agent("Show me blue jeans"))

# FAQ search
print(run_agent("What is your return policy?"))

# Out of scope
print(run_agent("Explain quantum physics"))
