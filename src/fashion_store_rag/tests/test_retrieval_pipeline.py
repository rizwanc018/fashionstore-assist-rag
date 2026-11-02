from fashion_store_rag.retrieval.retrieval_pipeline import (
    retrieve_products,
)

if __name__ == "__main__":
    queries = [
        "Find cotton shirts for men",
        # "Find comfortable clothes for hot weather",
        # "Show me blue jeans",
        "Find clothes under ₹800",
        # "Comfortable clothes for hot weather",
    ]

    for query in queries:
        print("\n" + "=" * 60)
        print("QUERY:", query)

        result = retrieve_products(query)

        print("INTENT:", result["intent"])

        if result["products"]:
            print("\nRETRIEVED PRODUCTS:")

            for rank, item in enumerate(result["products"], start=1):
                product = item["product"]
                props = product.properties

                print(f"\n{rank}. {product.properties['name']}")
                print(f"Score: {item['score']:.4f}")

                print(
                    props["name"],
                    "| Price:",
                    props["price"],
                    "| Fabric:",
                    props["fabric"],
                    "| Category:",
                    props["category"],
                    "| Subcategory:",
                    props["sub_category"],
                    "| Gender:",
                    props["gender"],
                )
