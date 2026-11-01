from fashion_store_rag.database.client import get_weaviate_client


def search_products(query: str, limit: int = 5):
    with get_weaviate_client() as client:
        collection = client.collections.get("Products")

        response = collection.query.near_text(query=query, limit=limit)

        print("\nQuery: ", query)
        for obj in response.objects:
            print("Product:", obj.properties["name"])
            print("Distance:", obj.metadata.distance)


if __name__ == "__main__":
    search_products("comfortable cotton clothes for summer")
    search_products("black casual t-shirts for men")
