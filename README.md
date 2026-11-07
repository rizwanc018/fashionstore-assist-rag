# Fashion Store RAG

An agentic RAG assistant for a fashion e‑commerce store. It answers customer
questions about products and store policies through a terminal chat, using a
hybrid retrieval pipeline (dense + BM25), cross‑encoder reranking, and an agent
loop that routes, evaluates, and refines its own retrieval.

## Features

- **Agentic orchestration** — a router sends each query to the right tool
  (product search, FAQ search, product details, or product comparison), then a
  retrieval evaluator decides whether the results are good enough or the query
  should be refined and retried.
- **Hybrid retrieval** — dense semantic search and BM25 keyword search run
  concurrently and are fused with Reciprocal Rank Fusion (RRF).
- **Query understanding** — query classification and metadata extraction drive
  structured filters (category, gender, color, price, etc.).
- **Reranking** — a `BAAI/bge-reranker-base` cross‑encoder reorders candidates.
- **Evaluation suite** — Precision@K / Recall@K retrieval metrics and
  faithfulness / response‑quality checks.


## Architecture

```
                  User Query
                      │
                      ▼
              Query Understanding
                      │
                      ▼
                 Query Router
          ┌───────────┼───────────┐
          ▼           ▼           ▼
      Products      FAQs     Out of Scope
          │           │           │
          ▼           │           │
  Retrieval Evaluation│           │
     │         │      │           │
  Accept   Refine / Retry ─┐      │
     │         ▲           │      │
     │         └───────────┘      │
     └───────────┼────────────────┘
                 ▼
          Answer Generation
                 │
                 ▼
            Final Answer
```

Retrieval backend is [Weaviate](https://weaviate.io) (cloud), embeddings and
answer generation use the OpenAI API, and the FAQ keyword index is built with
[`bm25s`](https://github.com/xhluo/bm25s).

## Requirements

- Python >= 3.14
- [uv](https://docs.astral.sh/uv/) for dependency management
- A Weaviate Cloud cluster
- An OpenAI API key

## Setup

1. Install dependencies:

   ```bash
   uv sync
   ```

2. Create a `.env` file in the project root:

   ```dotenv
   WEAVIATE_URL=https://your-cluster.weaviate.cloud
   WEAVIATE_API_KEY=your-weaviate-api-key
   OPENAI_API_KEY=your-openai-api-key
   ```

3. Create the Weaviate collections and ingest the data:

   ```bash
   uv run python -m fashion_store_rag.database.collection   # create collections
   uv run python -m fashion_store_rag.ingestion.products     # ingest products
   uv run python data/build_faq_indexes.py                   # build FAQ BM25 index
   ```

## Usage

Launch the interactive terminal assistant:

```bash
uv run fashion-store-rag
```

In‑chat commands:

| Command  | Description              |
|----------|--------------------------|
| `/help`  | Show available commands  |
| `/clear` | Clear the terminal       |
| `/exit`  | Quit the application      |

Enable logging by setting `LOG_LEVEL` (off by default):

```bash
LOG_LEVEL=INFO uv run fashion-store-rag
```

 Project structure

```
src/fashion_store_rag/
├── agent/              # orchestrator, router, evaluator, query refiner, tools
├── cli/                # rich terminal interface
├── config/             # settings / env loading
├── database/           # Weaviate client & collection definitions
├── ingestion/          # product and FAQ ingestion
├── query_understanding/# query classification & metadata extraction
├── retrieval/          # dense, BM25, fusion, filters, reranking, pipeline
├── evaluation/         # benchmark, dataset, metrics
├── prompts/            # prompt templates
└── services/           # OpenAI LLM service
```

## Evaluation

Retrieval and answer‑quality benchmarks live under
`src/fashion_store_rag/evaluation/` with a labelled dataset at
`data/evaluation/retrieval_dataset.json`.

## Data

- `data/raw/products.json` — 40 products with rich metadata (category, color,
  fabric, season, sizes, price, etc.).
- `data/raw/faqs.json` — 30 store FAQs across categories.
##