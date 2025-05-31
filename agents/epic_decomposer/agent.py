from google.adk.agents import Agent
from pydantic import BaseModel, Field
from typing import List


class UserStory(BaseModel):
    title: str = Field(
        description="A short, descriptive title of the user story"
    )
    description: str = Field(
        description="The full user story in the format: As a [role], I want to [goal], so that [reason]"
    )
    acceptance_criteria: List[str] = Field(
        description="A list of clear, testable acceptance criteria"
    )


class UserStoryList(BaseModel):
    stories: List[UserStory]

root_agent = Agent(
    name="epic_decomposer",
    model="gemini-2.0-flash",
    description="Converts an EPIC into user stories with acceptance criteria",
    instruction="""
        You are a Product Owner working in an Agile team.

        Your task is to break down a high-level EPIC into 3–7 individual USER STORIES.

        Each user story must include:
        - A short TITLE
        - A DESCRIPTION written in this format: "As a [role], I want to [goal], so that [reason]"
        - A list of 3–5 ACCEPTANCE CRITERIA

        GUIDELINES:
        - Only include what is needed to cover the EPIC’s scope
        - Each story should be deliverable within a single sprint
        - Acceptance criteria must be testable and specific (no vague or broad conditions)
        - Do not duplicate features across stories

        IMPORTANT: Your response must be valid JSON, following this format:

        [
        {
            "title": "Short title here",
            "description": "As a [role], I want to [goal], so that [reason]",
            "acceptance_criteria": [
            "Condition 1",
            "Condition 2",
            ...
            ]
        },
        ...
        ]

        Do not include any explanation or additional text outside this JSON structure.
    """,
    output_schema=UserStoryList,
    output_key="stories"
)
