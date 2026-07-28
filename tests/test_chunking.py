import pytest

from research_copilot.chunking import chunk_documents
from research_copilot.schemas import Document


def test_chunk_documents_preserves_metadata() -> None:
    document = Document(source="paper.pdf", page=2, text="Evidence " * 300)
    chunks = chunk_documents([document], chunk_size=200, overlap=30)

    assert len(chunks) > 1
    assert all(chunk.source == "paper.pdf" for chunk in chunks)
    assert all(chunk.page == 2 for chunk in chunks)
    assert len({chunk.id for chunk in chunks}) == len(chunks)


def test_invalid_overlap_is_rejected() -> None:
    with pytest.raises(ValueError):
        chunk_documents([], chunk_size=100, overlap=100)
