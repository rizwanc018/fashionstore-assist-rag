from fashion_store_rag.services.rag import answer_question


def main():
    questions = [
        "Show me comfortable cotton clothes for summer.",
        "Do you have black casual t-shirts for women?",
        "Which products are available for winter?",
    ]

    for question in questions:
        print(f"\nQuestion: {question}")

        answer = answer_question(question)

        print(f"Answer: {answer}")


if __name__ == "__main__":
    main()
