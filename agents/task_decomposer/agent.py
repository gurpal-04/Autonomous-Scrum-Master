from google.adk.agents import LlmAgent
from pydantic import BaseModel, Field, Extra
from typing import List, Dict


# --- Define the schema for a single decomposed task ---
class DecomposedTask(BaseModel):
    title: str = Field(description="Short title of the task")
    description: str = Field(description="Detailed explanation of the task")
    role: str = Field(description="Primary developer role required: frontend, backend, fullstack, QA, llm, etc.")
    estimate_hours: int = Field(description="Estimated time to complete the task in hours")
    story_points: int = Field(description="Sprint points estimate for the task based on complexity and effort")
    # devs_required: Dict[str, int] = Field(
    #     description="Dictionary mapping each required role to number of developers needed to complete the task in the given timeline. E.g., { 'frontend': 2 }"
    # )



# --- Wrapper for list of tasks ---
class DecomposedTaskList(BaseModel):
    tasks: List[DecomposedTask]


# --- LlmAgent definition ---
root_agent = LlmAgent(
    name="task_decomposer",
    model="gemini-2.0-flash",
    description="Breaks down a user story into technical tasks and estimates developers required to meet the timeline",
    instruction="""
        You are a senior agile team member assisting with sprint planning.

        Your task is to:
        - Take a user story and a total timeline in days
        - Break the story into 3–7 clearly defined tasks
        - For each task, estimate time in hours
        - Calculate how many developers are needed for that task to finish within the provided timeline

        DEVELOPER CALCULATION RULES:
        - 1 developer typically works ~6 productive hours per day
        - Total working hours available = days * 6
        - Distribute developers per role based on estimated time and the deadline
        - Estimate story points using Fibonacci scale (1, 2, 3, 5, 8, 13, 21):
            * Consider effort, complexity, and uncertainty when assigning story points
        - The `devs_required` field should map roles to number of devs needed for the task

        OUTPUT FORMAT: Valid JSON list following this structure:
        [
           {
            "title": "Title here",
            "description": "Description of the task",
            "role": "Role here",
            "estimate_hours": "Estimated time in hours",
            "story_points": "Story points estimate using Fibonacci scale (1, 2, 3, 5, 8, 13, 21)",
            "devs_required": { "frontend": 1 }
            },
          ...
        ]

        ONLY return the JSON list. DO NOT include any other text or explanation.
    """,
    output_schema=DecomposedTaskList,
    output_key="decomposed_tasks",
)
