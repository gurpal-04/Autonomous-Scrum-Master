from pydantic import BaseModel, Field
from typing import List

class EpicInput(BaseModel):
    epic_title: str = Field(..., description="Title of the epic")
    epic_description: str = Field(..., description="Detailed description of the epic")


class UserStory(BaseModel):
    title: str = Field(..., description="Title of the user story")
    description: str = Field(..., description="Detailed user story content")
    acceptance_criteria: List[str] = Field(
        ..., description="List of acceptance criteria for the story"
    )


class EpicOutput(BaseModel):
    stories: List[UserStory] = Field(
        ..., description="List of decomposed user stories with acceptance criteria"
    )
