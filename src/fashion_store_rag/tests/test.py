from fashion_store_rag.evaluation.benchmark import run_benchmark

results = run_benchmark(k=5, candidate_limit=15)

print("\n=== SUMMARY ===")

for strategy, metrics in results["summary"].items():
    print(f"\n{strategy}")

    for metric, score in metrics.items():
        print(f"{metric}: {score:.4f}")

print("\n=== PER QUERY RESULTS ===")

for item in results["per_query"]:
    print(f"\nQuery: {item['query']}")
    print(f"Relevant IDs: {item['relevant_product_ids']}")

    for strategy, metrics in item["strategies"].items():
        print(f"\n  {strategy}")
        print(f"    Retrieved: {metrics['retrieved_product_ids']}")
        print(f"    Precision@5: {metrics['Precision@5']:.4f}")
        print(f"    Recall@5: {metrics['Recall@5']:.4f}")
        print(f"    RR: {metrics['RR']:.4f}")
