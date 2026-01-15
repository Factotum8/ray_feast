FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
  && rm -rf /var/lib/apt/lists/*

# Feast + pandas для чтения CSV
RUN pip install --no-cache-dir feast pandas pyarrow

# Кладём repo
COPY feature_store.yaml /app/feature_store.yaml
COPY feature_repo.py /app/feature_repo.py
COPY data /app/data

# Инициализируем Feast repo в контейнере:
# - apply создаст таблицы онлайн/оффлайн
# - materialize заполнит онлайн-стор данными за период
# (время можно менять)
RUN feast apply && feast materialize 2020-01-01T00:00:00 2035-01-01T00:00:00

# Команда по умолчанию: показать список фичей (проверка)
CMD ["bash", "-lc", "feast feature-views list && feast entities list && echo 'Ready' && tail -f /dev/null"]
