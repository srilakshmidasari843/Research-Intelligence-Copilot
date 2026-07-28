from pathlib import Path

from research_copilot.config import Settings
from research_copilot.pipeline import ResearchCopilot, classify_intent


def test_intent_routing() -> None:
    assert classify_intent("Summarize the papers") == "summary"
    assert classify_intent("Compare the methods") == "comparison"
    assert classify_intent("What is retrieval?") == "question"


def test_pipeline_ingests_and_answers(tmp_path: Path) -> None:
    docs = tmp_path / "docs"
    docs.mkdir()
    (docs / "evidence.md").write_text(
        "Hybrid retrieval combines semantic similarity with lexical matching.",
        encoding="utf-8",
    )
    settings = Settings(index_path=tmp_path / "index.json", min_confidence=0.01)
    copilot = ResearchCopilot(settings)

    ingest_result = copilot.ingest(docs)
    response = copilot.query("What does hybrid retrieval combine?")

    assert ingest_result.documents == 1
    assert response.citations[0].source == "evidence.md"
    assert "semantic similarity" in response.answer
