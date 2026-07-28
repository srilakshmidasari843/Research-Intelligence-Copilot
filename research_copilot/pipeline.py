from pathlib import Path

from .chunking import chunk_documents
from .config import Settings, get_settings
from .generation import ExtractiveGenerator, OpenAIGenerator
from .ingestion import load_path
from .retrieval import HybridIndex
from .schemas import Citation, IngestResponse, QueryResponse


def classify_intent(question: str) -> str:
    lowered = question.lower()
    if any(word in lowered for word in ("summarize", "summary", "overview")):
        return "summary"
    if any(word in lowered for word in ("compare", "versus", "difference", "similarities")):
        return "comparison"
    if any(word in lowered for word in ("find", "search", "locate", "which document")):
        return "search"
    return "question"


class ResearchCopilot:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self.index = HybridIndex.load(self.settings.index_path)
        if self.settings.generator_provider.lower() == "openai":
            if not self.settings.openai_api_key:
                raise ValueError("OPENAI_API_KEY is required when GENERATOR_PROVIDER=openai")
            self.generator = OpenAIGenerator(
                api_key=self.settings.openai_api_key,
                model=self.settings.openai_model,
            )
        else:
            self.generator = ExtractiveGenerator()

    def ingest(self, path: Path) -> IngestResponse:
        documents = load_path(path)
        chunks = chunk_documents(documents)
        self.index = HybridIndex(chunks)
        self.index.save(self.settings.index_path)
        return IngestResponse(
            documents=len(documents),
            chunks=len(chunks),
            index_path=str(self.settings.index_path),
        )

    def query(self, question: str, top_k: int = 4) -> QueryResponse:
        intent = classify_intent(question)
        results = self.index.search(question, top_k=top_k)
        confidence = results[0].score if results else 0.0
        if confidence < self.settings.min_confidence:
            results = []

        answer = self.generator.generate(question, results, intent)
        citations = [
            Citation(
                source=result.chunk.source,
                page=result.chunk.page,
                chunk_id=result.chunk.id,
                excerpt=result.chunk.text[:220],
            )
            for result in results
        ]
        return QueryResponse(
            answer=answer,
            intent=intent,
            confidence=round(confidence, 4),
            citations=citations,
        )
