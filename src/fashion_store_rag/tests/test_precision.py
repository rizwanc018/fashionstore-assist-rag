# 1. All retrieved products are relevant
from fashion_store_rag.evaluation.metrics import precision_at_k

assert precision_at_k(["P1001", "P1002"], ["P1001", "P1002"], k=2) == 1.0


# 2. No retrieved products are relevant
assert precision_at_k(["P1003", "P1004"], ["P1001", "P1002"], k=2) == 0.0


# 3. Empty retrieval results
assert precision_at_k([], ["P1001", "P1002"], k=5) == 0.0

print("All tests passed!")
