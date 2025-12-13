FROM ghcr.io/astral-sh/uv:python3.12-trixie-slim AS base

WORKDIR /app
COPY uv.lock pyproject.toml /app/

RUN mkdir /venv

ENV UV_PROJECT_ENVIRONMENT=/venv/app

RUN uv sync --locked

EXPOSE 5050

CMD ["uv", "run", "ddtrace-run", "python", "main.py"]
