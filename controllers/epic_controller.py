from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from agents.epic_decomposer import root_agent as epic_agent
from google.genai import types
from firestore import epic, story
from fastapi import HTTPException
from typing import Dict, Any, List

session_service = InMemorySessionService()
USER_ID = "gurpalsingh"
APP_NAME = "epic decomposer"

async def decompose_epic_logic(payload: str):
    input_text = payload

    new_session = session_service.create_session(
        app_name=APP_NAME,
        user_id=USER_ID,
        state={"initial_key": "initial_value"}
    )
    SESSION_ID = new_session.id

    runner = Runner(
        agent=epic_agent,
        app_name=APP_NAME,
        session_service=session_service,
    )

    user_content = types.Content(role="user", parts=[types.Part(text=input_text)])

    final_response_text = None

    try:
        async for event in runner.run_async(user_id=USER_ID, session_id=SESSION_ID, new_message=user_content):
            if event.is_final_response() and event.content and event.content.parts:
                final_response_text = event.content.parts[0].text.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during agent run: {e}")

    if final_response_text:
        # Optional: Save to Firestore
        # story_data = json.loads(final_response_text).get("stories")
        # for i in story_data:
        #     story.create_story(i)
        return final_response_text
    else:
        raise HTTPException(status_code=500, detail="No response received from agent.")

async def create_epic_logic(epic_data: Dict[str, Any]) -> Dict[str, Any]:
    try:
        epic_id = epic.create_epic(epic_data)
        return {"id": epic_id, "message": "Epic created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def get_epic_logic(epic_id: str) -> Dict[str, Any]:
    try:
        result = epic.get_epic(epic_id)
        if not result:
            raise HTTPException(status_code=404, detail="Epic not found")
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def update_epic_logic(epic_id: str, updates: Dict[str, Any]) -> Dict[str, str]:
    try:
        epic.update_epic(epic_id, updates)
        return {"message": "Epic updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

async def list_epics_logic() -> Dict[str, List[Dict[str, Any]]]:
    try:
        epics = epic.list_epics()
        return {"epics": epics}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
