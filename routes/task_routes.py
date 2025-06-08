from fastapi import APIRouter, HTTPException
from typing import List, Optional, Dict
from models.task import TaskBase, TaskCreate, TaskUpdate, CommentBase, ActivityBase
from firestore.task import (
    create_task,
    get_task,
    update_task,
    delete_task,
    list_tasks,
    add_comment,
    get_comments,
    log_activity,
    get_activity_log,
    assign_developers_to_task,
    unassign_developers_from_task
)
from pydantic import BaseModel

router = APIRouter(prefix="/tasks", tags=["Tasks"])

# New models for developer assignment
class DeveloperAssignment(BaseModel):
    developer_ids: List[str]

# Task CRUD routes
@router.post("/", response_model=dict)
async def create_new_task(task: TaskCreate):
    try:
        task_id = create_task(task.model_dump())
        return {"id": task_id, "message": "Task created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{task_id}", response_model=dict)
async def get_task_by_id(task_id: str):
    task = get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}")
async def update_task_by_id(task_id: str, task_update: TaskUpdate):
    try:
        update_task(task_id, task_update.model_dump(exclude_unset=True))
        return {"message": "Task updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{task_id}")
async def delete_task_by_id(task_id: str):
    try:
        delete_task(task_id)
        return {"message": "Task deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[dict])
async def get_all_tasks():
    try:
        return list_tasks()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Comment routes
@router.post("/{task_id}/comments", response_model=dict)
async def create_comment(task_id: str, comment: CommentBase):
    try:
        comment_id = add_comment(task_id, comment.model_dump())
        return {"id": comment_id, "message": "Comment added successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{task_id}/comments", response_model=List[dict])
async def get_task_comments(task_id: str):
    try:
        return get_comments(task_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Activity log routes
@router.post("/{task_id}/activity", response_model=dict)
async def create_activity_log(task_id: str, activity: ActivityBase):
    try:
        activity_id = log_activity(task_id, activity.model_dump())
        return {"id": activity_id, "message": "Activity logged successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{task_id}/activity", response_model=List[dict])
async def get_task_activity_log(task_id: str):
    try:
        return get_activity_log(task_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Developer assignment routes
@router.post("/{task_id}/assign", response_model=Dict[str, str])
async def assign_developers(task_id: str, assignment: DeveloperAssignment):
    """Assign developers to a task."""
    try:
        await assign_developers_to_task(task_id, assignment.developer_ids)
        return {"message": "Developers assigned successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{task_id}/unassign", response_model=Dict[str, str])
async def unassign_developers(task_id: str, assignment: DeveloperAssignment):
    """Unassign developers from a task."""
    try:
        await unassign_developers_from_task(task_id, assignment.developer_ids)
        return {"message": "Developers unassigned successfully"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 