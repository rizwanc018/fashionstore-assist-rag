import json
from pathlib import Path

import bm25s

from fashion_store_rag.utils.text_preperation import faq_to_text

DATA_DIR = Path(__file__).resolve().parents[3] / "data"
FAQS_FILE = DATA_DIR / "raw" / "faqs.json"
FAQ_INDEX_DIR = DATA_DIR / "indexes" / "faqs_bm25"


def load_faqs() -> list[dict]:
    with FAQS_FILE.open(encoding="utf-8") as file:
        return json.load(file)


def build_faq_index():
    faqs = load_faqs()
    faq_texts = [faq_to_text(faq) for faq in faqs]

    corpus_tokens = bm25s.tokenize(
        faq_texts,
        stopwords="en",
    )

    retriever = bm25s.BM25()
    retriever.index(corpus_tokens)

    retriever.save(str(FAQ_INDEX_DIR))

    print("FAQ BM25 index built and saved.")

    return retriever, faqs


def load_faq_index():
    retriever = bm25s.BM25.load(
        str(FAQ_INDEX_DIR),
        load_corpus=False,
    )

    faqs = load_faqs()

    return retriever, faqs
