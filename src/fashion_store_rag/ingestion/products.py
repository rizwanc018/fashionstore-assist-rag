# DATA Already added


import json
from pathlib import Path

from weaviate.util import generate_uuid5

from fashion_store_rag.database.client import get_weaviate_client
from fashion_store_rag.utils.text_preperation import product_to_text

DATA_DIR = Path(__file__).resolve().parents[3] / "data"
PRODUCTS_FILE = DATA_DIR / "raw" / "products.json"


def load_products():
    with PRODUCTS_FILE.open(encoding="utf-8") as file:
        return json.load(file)


def ingest_products():
    products = load_products()

    with get_weaviate_client() as client:
        collection = client.collections.get("Products")

        with collection.batch.dynamic() as batch:
            for product in products:
                properties = {
                    "product_id": product["product_id"],
                    "searchable_text": product_to_text(product),
                    "name": product["name"],
                    "category": product["category"],
                    "sub_category": product["sub_category"],
                    "gender": product["gender"],
                    "usage": product["usage"],
                    "season": product["season"],
                    "color": product["color"],
                    "price": product["price"],
                    "fabric": product["fabric"],
                    "sizes": product["sizes"],
                }

                batch.add_object(
                    properties=properties, uuid=generate_uuid5(product["product_id"])
                )

        failed_objects = collection.batch.failed_objects

        print(f"Total products: {len(products)}")
        print(f"Failed imports: {len(failed_objects)}")
        print(f"Successful imports: {len(products) - len(failed_objects)}")

        if failed_objects:
            print("First failed object:")
            print(failed_objects[0])


if __name__ == "__main__":
    ingest_products()
