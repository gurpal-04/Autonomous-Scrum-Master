from typing import Optional, List, Literal
from pydantic import BaseModel, Field
from datetime import datetime

class TaskBase(BaseModel):
    title: str
    description: str
    assignees: List[str] = Field(default_factory=list)
    status: str
    priority: Optional[Literal["normal", "high", "urgent"]] = "normal"
    story_id: Optional[str] = None
    epic_id: Optional[str] = None
    sprint_id: Optional[str] = None
    due_date: Optional[str] = None
    sprint_points: Optional[int] = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    assignees: Optional[List[str]] = None
    status: Optional[str] = None
    priority: Optional[Literal["normal", "high", "urgent"]] = None
    story_id: Optional[str] = None
    epic_id: Optional[str] = None
    sprint_id: Optional[str] = None
    due_date: Optional[str] = None
    sprint_points: Optional[int] = None

class CommentBase(BaseModel):
    content: str
    author: str

class ActivityBase(BaseModel):
    action: str
    description: str
    user: str 