from __future__ import annotations

from fastapi import APIRouter, HTTPException

from types_ import PredictRequest, PredictResponse

api_router_v1 = APIRouter()


@api_router_v1.get("/readyz")
async def readyz():
    return {"status": "ok"}


@api_router_v1.get("/livez")
async def livez():
    return {"status": "ok"}


@api_router_v1.post("/predict")
async def predict(req: PredictRequest):
    try:
        return PredictResponse(
            prediction=req.entity_id * 0.01, features={"entity_id": req.entity_id}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")
