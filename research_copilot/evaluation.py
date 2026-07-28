import json
from pathlib import Path

from .retrieval import HybridIndex


def evaluate_retrieval(index: HybridIndex, dataset_path: Path, top_k: int = 4) -> dict:
    examples = json.loads(dataset_path.read_text(encoding="utf-8"))
    hits = 0
    reciprocal_ranks: list[float] = []

    for example in examples:
        results = index.search(example["question"], top_k=top_k)
        expected_source = example["expected_source"]
        rank = next(
            (
                position
                for position, result in enumerate(results, start=1)
                if result.chunk.source == expected_source
            ),
            None,
        )
        hits += int(rank is not None)
        reciprocal_ranks.append(1 / rank if rank else 0.0)

    count = len(examples)
    return {
        "questions": count,
        "recall_at_k": round(hits / count, 4) if count else 0,
        "mean_reciprocal_rank": (
            round(sum(reciprocal_ranks) / count, 4) if count else 0
        ),
    }
