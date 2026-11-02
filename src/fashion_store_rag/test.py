from fashion_store_rag.query_understanding.metadata_extractor import extract_metadata
from fashion_store_rag.retrieval.product_search import (
    search_products,
    search_products_with_filters,
)

query = "Show me black cotton T-shirts for men under 800"

metadata = extract_metadata(query)

print("Extracted metadata:")
print(metadata.model_dump())


products = search_products(
    query=query,
    limit=5,
)
print("\nRetrieved products:")
for product in products.objects:
    print(
        product.properties["name"],
        product.properties["color"],
        product.properties["fabric"],
        product.properties["price"],
    )

metadata_products = search_products_with_filters(
    query=query,
    metadata=metadata,
    limit=5,
)
print("\nRetrieved metadata_products:")
for product in metadata_products.objects:
    print(
        product.properties["name"],
        product.properties["color"],
        product.properties["fabric"],
        product.properties["price"],
    )
