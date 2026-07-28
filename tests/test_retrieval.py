from research_copilot.retrieval import HybridIndex
from research_copilot.schemas import Chunk


def test_hybrid_search_returns_relevant_source() -> None:
    index = HybridIndex(
        [
            Chunk(id="a", source="rag.md", text="Recall at K evaluates retrieval ranking."),
            Chunk(id="b", source="security.md", text="Access control protects private data."),
        ]
    )

    results = index.search("retrieval recall metric", top_k=1)

    assert results[0].chunk.source == "rag.md"
    assert results[0].score > 0
