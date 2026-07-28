from pathlib import Path

from pydantic import BaseModel, Field


class Document(BaseModel):
    source: str
    text: str
    page: int | None = None


class Chunk(BaseModel):
    id: str
    source: str
    text: str
    page: int | None = None
    position: int = 0


class SearchResult(BaseModel):
    chunk: Chunk
    score: float = Field(ge=0)
    semantic_score: float = Field(ge=0)
    lexical_score: float = Field(ge=0)


class Citation(BaseModel):
    source: str
    page: int | None = None
    chunk_id: str
    excerpt: str


class QueryRequest(BaseModel):
    question: str = Field(min_length=3)
    top_k: int = Field(default=4, ge=1, le=10)


class QueryResponse(BaseModel):
    answer: str
    intent: str
    confidence: float
    citations: list[Citation]


class IngestRequest(BaseModel):
    path: Path


class IngestResponse(BaseModel):
    documents: int
    chunks: int
    index_path: str
