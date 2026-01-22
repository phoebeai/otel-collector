FROM ghcr.io/astral-sh/uv:python3.12-trixie-slim AS base

WORKDIR /app
COPY uv.lock pyproject.toml main.py /app/

RUN mkdir /venv

ENV UV_PROJECT_ENVIRONMENT=/venv/app

RUN uv sync --locked

EXPOSE 8089

CMD ["uv", "run", "python", "main.py"]
