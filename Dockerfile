FROM python:3.12-slim

LABEL org.opencontainers.image.title="pdf-extractext-api"
LABEL org.opencontainers.image.version="1.0.0"
LABEL org.opencontainers.image.description="FastAPI API for extracting text from PDF documents"
LABEL org.opencontainers.image.authors="Santiago Viñolo, Renata Michaux, Gaston Fernandez"

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /app

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock README.md ./

RUN uv sync --frozen --no-dev

COPY app ./app

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
