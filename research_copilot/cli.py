import json
from pathlib import Path

import typer

from .evaluation import evaluate_retrieval
from .pipeline import ResearchCopilot

app = typer.Typer(help="Research Intelligence Copilot")


@app.command()
def ingest(path: Path) -> None:
    """Ingest PDF, Markdown, and text files."""
    result = ResearchCopilot().ingest(path)
    typer.echo(result.model_dump_json(indent=2))


@app.command()
def ask(question: str, top_k: int = 4) -> None:
    """Ask a grounded question against the local index."""
    result = ResearchCopilot().query(question, top_k)
    typer.echo(result.model_dump_json(indent=2))


@app.command()
def evaluate(dataset: Path, top_k: int = 4) -> None:
    """Measure retrieval Recall@K and Mean Reciprocal Rank."""
    copilot = ResearchCopilot()
    metrics = evaluate_retrieval(copilot.index, dataset, top_k)
    typer.echo(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    app()
