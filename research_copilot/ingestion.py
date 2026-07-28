from pathlib import Path

from pypdf import PdfReader

from .schemas import Document

SUPPORTED_EXTENSIONS = {".pdf", ".txt", ".md"}


def load_file(path: Path) -> list[Document]:
    if path.suffix.lower() == ".pdf":
        reader = PdfReader(path)
        return [
            Document(source=path.name, page=number, text=page.extract_text() or "")
            for number, page in enumerate(reader.pages, start=1)
            if (page.extract_text() or "").strip()
        ]

    if path.suffix.lower() in {".txt", ".md"}:
        return [Document(source=path.name, text=path.read_text(encoding="utf-8"))]

    raise ValueError(f"Unsupported file type: {path.suffix}")


def load_path(path: Path) -> list[Document]:
    if not path.exists():
        raise FileNotFoundError(f"Path does not exist: {path}")

    files = [path] if path.is_file() else sorted(
        item for item in path.rglob("*") if item.suffix.lower() in SUPPORTED_EXTENSIONS
    )
    documents: list[Document] = []
    for file_path in files:
        documents.extend(load_file(file_path))
    return documents
