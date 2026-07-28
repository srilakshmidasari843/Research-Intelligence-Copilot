import json
import math
import re
from collections import Counter
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import HashingVectorizer

from .schemas import Chunk, SearchResult

TOKEN_PATTERN = re.compile(r"\b[a-zA-Z0-9][a-zA-Z0-9_-]+\b")


def tokenize(text: str) -> list[str]:
    return TOKEN_PATTERN.findall(text.lower())


class HybridIndex:
    def __init__(self, chunks: list[Chunk] | None = None) -> None:
        self.chunks = chunks or []
        self.vectorizer = HashingVectorizer(
            n_features=2**12,
            alternate_sign=False,
            norm="l2",
            stop_words="english",
        )
        self._document_frequencies = self._build_document_frequencies()

    def _build_document_frequencies(self) -> Counter[str]:
        frequencies: Counter[str] = Counter()
        for chunk in self.chunks:
            frequencies.update(set(tokenize(chunk.text)))
        return frequencies

    def add(self, chunks: list[Chunk]) -> None:
        self.chunks.extend(chunks)
        self._document_frequencies = self._build_document_frequencies()

    def _lexical_score(self, query_tokens: list[str], chunk: Chunk) -> float:
        if not query_tokens:
            return 0.0
        chunk_counts = Counter(tokenize(chunk.text))
        total_documents = max(len(self.chunks), 1)
        score = 0.0
        for token in query_tokens:
            term_frequency = chunk_counts[token] / max(len(chunk_counts), 1)
            inverse_document_frequency = math.log(
                1 + total_documents / (1 + self._document_frequencies[token])
            )
            score += term_frequency * inverse_document_frequency
        return score

    def search(self, query: str, top_k: int = 4) -> list[SearchResult]:
        if not self.chunks:
            return []

        corpus = [chunk.text for chunk in self.chunks]
        chunk_vectors = self.vectorizer.transform(corpus)
        query_vector = self.vectorizer.transform([query])
        semantic = (chunk_vectors @ query_vector.T).toarray().ravel()
        lexical = np.array(
            [self._lexical_score(tokenize(query), chunk) for chunk in self.chunks]
        )

        if lexical.max(initial=0) > 0:
            lexical = lexical / lexical.max()
        combined = 0.7 * semantic + 0.3 * lexical
        best_indices = np.argsort(combined)[::-1][:top_k]

        return [
            SearchResult(
                chunk=self.chunks[index],
                score=float(max(combined[index], 0)),
                semantic_score=float(max(semantic[index], 0)),
                lexical_score=float(max(lexical[index], 0)),
            )
            for index in best_indices
            if combined[index] > 0
        ]

    def save(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps([chunk.model_dump() for chunk in self.chunks], indent=2),
            encoding="utf-8",
        )

    @classmethod
    def load(cls, path: Path) -> "HybridIndex":
        if not path.exists():
            return cls()
        data = json.loads(path.read_text(encoding="utf-8"))
        return cls([Chunk.model_validate(item) for item in data])
