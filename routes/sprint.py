from fastapi import APIRouter
from controllers.sprint_controller import (
    plan_sprint_logic,
    create_sprint_logic,
    get_sprint_logic,
    update_sprint_logic,
    delete_sprint_logic,
    list_sprints_logic,
    add_sprint_comment_logic,
    get_sprint_comments_logic,
    log_sprint_activity_logic,
    get_sprint_activity_log_logic
)
from typing import Dict, Any

router = APIRouter(prefix="/sprint", tags=["Sprint Planner"])

@router.post("/plan")
async def plan_sprint(payload: str):
    result = await plan_sprint_logic(payload)
    return {"response": result}

@router.post("/")
async def create_sprint(sprint_data: Dict[str, Any]):
    return await create_sprint_logic(sprint_data)

@router.get("/{sprint_id}")
async def get_sprint(sprint_id: str):
    return await get_sprint_logic(sprint_id)

@router.put("/{sprint_id}")
async def update_sprint(sprint_id: str, updates: Dict[str, Any]):
    return await update_sprint_logic(sprint_id, updates)

@router.delete("/{sprint_id}")
async def delete_sprint(sprint_id: str):
    return await delete_sprint_logic(sprint_id)

@router.get("/")
async def list_sprints():
    return await list_sprints_logic()

@router.post("/{sprint_id}/comments")
async def add_sprint_comment(sprint_id: str, comment: Dict[str, Any]):
    return await add_sprint_comment_logic(sprint_id, comment)

@router.get("/{sprint_id}/comments")
async def get_sprint_comments(sprint_id: str):
    return await get_sprint_comments_logic(sprint_id)

@router.post("/{sprint_id}/activity")
async def log_sprint_activity(sprint_id: str, activity: Dict[str, Any]):
    return await log_sprint_activity_logic(sprint_id, activity)

@router.get("/{sprint_id}/activity")
async def get_sprint_activity_log(sprint_id: str):
    return await get_sprint_activity_log_logic(sprint_id)
