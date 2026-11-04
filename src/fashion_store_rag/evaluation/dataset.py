import json
from pathlib import Path

DATASET_FILE = (
    Path(__file__).resolve().parents[3]
    / "data"
    / "evaluation"
    / "retrieval_dataset.json"
)


def load_evaluation_dataset() -> list[dict]:
    with DATASET_FILE.open(encoding="utf-8") as file:
        return json.load(file)
