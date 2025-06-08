from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class SprintBase(BaseModel):
    name: str
    goal: str
    start_date: datetime
    end_date: datetime
    status: str
    capacity: Optional[int] = None
    velocity: Optional[float] = None
    team_id: Optional[str] = None

class SprintCreate(SprintBase):
    pass

class SprintUpdate(BaseModel):
    name: Optional[str] = None
    goal: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    status: Optional[str] = None
    capacity: Optional[int] = None
    velocity: Optional[float] = None
    team_id: Optional[str] = None

class SprintComment(BaseModel):
    content: str
    author: str
    created_at: Optional[datetime] = None

class SprintActivity(BaseModel):
    action: str
    description: str
    user: str
    timestamp: Optional[datetime] = None

class SprintPlan(BaseModel):
    sprint_goal: str
    available_stories: List[str]
    team_capacity: int
    constraints: Optional[List[str]] = None 