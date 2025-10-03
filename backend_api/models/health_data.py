from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime, date
from enum import Enum

class SugarTestType(str, Enum):
    FASTING = "fasting"
    AFTER_MEAL = "after_meal"
    RANDOM = "random"

class HealthDataCreate(BaseModel):
    # Blood Pressure
    systolic_bp: Optional[float] = Field(None, ge=70, le=250, description="Systolic blood pressure (70-250 mmHg)")
    diastolic_bp: Optional[float] = Field(None, ge=40, le=150, description="Diastolic blood pressure (40-150 mmHg)")
    
    # Blood Sugar
    blood_sugar: Optional[float] = Field(None, ge=30, le=600, description="Blood sugar level (30-600 mg/dL)")
    sugar_test_type: Optional[SugarTestType] = Field(None, description="Type of sugar test")
    
    # Sleep
    sleep_hours: Optional[float] = Field(None, ge=0, le=24, description="Hours of sleep (0-24)")
    sleep_quality: Optional[int] = Field(None, ge=1, le=10, description="Sleep quality rating (1-10)")
    
    # Stress
    stress_level: Optional[int] = Field(None, ge=1, le=10, description="Stress level (1-10)")
    stress_notes: Optional[str] = Field(None, max_length=500, description="Notes about stress")
    
    # Physical Activity
    steps_count: Optional[int] = Field(None, ge=0, le=100000, description="Number of steps")
    exercise_minutes: Optional[float] = Field(None, ge=0, le=1440, description="Exercise duration in minutes")
    
    # Physical Measurements
    weight: Optional[float] = Field(None, ge=20, le=500, description="Weight in kg")
    height: Optional[float] = Field(None, ge=50, le=300, description="Height in cm")
    
    # Vital Signs
    heart_rate: Optional[int] = Field(None, ge=30, le=250, description="Heart rate in BPM")
    
    # Lifestyle
    water_intake: Optional[float] = Field(None, ge=0, le=20, description="Water intake in liters")
    mood_score: Optional[int] = Field(None, ge=1, le=10, description="Mood rating (1-10)")
    energy_level: Optional[int] = Field(None, ge=1, le=10, description="Energy level (1-10)")
    
    # Additional info
    notes: Optional[str] = Field(None, max_length=1000, description="Additional notes")
    measurement_time: Optional[datetime] = Field(None, description="When measurement was taken")

    @validator('systolic_bp', 'diastolic_bp')
    def validate_blood_pressure(cls, v, values):
        if v is not None:
            if 'systolic_bp' in values and 'diastolic_bp' in values:
                systolic = values.get('systolic_bp')
                diastolic = v if 'diastolic_bp' not in values else values.get('diastolic_bp')
                if systolic and diastolic and systolic <= diastolic:
                    raise ValueError('Systolic pressure must be greater than diastolic pressure')
        return v

    @validator('blood_sugar')
    def validate_blood_sugar_with_type(cls, v, values):
        if v is not None and 'sugar_test_type' in values:
            test_type = values.get('sugar_test_type')
            if test_type == SugarTestType.FASTING and (v < 70 or v > 126):
                raise ValueError('Fasting blood sugar should typically be 70-126 mg/dL')
            elif test_type == SugarTestType.AFTER_MEAL and (v < 70 or v > 200):
                raise ValueError('Post-meal blood sugar should typically be 70-200 mg/dL')
        return v

class HealthDataResponse(BaseModel):
    id: int
    user_id: int
    systolic_bp: Optional[float]
    diastolic_bp: Optional[float]
    blood_sugar: Optional[float]
    sugar_test_type: Optional[str]
    sleep_hours: Optional[float]
    sleep_quality: Optional[int]
    stress_level: Optional[int]
    stress_notes: Optional[str]
    steps_count: Optional[int]
    exercise_minutes: Optional[float]
    weight: Optional[float]
    height: Optional[float]
    bmi: Optional[float]
    heart_rate: Optional[int]
    water_intake: Optional[float]
    mood_score: Optional[int]
    energy_level: Optional[int]
    notes: Optional[str]
    measurement_time: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class HealthDataUpdate(BaseModel):
    systolic_bp: Optional[float] = Field(None, ge=70, le=250)
    diastolic_bp: Optional[float] = Field(None, ge=40, le=150)
    blood_sugar: Optional[float] = Field(None, ge=30, le=600)
    sugar_test_type: Optional[SugarTestType] = None
    sleep_hours: Optional[float] = Field(None, ge=0, le=24)
    sleep_quality: Optional[int] = Field(None, ge=1, le=10)
    stress_level: Optional[int] = Field(None, ge=1, le=10)
    stress_notes: Optional[str] = Field(None, max_length=500)
    steps_count: Optional[int] = Field(None, ge=0, le=100000)
    exercise_minutes: Optional[float] = Field(None, ge=0, le=1440)
    weight: Optional[float] = Field(None, ge=20, le=500)
    height: Optional[float] = Field(None, ge=50, le=300)
    heart_rate: Optional[int] = Field(None, ge=30, le=250)
    water_intake: Optional[float] = Field(None, ge=0, le=20)
    mood_score: Optional[int] = Field(None, ge=1, le=10)
    energy_level: Optional[int] = Field(None, ge=1, le=10)
    notes: Optional[str] = Field(None, max_length=1000)
    measurement_time: Optional[datetime] = None

class HealthDataSummary(BaseModel):
    """Summary statistics for health data visualization"""
    total_entries: int
    date_range: dict
    averages: dict
    latest_readings: dict
    trends: dict

class HealthDataChartData(BaseModel):
    """Data formatted for chart visualization"""
    dates: list[str]
    blood_pressure_systolic: list[Optional[float]]
    blood_pressure_diastolic: list[Optional[float]]
    blood_sugar: list[Optional[float]]
    weight: list[Optional[float]]
    sleep_hours: list[Optional[float]]
    stress_level: list[Optional[int]]
    mood_score: list[Optional[int]]
    energy_level: list[Optional[int]]