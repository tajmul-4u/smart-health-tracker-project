from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class HabitBase(BaseModel):
    name: str
    description: Optional[str] = None
    frequency: str
    target_value: float
    current_value: float = 0
    unit: str

class HabitCreate(HabitBase):
    pass

class HabitUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    frequency: Optional[str] = None
    target_value: Optional[float] = None
    current_value: Optional[float] = None
    unit: Optional[str] = None
    is_active: Optional[bool] = None

class HabitResponse(HabitBase):
    id: int
    user_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    start_date: datetime
    end_date: Optional[datetime] = None

    class Config:
        orm_mode = True
