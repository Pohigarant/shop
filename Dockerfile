FROM ghcr.io/astral-sh/uv:python3.14-alpine
ENV UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-install-project
COPY .env ./
COPY manage.py ./
COPY conftest.py ./
COPY shop1/ shop1/
COPY cart/ cart/
COPY categories/ categories/
COPY order/ order/
COPY products/ products/
COPY review/ review/
COPY users/ users/
COPY tests/ tests/
RUN uv run python manage.py collectstatic --noinput
CMD ["uv", "run", "gunicorn", "shop1.wsgi:application", \
     "--bind", "0.0.0.0:8000", \
     "--workers", "3",\
     "--timeout", "60", \
     "--access-logfile", "-"]
