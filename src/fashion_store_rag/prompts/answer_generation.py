from weaviate.collections.classes.internal import Object


def format_retrieved_products(response_objects: list[Object]) -> str:

    if not response_objects:
        return "No relevant products found."

    context = "\n\n".join(obj.properties["searchable_text"] for obj in response_objects)
    return context


def build_rag_prompt(query: str, context: str) -> str:
    prompt = f"""
        You are a helpful fashion store assistant.

        Your task is to answer the customer's question using
        ONLY the information provided in the product context.

        Instructions:
        - Use only the supplied context to answer.
        - Do not invent or assume product details, prices,
          discounts, availability, sizes, colors, or other attributes.
        - If the context contains the answer, provide a clear,
          concise, and helpful response.
        - If the context contains only partial information,
          answer what you can and clearly mention what is missing.
        - If the context does not contain the answer, politely
          inform the customer that the information is unavailable.
        - Do not use external knowledge or make assumptions.
        - Do not mention internal retrieval processes or the
          context itself.

        Product information:
        {context}
        
        Customer question:
        {query}
        """
    return prompt
