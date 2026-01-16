from __future__ import annotations

import os

import ray
from ray import serve
from fastapi import FastAPI

from predictor import Predictor
from routes import api_router_v1, ApiDeployment

app = FastAPI(title="Ray Serve + FastAPI")

app.include_router(api_router_v1)

# deployment обычный класс c логикой обращения к Feast
predictor_deployment = Predictor.bind()
# ingress применяем к FastAPI приложение для доступа из сети
ingressed_app = serve.deployment()(serve.ingress(app)(ApiDeployment)).bind(
    predictor_deployment
)


def main() -> None:
    addr = os.getenv("RAY_ADDRESS")
    ray.init(address=addr) if addr else ray.init(ignore_reinit_error=True)

    serve.start(
        http_options={
            "host": "0.0.0.0",
            "port": 8000,
        }
    )

    serve.run(ingressed_app, route_prefix="/")


if __name__ == "__main__":
    main()
