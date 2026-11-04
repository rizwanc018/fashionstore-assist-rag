import time

from fashion_store_rag.agent.orchestrator import run_agent


def main():

    questions = [
        "Show me comfortable cotton clothes for summer.",
        "Do you have black casual t-shirts for women?",
        # "Which products are available for winter?",
        # "What is your return policy?"
    ]

    for question in questions:
        start = time.perf_counter()
        print(f"\nQuestion: {question}")
        timings = {}
        answer = run_agent(question, timings=timings)

        print(f"Answer: {answer}")
        print("\n--- Performance Metrics ---")

        for stage, duration in timings.items():
            print(f"{stage}: {duration:.2f} ms")

        total_ms = (time.perf_counter() - start) * 1000
        print(f"Total pipeline: {total_ms:.2f} ms")


if __name__ == "__main__":
    main()
