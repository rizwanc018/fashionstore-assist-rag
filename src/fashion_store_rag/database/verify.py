from fashion_store_rag.database.client import get_weaviate_client


def verify_products():
    with get_weaviate_client() as client:
        collection = client.collections.get("Products")

        result = collection.aggregate.over_all(total_count=True)
        print("Total stored products: ", result.total_count)

        response = collection.query.fetch_objects(limit=5)

        if result.total_count > 0:
            for obj in response.objects:
                print("\nProduct ID:", obj.properties["product_id"])
                print("Name:", obj.properties["name"])
                print("Category:", obj.properties["category"])


if __name__ == "__main__":
    verify_products()
