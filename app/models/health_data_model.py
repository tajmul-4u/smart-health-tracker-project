from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database.local_db import Base

class HealthData(Base):
    __tablename__ = "health_data"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Blood Pressure readings
    systolic_bp = Column(Float, nullable=True)  # Top number (120 in 120/80)
    diastolic_bp = Column(Float, nullable=True)  # Bottom number (80 in 120/80)
    
    # Blood Sugar Level
    blood_sugar = Column(Float, nullable=True)  # mg/dL
    sugar_test_type = Column(String(50), nullable=True)  # fasting, after_meal, random
    
    # Sleep Data
    sleep_hours = Column(Float, nullable=True)  # Hours of sleep
    sleep_quality = Column(Integer, nullable=True)  # 1-10 scale
    
    # Stress Level
    stress_level = Column(Integer, nullable=True)  # 1-10 scale
    stress_notes = Column(String(500), nullable=True)
    
    # Physical Activity
    steps_count = Column(Integer, nullable=True)
    exercise_minutes = Column(Float, nullable=True)
    
    # Weight and BMI
    weight = Column(Float, nullable=True)  # kg
    height = Column(Float, nullable=True)  # cm
    bmi = Column(Float, nullable=True)  # calculated
    
    # Heart Rate
    heart_rate = Column(Integer, nullable=True)  # bpm
    
    # Additional metrics
    water_intake = Column(Float, nullable=True)  # liters
    mood_score = Column(Integer, nullable=True)  # 1-10 scale
    energy_level = Column(Integer, nullable=True)  # 1-10 scale
    
    # Notes and metadata
    notes = Column(String(1000), nullable=True)
    measurement_time = Column(DateTime, nullable=True)  # When measurement was taken
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="health_data")