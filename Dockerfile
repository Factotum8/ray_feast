FROM python:3.12-slim AS requirements-builder
WORKDIR /build
RUN pip install uv
COPY pyproject.toml uv.lock /build/
RUN uv pip compile pyproject.toml --quiet --output-file requirements.txt

FROM python:3.12-slim
WORKDIR /app

COPY --from=requirements-builder /build/requirements.txt /app/requirements.txt

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc curl \
 && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py predictor.py routes.py types_.py /app/

ENV PYTHONUNBUFFERED=1


# another way to start see app.py
#CMD ["python", "app.py"]
CMD ["bash", "-lc", "ray start --head --disable-usage-stats --dashboard-host 0.0.0.0 && serve start --http-host 0.0.0.0 --http-port 8000 --address auto && serve run app:ingressed_app"]
