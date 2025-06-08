from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

class UserStoryBase(BaseModel):
    title: str
    description: str
    acceptance_criteria: List[str]
    status: str
    priority: Optional[str] = None
    epic_id: Optional[str] = None
    sprint_id: Optional[str] = None
    assignee: Optional[str] = None
    story_points: Optional[int] = None
    due_date: Optional[datetime] = None

class UserStoryCreate(UserStoryBase):
    pass

class UserStoryUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    acceptance_criteria: Optional[List[str]] = None
    status: Optional[str] = None
    priority: Optional[str] = None
    epic_id: Optional[str] = None
    sprint_id: Optional[str] = None
    assignee: Optional[str] = None
    story_points: Optional[int] = None
    due_date: Optional[datetime] = None

class StoryComment(BaseModel):
    content: str
    author: str
    created_at: Optional[datetime] = None

class StoryActivity(BaseModel):
    action: str
    description: str
    user: str
    timestamp: Optional[datetime] = None

class StoryDecompose(BaseModel):
    story_description: str
    acceptance_criteria: Optional[List[str]] = None
    constraints: Optional[List[str]] = None 