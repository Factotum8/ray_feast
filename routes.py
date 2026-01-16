from __future__ import annotations

from fastapi import APIRouter
from ray import serve

from types_ import PredictRequest

api_router_v1 = APIRouter()


@api_router_v1.get("/readyz")
async def readyz():
    return {"status": "ok"}


@api_router_v1.get("/livez")
async def livez():
    return {"status": "ok"}


class ApiDeployment:
    def __init__(self, model_handle):
        self.predictor = model_handle
        self._predictor = serve.get_deployment_handle("Predictor")


    @api_router_v1.post("/predict")
    async def predict(self, req: PredictRequest):
        # вызов внутреннего deployment
        y = await self.predictor.predict.remote(req.entity_id)
        r =  {"prediction": y}
        print(f"reply: {r}")
        return r
