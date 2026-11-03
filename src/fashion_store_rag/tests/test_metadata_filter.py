from fashion_store_rag.database.client import get_weaviate_client
from fashion_store_rag.query_understanding.metadata_extractor import ProductMetadata
from fashion_store_rag.retrieval.metadata_filters import build_metadata_filters


def test_metadata_filter():
    metadata = ProductMetadata(
        category="Topwear", sub_category="Shirt", gender="Men", fabric="Cotton"
    )

    filters = build_metadata_filters(metadata)

    with get_weaviate_client() as client:
        collection = client.collections.get("Products")

        response = collection.query.fetch_objects(
            filters=filters,
            limit=50,
        )

        for obj in response.objects:
            print(
                obj.properties["name"],
                "| Subcategory:",
                obj.properties["sub_category"],
                "| Fabric:",
                obj.properties["fabric"],
            )


test_metadata_filter()
