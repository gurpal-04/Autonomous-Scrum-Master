from fastapi import HTTPException
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from agents.sprint_planner import root_agent as sprint_planner_agent
from google.genai import types
from dotenv import load_dotenv
from firestore import sprint
from typing import Dict, Any, List

load_dotenv()

# Initialize the session service once
session_service = InMemorySessionService()
USER_ID = "gurpalsingh"
APP_NAME = "sprint planner"


async def plan_sprint_logic(payload: str):
    input_text = payload

    # Create a new session
    new_session = session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        state={"initial_key": "initial_value"}
    )
    SESSION_ID = new_session.id

    # Initialize the runner with the existing session service
    runner = Runner(
        agent=sprint_planner_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    # Prepare the user content
    user_content = types.Content(role="user", parts=[types.Part(text=input_text)])

    final_response_text = None

    try:
        async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=user_content):
            if event.is_final_response() and event.content and event.content.parts:
                final_response_text = event.content.parts[0].text.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during agent run: {e}")

    if final_response_text:
        return {"response": final_response_text}
    else:
        raise HTTPException(status_code=500, detail="No response received from agent.")

async def create_sprint_logic(sprint_data: Dict[str, Any]) -> Dict[str, Any]:
    try:
        sprint_id = sprint.create_sprint(sprint_data)
        return {"id": sprint_id, "message": "Sprint created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_sprint_logic(sprint_id: str) -> Dict[str, Any]:
    try:
        result = sprint.get_sprint(sprint_id)
        if not result:
            raise HTTPException(status_code=404, detail="Sprint not found")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def update_sprint_logic(sprint_id: str, updates: Dict[str, Any]) -> Dict[str, str]:
    try:
        sprint.update_sprint(sprint_id, updates)
        return {"message": "Sprint updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def delete_sprint_logic(sprint_id: str) -> Dict[str, str]:
    try:
        sprint.delete_sprint(sprint_id)
        return {"message": "Sprint deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def list_sprints_logic() -> Dict[str, List[Dict[str, Any]]]:
    try:
        sprints = sprint.list_sprints()
        return {"sprints": sprints}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def add_sprint_comment_logic(sprint_id: str, comment: Dict[str, Any]) -> Dict[str, Any]:
    try:
        comment_id = sprint.add_comment(sprint_id, comment)
        return {"id": comment_id, "message": "Comment added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_sprint_comments_logic(sprint_id: str) -> Dict[str, List[Dict[str, Any]]]:
    try:
        comments = sprint.get_comments(sprint_id)
        return {"comments": comments}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def log_sprint_activity_logic(sprint_id: str, activity: Dict[str, Any]) -> Dict[str, Any]:
    try:
        activity_id = sprint.log_activity(sprint_id, activity)
        return {"id": activity_id, "message": "Activity logged successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_sprint_activity_log_logic(sprint_id: str) -> Dict[str, List[Dict[str, Any]]]:
    try:
        activity_log = sprint.get_activity_log(sprint_id)
        return {"activity_log": activity_log}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
