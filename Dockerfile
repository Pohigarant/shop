FROM ghcr.io/astral-sh/uv:python3.14-alpine
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1
WORKDIR /app
COPY . .
RUN uv sync --frozen --no-dev

CMD ["uv", "run", "manage.py", "runserver"]