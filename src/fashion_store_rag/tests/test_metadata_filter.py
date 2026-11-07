from fashion_store_rag.database.client import get_weaviate_client
from fashion_store_rag.query_understanding.metadata_extractor import extract_metadata
from fashion_store_rag.retrieval.metadata_filters import build_metadata_filters
from fashion_store_rag.retrieval.product_search import (
    search_products_hybrid,
)

query = "Show me blue prodcuts"

metadata = extract_metadata(query)
metadata_filter = build_metadata_filters(metadata)

print("Metadata:", metadata.model_dump(exclude_none=True))
print("Filter:", metadata_filter)

with get_weaviate_client() as client:
    collection = client.collections.get("Products")

    # response = collection.query.fetch_objects(
    #     filters=metadata_filter,
    #     limit=20,
    # )

    response = collection.query.near_text(
        query=query,
        filters=metadata_filter,
        limit=20,
    )

    for obj in response.objects:
        print(
            obj.properties["product_id"],
            obj.properties["name"],
            obj.properties["category"],
            obj.properties["sub_category"],
            obj.properties["color"],
        )


query = "Show me blue jeans"
metadata = extract_metadata(query)

results = search_products_hybrid(
    query=query,
    metadata=metadata,
    limit=10,
    retrieval_limit=15,
)

for obj in results:
    print(
        obj.properties["product_id"],
        obj.properties["name"],
        obj.properties["category"],
        obj.properties["sub_category"],
        obj.properties["color"],
    )
