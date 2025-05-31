from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field
from typing import List, Optional


class Developer(BaseModel):
    name: str
    role: str
    available_hours_per_day: int


class AssignedTask(BaseModel):
    title: str
    description: str
    role: str
    estimate_hours: int
    sprint_points: int
    assigned_to: Optional[str]
    status: str  # "scheduled" or "unassigned"
    planned_start_day: Optional[int]
    planned_end_day: Optional[int]


class PlanningInput(BaseModel):
    tasks: List[AssignedTask]
    developers: List[Developer]
    timeline_days: Optional[int] = Field(description="Optional number of days for the sprint")


class PlanningOutput(BaseModel):
    planned_tasks: List[AssignedTask]


root_agent = LlmAgent(
    name="sprint_planner",
    model="gemini-2.0-flash",
    description="Assigns tasks to developers based on role match and availability",
    instruction="""
        You are a Sprint Planning Assistant helping a software team.

        Your task is to assign decomposed technical tasks to available developers.

        Each developer has:
        - A specific role (frontend, backend, fullstack, etc.)
        - Limited availability per day (in hours)

        Each task requires:
        - A role match
        - An estimated number of hours

        If a timeline (number of days) is provided, plan accordingly so all tasks finish within the sprint.
        Otherwise, just assign based on availability.

        Rules:
        - Assign only to matching role
        - Assign only if developer has enough capacity
        - Distribute tasks fairly
        - Set planned start and end day for each task (Day 1, Day 2, ...)

        If no suitable developer is available, mark the task as `"unassigned"`.

        Your output MUST be a list of tasks with these fields:
        - title
        - description
        - role
        - estimate_hours
        - sprint_points
        - assigned_to (developer name)
        - status ("scheduled" or "unassigned")
        - planned_start_day (integer, optional)
        - planned_end_day (integer, optional)

        DO NOT include any explanation or extra text outside the JSON.
    """,
    output_schema=PlanningOutput,
    output_key="planned_tasks"
)
