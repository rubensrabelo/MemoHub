# Camada 1: Construtor (Builder)
FROM ghcr.io/astral-sh/uv:python3.12-alpine AS builder

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project --no-dev


# --- TRANSICAO: ESTAGIO DE EXECUCAO ---
FROM python:3.12-alpine

WORKDIR /app

COPY --from=builder /app/.venv /app/.venv

ENV PATH="/app/.venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1

COPY src/ /app/src/
COPY alembic.ini /app/alembic.ini
COPY entrypoint.sh /app/src/entrypoint.sh

RUN chmod +x /app/src/entrypoint.sh

EXPOSE 8000

ENTRYPOINT ["/app/src/entrypoint.sh"]
