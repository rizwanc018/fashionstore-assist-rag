import json
from pathlib import Path

from fashion_store_rag.utils.text_preperation import faq_to_text, product_to_text

DATA_DIR = Path(__file__).resolve().parent.parent.parent.parent / "data"
PRODUCTS_RAW = DATA_DIR / "raw" / "products.json"
FAQS_RAW = DATA_DIR / "raw" / "faqs.json"

with PRODUCTS_RAW.open(encoding="utf-8") as f:
    products = json.load(f)

with FAQS_RAW.open(encoding="utf-8") as f:
    faqs = json.load(f)

products_text = [product_to_text(product) for product in products]
faqs_text = [faq_to_text(faq) for faq in faqs]


products_text[0]
faqs_text[0]
