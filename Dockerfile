FROM ghcr.io/astral-sh/uv:python3.14-alpine
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1
WORKDIR /app
COPY . .
RUN uv sync --frozen --no-dev
RUN uv run python manage.py collectstatic --noinput

CMD ["uv", "run", "gunicorn", "shop1.wsgi:application", \

     "--bind", "0.0.0.0:8000", \

     "--workers", "3", \

     "--timeout", "60", \

     "--access-logfile", "-"]
