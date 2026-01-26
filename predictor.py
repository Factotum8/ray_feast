from __future__ import annotations

import os
from typing import Any

from ray import serve
from feast import FeatureStore


@serve.deployment(
    ray_actor_options={"num_cpus": 2},
    max_ongoing_requests=64,
)
class Predictor:
    """
     Внутренний deployment (без ingress).
     Тут можно держать Feast FeatureStore, модель и т.д.
     Что даёт внутренний deployment
        Масштабируется отдельно от API
        Можно задать другие ресурсы (CPU/GPU)
        Можно включить batching
        Можно менять модель без трогания API

    | Сценарий              | Да / Нет |
    | --------------------- | -------- |
    | ML inference          | ✅        |
    | Feast / feature store | ✅        |
    | Batch inference       | ✅        |
    | Heavy CPU/GPU         | ✅        |
    | Простое CRUD API      | ❌        |
    """

    def __init__(self) -> None:
        repo_path = os.getenv(
            "FEAST_REPO_PATH", "/Users/alex/Documents/projects/ray_feast/feast_repo"
        )
        self.store = FeatureStore(repo_path=repo_path)
        self.feature_refs = ["player_features:avg_deposit"]
        self.bias = float(os.getenv("MODEL_BIAS", "0.1"))

    def get_features(self, entity_id: int) -> dict[str, Any]:
        """
        Забирает online-фичи из Feast и приводит к плоскому dict.
        """
        raw = self.store.get_online_features(
            features=self.feature_refs,
            entity_rows=[{"player_id": entity_id}],
        ).to_dict()

        # Feast возвращает: {"feature_name": [value]}
        return {
            name: values[0] if isinstance(values, list) else values
            for name, values in raw.items()
        }

    def predict(self, entity_id: int) -> float:
        """
        Делает prediction на основе фичей.
        """
        features = self.get_features(entity_id)

        # --- пример бизнес-логики / модели ---
        avg_deposit = float(features.get("player_features:avg_deposit") or 0.0)

        prediction = avg_deposit * 0.01 + self.bias
        return prediction
