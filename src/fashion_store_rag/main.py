from fashion_store_rag.agent.orchestrator import run_agent


def main():
    questions = [
        # "Show me comfortable cotton clothes for summer.",
        "Do you have black casual t-shirts for women?",
        # "Which products are available for winter?",
        # "What is your return policy?"
    ]

    for question in questions:
        print(f"\nQuestion: {question}")

        answer = run_agent(question)

        print(f"Answer: {answer}")


if __name__ == "__main__":
    main()
