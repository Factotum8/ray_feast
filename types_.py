from typing import Any

from pydantic import BaseModel, Field


class PredictRequest(BaseModel):
    entity_id: int = Field(..., ge=1, description="Entity id in Feast")


class PredictResponse(BaseModel):
    prediction: float
    features: dict[str, Any]
