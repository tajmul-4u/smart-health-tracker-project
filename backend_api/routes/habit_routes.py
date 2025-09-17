from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..models.habit import HabitCreate, HabitResponse, HabitUpdate
from ..utils.security import SecurityUtils
from ...app.database.local_db import get_db
from ...app.models.habit_model import Habit
from ...app.models.user_model import User

router = APIRouter()

@router.post("/", response_model=HabitResponse)
async def create_habit(
    habit: HabitCreate,
    token: dict = Depends(SecurityUtils.auth_wrapper),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == token["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_habit = Habit(**habit.dict(), user_id=user.id)
    db.add(db_habit)
    db.commit()
    db.refresh(db_habit)
    return db_habit

@router.get("/", response_model=List[HabitResponse])
async def get_habits(
    token: dict = Depends(SecurityUtils.auth_wrapper),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == token["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    habits = db.query(Habit).filter(Habit.user_id == user.id).all()
    return habits

@router.get("/{habit_id}", response_model=HabitResponse)
async def get_habit(
    habit_id: int,
    token: dict = Depends(SecurityUtils.auth_wrapper),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == token["sub"]).first()
    habit = db.query(Habit).filter(Habit.id == habit_id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    if habit.user_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this habit")
    return habit

@router.put("/{habit_id}", response_model=HabitResponse)
async def update_habit(
    habit_id: int,
    habit_update: HabitUpdate,
    token: dict = Depends(SecurityUtils.auth_wrapper),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == token["sub"]).first()
    habit = db.query(Habit).filter(Habit.id == habit_id, Habit.user_id == user.id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    for key, value in habit_update.dict(exclude_unset=True).items():
        setattr(habit, key, value)
    
    db.commit()
    db.refresh(habit)
    return habit

@router.delete("/{habit_id}")
async def delete_habit(
    habit_id: int,
    token: dict = Depends(SecurityUtils.auth_wrapper),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == token["sub"]).first()
    habit = db.query(Habit).filter(Habit.id == habit_id, Habit.user_id == user.id).first()
    if not habit:
        raise HTTPException(status_code=404, detail="Habit not found")
    
    db.delete(habit)
    db.commit()
    return {"message": "Habit deleted successfully"}
