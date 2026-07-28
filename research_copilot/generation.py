import re
from abc import ABC, abstractmethod

from .schemas import SearchResult


class AnswerGenerator(ABC):
    @abstractmethod
    def generate(self, question: str, results: list[SearchResult], intent: str) -> str:
        raise NotImplementedError


class ExtractiveGenerator(AnswerGenerator):
    """Deterministic generator for a free, reproducible local demo."""

    def generate(self, question: str, results: list[SearchResult], intent: str) -> str:
        del question
        if not results:
            return "I do not have enough evidence in the indexed documents to answer that."

        sentences: list[str] = []
        for result in results[:3]:
            candidates = re.split(r"(?<=[.!?])\s+", result.chunk.text)
            best = next((sentence for sentence in candidates if len(sentence) > 45), candidates[0])
            source = result.chunk.source
            page = f", p. {result.chunk.page}" if result.chunk.page else ""
            sentences.append(f"{best.strip()} [{source}{page}]")

        lead = {
            "summary": "The indexed evidence can be summarized as follows:",
            "comparison": "The most relevant points for comparison are:",
            "search": "The strongest evidence I found is:",
            "question": "Based on the indexed evidence:",
        }.get(intent, "Based on the indexed evidence:")
        return f"{lead}\n\n" + "\n\n".join(f"- {sentence}" for sentence in sentences)


class OpenAIGenerator(AnswerGenerator):
    def __init__(self, api_key: str, model: str) -> None:
        try:
            from openai import OpenAI
        except ImportError as error:
            raise RuntimeError("Install the OpenAI extra: pip install -e '.[openai]'") from error
        self.client = OpenAI(api_key=api_key)
        self.model = model

    def generate(self, question: str, results: list[SearchResult], intent: str) -> str:
        context = "\n\n".join(
            f"[{result.chunk.source}, page {result.chunk.page or 'n/a'}]\n{result.chunk.text}"
            for result in results
        )
        response = self.client.responses.create(
            model=self.model,
            instructions=(
                "Answer only from the supplied context. Cite claims using the source labels. "
                "If evidence is insufficient, say so. Do not invent facts."
            ),
            input=f"Intent: {intent}\nQuestion: {question}\n\nContext:\n{context}",
        )
        return response.output_text
