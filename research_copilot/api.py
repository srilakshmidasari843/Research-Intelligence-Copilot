from functools import lru_cache

from fastapi import FastAPI, HTTPException

from .pipeline import ResearchCopilot
from .schemas import IngestRequest, IngestResponse, QueryRequest, QueryResponse

app = FastAPI(
    title="Research Intelligence Copilot",
    description="Hybrid RAG with grounded citations and retrieval evaluation.",
    version="0.1.0",
)


@lru_cache
def get_copilot() -> ResearchCopilot:
    return ResearchCopilot()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}


@app.post("/ingest", response_model=IngestResponse)
def ingest(request: IngestRequest) -> IngestResponse:
    try:
        return get_copilot().ingest(request.path)
    except (FileNotFoundError, ValueError) as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest) -> QueryResponse:
    return get_copilot().query(request.question, request.top_k)
