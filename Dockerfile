FROM python:3.12-slim AS requirements-builder

RUN mkdir build/
WORKDIR /build/

RUN pip install uv

COPY pyproject.toml uv.lock /build/

RUN uv pip compile pyproject.toml --quiet --output-file requirements.txt

FROM python:3.12-slim

WORKDIR /app

COPY --from=requirements-builder /build/requirements.txt /app/requirements.txt

# системные зависимости (часто нужны под feast / grpc / snappy и т.п.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py /app/app.py
# сюда же положи feature_store.yaml и repo Feast
# COPY feature_repo/ /app/feature_repo/
# ENV FEAST_REPO_PATH=/app/feature_repo

ENV PYTHONUNBUFFERED=1

CMD ["python", "-m", "app"]
