def product_to_text(product):
    return (
        f"Product Name: {product['name']}. "
        f"Description: {product['description']}. "
        f"Category: {product['category']}. "
        f"Gender: {product['gender']}. "
        f"Available sizes: {', '.join(product['sizes'])}. "
        f"Usage: {product['usage']}. "
        f"Care instructions: {product['care_instructions']}."
    )


def faq_to_text(faq):
    return (
        f"Question: {faq['question']}. "
        f"Answer: {faq['answer']}. "
        f"Category: {faq['category']}."
    )
