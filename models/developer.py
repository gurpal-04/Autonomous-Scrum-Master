from typing import Optional, List, Literal
from pydantic import BaseModel, Field

class DeveloperBase(BaseModel):
    name: str
    designation: str
    experience_level: Literal["Junior", "Mid", "Senior", "Lead"]
    skills: List[str]
    status: Literal["available", "overloaded", "on_leave"]
    profile_pic_url: Optional[str] = None
    assigned_tasks: List[str] = Field(default_factory=list)

class DeveloperCreate(DeveloperBase):
    pass

class DeveloperUpdate(BaseModel):
    name: Optional[str] = None
    designation: Optional[str] = None
    experience_level: Optional[Literal["Junior", "Mid", "Senior", "Lead"]] = None
    skills: Optional[List[str]] = None
    status: Optional[Literal["available", "overloaded", "on_leave"]] = None
    profile_pic_url: Optional[str] = None
    assigned_tasks: Optional[List[str]] = None 