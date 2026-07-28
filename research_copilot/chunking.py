import hashlib
import re

from .schemas import Chunk, Document


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def chunk_documents(
    documents: list[Document],
    chunk_size: int = 900,
    overlap: int = 150,
) -> list[Chunk]:
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks: list[Chunk] = []
    for document in documents:
        text = normalize_text(document.text)
        start = 0
        position = 0
        while start < len(text):
            end = min(start + chunk_size, len(text))
            if end < len(text):
                boundary = text.rfind(" ", start, end)
                end = boundary if boundary > start else end
            content = text[start:end].strip()
            if content:
                raw_id = f"{document.source}:{document.page}:{position}:{content[:80]}"
                chunk_id = hashlib.sha1(raw_id.encode(), usedforsecurity=False).hexdigest()[:12]
                chunks.append(
                    Chunk(
                        id=chunk_id,
                        source=document.source,
                        page=document.page,
                        position=position,
                        text=content,
                    )
                )
                position += 1
            if end >= len(text):
                break
            start = max(end - overlap, start + 1)
    return chunks
