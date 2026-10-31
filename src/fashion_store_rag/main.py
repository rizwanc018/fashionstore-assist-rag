from weaviate.classes.config import DataType, Property

from fashion_store_rag.database.client import get_weaviate_client


def add_missing_properties():
    with get_weaviate_client() as client:
        products = client.collections.get("Products")

        properties = [
            Property(
                name="description", data_type=DataType.TEXT, skip_vectorization=True
            ),
            Property(
                name="sizes", data_type=DataType.TEXT_ARRAY, skip_vectorization=True
            ),
            Property(name="currency", data_type=DataType.TEXT, skip_vectorization=True),
            Property(name="fabric", data_type=DataType.TEXT, skip_vectorization=True),
            Property(
                name="features", data_type=DataType.TEXT_ARRAY, skip_vectorization=True
            ),
            Property(
                name="care_instructions",
                data_type=DataType.TEXT,
                skip_vectorization=True,
            ),
        ]

        for prop in properties:
            products.config.add_property(prop)

        print("Additional product properties added.")


add_missing_properties()
