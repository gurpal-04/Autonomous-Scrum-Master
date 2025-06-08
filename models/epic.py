from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class EpicBase(BaseModel):
    title: str
    description: str
    status: str
    priority: Optional[str] = None
    owner: Optional[str] = None
    due_date: Optional[datetime] = None
    estimated_completion_date: Optional[datetime] = None
    story_points: Optional[int] = None

class EpicCreate(EpicBase):
    pass

class EpicUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    owner: Optional[str] = None
    due_date: Optional[datetime] = None
    estimated_completion_date: Optional[datetime] = None
    story_points: Optional[int] = None

class EpicDecompose(BaseModel):
    description: str
    title: str
    constraints: Optional[List[str]] = None
    acceptance_criteria: Optional[List[str]] = None
