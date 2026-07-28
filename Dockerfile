FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml README.md ./
COPY research_copilot ./research_copilot
RUN pip install --no-cache-dir .

COPY data ./data

EXPOSE 8000

CMD ["uvicorn", "research_copilot.api:app", "--host", "0.0.0.0", "--port", "8000"]
