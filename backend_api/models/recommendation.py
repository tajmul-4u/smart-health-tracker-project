from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class RecommendationBase(BaseModel):
    title: str
    description: str
    recommendation_type: str
    confidence_score: float
    priority_level: int

class RecommendationCreate(RecommendationBase):
    pass

class RecommendationResponse(RecommendationBase):
    id: int
    user_id: int
    is_implemented: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True