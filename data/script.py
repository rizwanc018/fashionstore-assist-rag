import json

data = json.load(open("raw/products.json"))  # noqa: SIM115
items = data if isinstance(data, list) else data.get("products", data)
ids = [
    p.get("product_id")
    for p in items
    # if float(p.get("price", 0)) < 800
    if str(p.get("fabric", "")).strip().lower() == "cotton"
    and str(p.get("gender", "")).strip().lower() == "women"
]
print(len(ids))
print(ids)
