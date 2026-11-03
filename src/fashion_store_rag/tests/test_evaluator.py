from fashion_store_rag.agent.evaluator import evaluate_retrieval

# products = [
#     {
#         "name": "Women's High-Rise Straight Jeans",
#         "category": "Bottomwear",
#         "sub_category": "Jeans",
#         "color": "Blue",
#         "fabric": "Denim Cotton",
#         "price": 1999,
#     }
# ]

# products = [
#     {
#         "name": "Men's Slim Fit Polo T-Shirt",
#         "category": "Topwear",
#         "sub_category": "T-Shirt",
#         "color": "Black",
#         "fabric": "Cotton",
#         "price": 899,
#     }
# ]

products = []
evaluation = evaluate_retrieval(
    query="Show me blue jeans",
    products=products,
)

print(evaluation.model_dump())
