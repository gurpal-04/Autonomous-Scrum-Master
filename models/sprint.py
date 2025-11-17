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

class SprintTask(BaseModel):
    title: str
    description: str
    role: str
    estimate_hours: int
    sprint_points: int

class SprintDeveloper(BaseModel):
    name: str
    role: str
    available_hours_per_day: int

class SprintPlan(BaseModel):
    tasks: Optional[List[SprintTask]] = None
    developers: Optional[List[SprintDeveloper]] = None
    timeline_days: Optional[int] = None
    sprint_name: Optional[str] = None
    sprint_goal: Optional[str] = None
    # Keep backward compatibility
    available_stories: Optional[List[str]] = None
    team_capacity: Optional[int] = None
    constraints: Optional[List[str]] = None 