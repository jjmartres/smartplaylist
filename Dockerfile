ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim-bookworm AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml uv.lock ./
COPY src ./src

# hadolint ignore=DL3013
RUN pip install --no-cache-dir uv \
  && uv venv \
  && uv sync --frozen --all-extras \
  && uv pip install -e . \
  && find /app/src -type d -name __pycache__ -exec rm -rf {} +

FROM python:${PYTHON_VERSION}-slim-bookworm AS final

RUN addgroup --system appgroup \
  && adduser --system --ingroup appgroup --home /home/appuser appuser

WORKDIR /app

ENV HOME=/home/appuser \
  PYTHONDONTWRITEBYTECODE=1 \
  PYTHONUNBUFFERED=1 \
  PATH="/app/.venv/bin:$PATH" \
  PYTHONPATH="/app/src"

COPY --from=builder /app/.venv /app/.venv
COPY --from=builder /app/src ./src
COPY docker/entrypoint.sh /entrypoint.sh

RUN mkdir -p /app/data \
  && chmod +x /entrypoint.sh \
  && chown -R appuser:appgroup /app \
  && chown appuser:appgroup /entrypoint.sh

USER appuser

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
