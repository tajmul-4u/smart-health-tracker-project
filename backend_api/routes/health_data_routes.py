from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc, func, and_
from typing import List, Optional
from datetime import datetime, date, timedelta
import sys
import os

# Add project root to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../'))

from app.database.local_db import get_db
from app.models.user_model import User
from app.models.health_data_model import HealthData
from models.health_data import (
    HealthDataCreate, 
    HealthDataResponse, 
    HealthDataUpdate,
    HealthDataSummary,
    HealthDataChartData
)

router = APIRouter()

def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    """Calculate BMI from weight and height"""
    if weight_kg and height_cm:
        height_m = height_cm / 100
        return round(weight_kg / (height_m ** 2), 2)
    return None

def get_current_user_id():
    """Get current user ID - simplified for demo, in production use JWT"""
    # This should be replaced with proper JWT token validation
    # For now, we'll use a global variable as in the enhanced main
    global current_user_id
    return getattr(sys.modules.get('__main__', sys.modules[__name__]), 'current_user_id', None)

@router.post("/api/v1/healthdata", response_model=HealthDataResponse)
async def create_health_data(health_data: HealthDataCreate, db: Session = Depends(get_db)):
    """Create new health data entry"""
    user_id = get_current_user_id()
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # Verify user exists
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Calculate BMI if weight and height are provided
    bmi = None
    if health_data.weight and health_data.height:
        bmi = calculate_bmi(health_data.weight, health_data.height)
    elif health_data.weight and user.height:
        bmi = calculate_bmi(health_data.weight, user.height)
    elif user.weight and health_data.height:
        bmi = calculate_bmi(user.weight, health_data.height)
    elif user.weight and user.height:
        bmi = calculate_bmi(user.weight, user.height)
    
    # Create health data entry
    db_health_data = HealthData(
        user_id=user_id,
        systolic_bp=health_data.systolic_bp,
        diastolic_bp=health_data.diastolic_bp,
        blood_sugar=health_data.blood_sugar,
        sugar_test_type=health_data.sugar_test_type,
        sleep_hours=health_data.sleep_hours,
        sleep_quality=health_data.sleep_quality,
        stress_level=health_data.stress_level,
        stress_notes=health_data.stress_notes,
        steps_count=health_data.steps_count,
        exercise_minutes=health_data.exercise_minutes,
        weight=health_data.weight,
        height=health_data.height,
        bmi=bmi,
        heart_rate=health_data.heart_rate,
        water_intake=health_data.water_intake,
        mood_score=health_data.mood_score,
        energy_level=health_data.energy_level,
        notes=health_data.notes,
        measurement_time=health_data.measurement_time or datetime.utcnow()
    )
    
    db.add(db_health_data)
    db.commit()
    db.refresh(db_health_data)
    
    return db_health_data

@router.get("/api/v1/healthdata", response_model=List[HealthDataResponse])
async def get_health_data(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    db: Session = Depends(get_db)
):
    """Get health data entries for current user"""
    user_id = get_current_user_id()
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    query = db.query(HealthData).filter(HealthData.user_id == user_id)
    
    # Filter by date range if provided
    if start_date:
        query = query.filter(HealthData.measurement_time >= start_date)
    if end_date:
        query = query.filter(HealthData.measurement_time <= end_date + timedelta(days=1))
    
    health_data = query.order_by(desc(HealthData.measurement_time)).offset(skip).limit(limit).all()
    return health_data

@router.get("/api/v1/healthdata/{health_data_id}", response_model=HealthDataResponse)
async def get_health_data_by_id(health_data_id: int, db: Session = Depends(get_db)):
    """Get specific health data entry"""
    user_id = get_current_user_id()
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    health_data = db.query(HealthData).filter(
        HealthData.id == health_data_id,
        HealthData.user_id == user_id
    ).first()
    
    if not health_data:
        raise HTTPException(status_code=404, detail="Health data not found")
    
    return health_data

@router.put("/api/v1/healthdata/{health_data_id}", response_model=HealthDataResponse)
async def update_health_data(
    health_data_id: int, 
    health_data_update: HealthDataUpdate, 
    db: Session = Depends(get_db)
):
    """Update health data entry"""
    user_id = get_current_user_id()
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    health_data = db.query(HealthData).filter(
        HealthData.id == health_data_id,
        HealthData.user_id == user_id
    ).first()
    
    if not health_data:
        raise HTTPException(status_code=404, detail="Health data not found")
    
    # Update fields
    update_data = health_data_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(health_data, key, value)
    
    # Recalculate BMI if weight or height changed
    if 'weight' in update_data or 'height' in update_data:
        weight = health_data.weight
        height = health_data.height
        if weight and height:
            health_data.bmi = calculate_bmi(weight, height)
    
    health_data.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(health_data)
    
    return health_data

@router.delete("/api/v1/healthdata/{health_data_id}")
async def delete_health_data(health_data_id: int, db: Session = Depends(get_db)):
    """Delete health data entry"""
    user_id = get_current_user_id()
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    health_data = db.query(HealthData).filter(
        HealthData.id == health_data_id,
        HealthData.user_id == user_id
    ).first()
    
    if not health_data:
        raise HTTPException(status_code=404, detail="Health data not found")
    
    db.delete(health_data)
    db.commit()
    
    return {"message": "Health data deleted successfully"}

@router.get("/api/v1/healthdata/summary", response_model=HealthDataSummary)
async def get_health_data_summary(db: Session = Depends(get_db)):
    """Get health data summary for analytics"""
    user_id = get_current_user_id()
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # Get all health data for user
    health_data = db.query(HealthData).filter(HealthData.user_id == user_id).all()
    
    if not health_data:
        return HealthDataSummary(
            total_entries=0,
            date_range={},
            averages={},
            latest_readings={},
            trends={}
        )
    
    # Calculate summary statistics
    total_entries = len(health_data)
    
    # Date range
    dates = [hd.measurement_time for hd in health_data if hd.measurement_time]
    date_range = {
        "earliest": min(dates).isoformat() if dates else None,
        "latest": max(dates).isoformat() if dates else None
    }
    
    # Calculate averages
    def safe_average(values):
        filtered = [v for v in values if v is not None]
        return round(sum(filtered) / len(filtered), 2) if filtered else None
    
    averages = {
        "systolic_bp": safe_average([hd.systolic_bp for hd in health_data]),
        "diastolic_bp": safe_average([hd.diastolic_bp for hd in health_data]),
        "blood_sugar": safe_average([hd.blood_sugar for hd in health_data]),
        "sleep_hours": safe_average([hd.sleep_hours for hd in health_data]),
        "stress_level": safe_average([hd.stress_level for hd in health_data]),
        "weight": safe_average([hd.weight for hd in health_data]),
        "heart_rate": safe_average([hd.heart_rate for hd in health_data]),
        "mood_score": safe_average([hd.mood_score for hd in health_data]),
        "energy_level": safe_average([hd.energy_level for hd in health_data])
    }
    
    # Latest readings
    latest = max(health_data, key=lambda x: x.measurement_time or datetime.min)
    latest_readings = {
        "systolic_bp": latest.systolic_bp,
        "diastolic_bp": latest.diastolic_bp,
        "blood_sugar": latest.blood_sugar,
        "weight": latest.weight,
        "measurement_time": latest.measurement_time.isoformat() if latest.measurement_time else None
    }
    
    return HealthDataSummary(
        total_entries=total_entries,
        date_range=date_range,
        averages=averages,
        latest_readings=latest_readings,
        trends={}  # Could implement trend analysis here
    )

@router.get("/api/v1/healthdata/charts", response_model=HealthDataChartData)
async def get_chart_data(
    days: int = Query(30, ge=1, le=365),
    db: Session = Depends(get_db)
):
    """Get health data formatted for charts"""
    user_id = get_current_user_id()
    if not user_id:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # Get health data for the specified number of days
    start_date = datetime.utcnow() - timedelta(days=days)
    
    health_data = db.query(HealthData).filter(
        HealthData.user_id == user_id,
        HealthData.measurement_time >= start_date
    ).order_by(HealthData.measurement_time).all()
    
    # Format data for charts
    dates = []
    blood_pressure_systolic = []
    blood_pressure_diastolic = []
    blood_sugar = []
    weight = []
    sleep_hours = []
    stress_level = []
    mood_score = []
    energy_level = []
    
    for hd in health_data:
        date_str = hd.measurement_time.strftime("%Y-%m-%d") if hd.measurement_time else ""
        dates.append(date_str)
        blood_pressure_systolic.append(hd.systolic_bp)
        blood_pressure_diastolic.append(hd.diastolic_bp)
        blood_sugar.append(hd.blood_sugar)
        weight.append(hd.weight)
        sleep_hours.append(hd.sleep_hours)
        stress_level.append(hd.stress_level)
        mood_score.append(hd.mood_score)
        energy_level.append(hd.energy_level)
    
    return HealthDataChartData(
        dates=dates,
        blood_pressure_systolic=blood_pressure_systolic,
        blood_pressure_diastolic=blood_pressure_diastolic,
        blood_sugar=blood_sugar,
        weight=weight,
        sleep_hours=sleep_hours,
        stress_level=stress_level,
        mood_score=mood_score,
        energy_level=energy_level
    )