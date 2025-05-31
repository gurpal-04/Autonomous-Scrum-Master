from fastapi import  HTTPException
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from agents.task_decomposer import root_agent as task_decomposer_agent
from google.genai import types
from dotenv import load_dotenv
from firestore import story
from typing import Dict, Any, List

load_dotenv()

# Initialize the session service once
session_service = InMemorySessionService()
USER_ID = "gurpalsingh"
APP_NAME = "user story decomposer"

async def decompose_user_story_logic(payload: str):
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
        agent=task_decomposer_agent,
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

async def create_story_logic(story_data: Dict[str, Any]) -> Dict[str, Any]:
    try:
        story_id = story.create_story(story_data)
        return {"id": story_id, "message": "Story created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_story_logic(story_id: str) -> Dict[str, Any]:
    try:
        result = story.get_story(story_id)
        if not result:
            raise HTTPException(status_code=404, detail="Story not found")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def update_story_logic(story_id: str, updates: Dict[str, Any]) -> Dict[str, str]:
    try:
        story.update_story(story_id, updates)
        return {"message": "Story updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def delete_story_logic(story_id: str) -> Dict[str, str]:
    try:
        story.delete_story(story_id)
        return {"message": "Story deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def list_stories_logic() -> Dict[str, List[Dict[str, Any]]]:
    try:
        stories = story.list_stories()
        return {"stories": stories}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def add_comment_logic(story_id: str, comment: Dict[str, Any]) -> Dict[str, Any]:
    try:
        comment_id = story.add_comment(story_id, comment)
        return {"id": comment_id, "message": "Comment added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_comments_logic(story_id: str) -> Dict[str, List[Dict[str, Any]]]:
    try:
        comments = story.get_comments(story_id)
        return {"comments": comments}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def log_activity_logic(story_id: str, activity: Dict[str, Any]) -> Dict[str, Any]:
    try:
        activity_id = story.log_activity(story_id, activity)
        return {"id": activity_id, "message": "Activity logged successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_activity_log_logic(story_id: str) -> Dict[str, List[Dict[str, Any]]]:
    try:
        activity_log = story.get_activity_log(story_id)
        return {"activity_log": activity_log}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
