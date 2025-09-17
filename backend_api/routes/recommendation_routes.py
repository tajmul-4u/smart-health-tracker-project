from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..models.recommendation import RecommendationResponse
from ..utils.security import SecurityUtils
from ...app.database.local_db import get_db
from ...app.models.recommendation_model import Recommendation
from ...app.models.user_model import User
from ...app.services.ai_service import AIService

router = APIRouter()

@router.get("/", response_model=List[RecommendationResponse])
async def get_recommendations(
    token: dict = Depends(SecurityUtils.auth_wrapper),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == token["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get user's habits and health metrics for AI analysis
    recommendations = db.query(Recommendation).filter(
        Recommendation.user_id == user.id
    ).order_by(Recommendation.created_at.desc()).all()
    
    return recommendations

@router.post("/generate", response_model=List[RecommendationResponse])
async def generate_recommendations(
    token: dict = Depends(SecurityUtils.auth_wrapper),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == token["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Generate new recommendations using AI service
    ai_service = AIService()
    new_recommendations = ai_service.generate_recommendations(user, db)
    
    # Save new recommendations to database
    for rec in new_recommendations:
        db_rec = Recommendation(**rec.dict(), user_id=user.id)
        db.add(db_rec)
    
    db.commit()
    
    return new_recommendations

@router.put("/{recommendation_id}/implement")
async def mark_recommendation_implemented(
    recommendation_id: int,
    token: dict = Depends(SecurityUtils.auth_wrapper),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == token["sub"]).first()
    recommendation = db.query(Recommendation).filter(
        Recommendation.id == recommendation_id,
        Recommendation.user_id == user.id
    ).first()
    
    if not recommendation:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    
    recommendation.is_implemented = True
    db.commit()
    db.refresh(recommendation)
    
    return {"message": "Recommendation marked as implemented"}