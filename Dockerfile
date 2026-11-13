FROM python:3.14-slim

COPY --from=ghcr.io/astral-sh/uv:0.13.8 /uv /uvx /bin/

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN uv sync --locked --no-dev --no-install-project

COPY README.md ./
COPY schemas ./schemas
COPY src ./src
COPY data/interim/human-coded ./data/interim/human-coded
RUN uv sync --locked --no-dev

WORKDIR /app/src/myproject

EXPOSE 8000

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"]
