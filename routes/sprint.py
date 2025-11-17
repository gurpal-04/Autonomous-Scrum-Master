from fastapi import APIRouter, HTTPException
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
    get_sprint_activity_log_logic,
    get_sprint_tasks_logic
)
from models.sprint import SprintCreate, SprintUpdate, SprintComment, SprintActivity, SprintPlan
from firestore import sprint as sprint_module

router = APIRouter(prefix="/sprint", tags=["Sprint Planner"])

@router.post("/plan")
async def plan_sprint(payload: SprintPlan):
    result = await plan_sprint_logic(payload.model_dump())
    return result

@router.get("/{sprint_id}/tasks")
async def get_sprint_tasks(sprint_id: str):
    """Get all tasks planned for a sprint."""
    return await get_sprint_tasks_logic(sprint_id)

@router.post("/{sprint_id}/tasks")
async def add_tasks_to_sprint(sprint_id: str, task_ids: list):
    """Add task IDs to a sprint."""
    try:
        sprint_module.add_tasks_to_sprint(sprint_id, task_ids)
        return {"message": f"Added {len(task_ids)} tasks to sprint"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{sprint_id}/tasks")
async def remove_tasks_from_sprint(sprint_id: str, task_ids: list):
    """Remove task IDs from a sprint."""
    try:
        sprint_module.remove_tasks_from_sprint(sprint_id, task_ids)
        return {"message": f"Removed {len(task_ids)} tasks from sprint"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{sprint_id}/assignments")
async def update_task_assignments(sprint_id: str, assignments: dict):
    """Update task assignments for a sprint."""
    try:
        sprint_module.update_task_assignments(sprint_id, assignments)
        return {"message": f"Updated {len(assignments)} task assignments"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
async def create_sprint(sprint_data: SprintCreate):
    return await create_sprint_logic(sprint_data.model_dump())

@router.get("/{sprint_id}")
async def get_sprint(sprint_id: str):
    return await get_sprint_logic(sprint_id)

@router.put("/{sprint_id}")
async def update_sprint(sprint_id: str, updates: SprintUpdate):
    return await update_sprint_logic(sprint_id, updates.model_dump(exclude_unset=True))

@router.delete("/{sprint_id}")
async def delete_sprint(sprint_id: str):
    return await delete_sprint_logic(sprint_id)

@router.get("/")
async def list_sprints():
    return await list_sprints_logic()

@router.post("/{sprint_id}/comments")
async def add_sprint_comment(sprint_id: str, comment: SprintComment):
    return await add_sprint_comment_logic(sprint_id, comment.model_dump())

@router.get("/{sprint_id}/comments")
async def get_sprint_comments(sprint_id: str):
    return await get_sprint_comments_logic(sprint_id)

@router.post("/{sprint_id}/activity")
async def log_sprint_activity(sprint_id: str, activity: SprintActivity):
    return await log_sprint_activity_logic(sprint_id, activity.model_dump())

@router.get("/{sprint_id}/activity")
async def get_sprint_activity_log(sprint_id: str):
    return await get_sprint_activity_log_logic(sprint_id)
