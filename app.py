from __future__ import annotations

import os

import ray
from ray import serve
from fastapi import FastAPI

from predictor import Predictor
from routes import api_router_v1

app = FastAPI(title="Ray Serve + FastAPI")

app.include_router(api_router_v1)


class ApiDeployment:
    def __init__(self, model_handle):
        self.predictor = model_handle

    @app.get("/predict")
    async def predict(self, x: int):
        # вызов внутреннего deployment
        y = await self.predictor.predict.remote(x)
        return {"prediction": y}

# ingress применяем к обычному классу
# IngressedPredictor = serve.ingress(app)(Predictor)

# затем превращаем в deployment (тут задаём ресурсы и лимиты)
# IngressedApp = serve.deployment(
#     ray_actor_options={"num_cpus": 1},
#     max_ongoing_requests=64,
# )(IngressedPredictor)

# ingressed_app=IngressedApp.bind()

# ingress = serve.ingress(app)()

# deployment обычный класс c логикой обращения к Feast
predictor_deployment = Predictor.bind()

# ingress применяем к FastAPI приложение для доступа из сети
ingressed_app = serve.deployment()(serve.ingress(app)(ApiDeployment)).bind(predictor_deployment)
# ingressed_app = serve.deployment()(serve.ingress(app)(Predictor)).bind()

def main() -> None:
    addr = os.getenv("RAY_ADDRESS")
    ray.init(address=addr) if addr else ray.init(ignore_reinit_error=True)

    serve.run(ingressed_app, route_prefix="/")


if __name__ == "__main__":
    main()
