from firestore.firestore_client import db
from datetime import datetime, timezone
from typing import List, Dict, Any

from dotenv import load_dotenv
import os

load_dotenv()
print("GOOGLE_APPLICATION_CREDENTIALS: sprint", os.getenv("GOOGLE_APPLICATION_CREDENTIALS"))

SPRINT_COLLECTION = "sprints"

# ---------- SPRINT CRUD ----------

def create_sprint(data: dict) -> str:
    data["created_at"] = datetime.now(timezone.utc)
    doc_ref = db.collection(SPRINT_COLLECTION).add(data)
    return doc_ref[1].id

def get_sprint(sprint_id: str):
    doc = db.collection(SPRINT_COLLECTION).document(sprint_id).get()
    return doc.to_dict() | {"id": doc.id} if doc.exists else None

def update_sprint(sprint_id: str, updates: dict):
    updates["updated_at"] = datetime.now(timezone.utc)
    db.collection(SPRINT_COLLECTION).document(sprint_id).update(updates)

def delete_sprint(sprint_id: str):
    db.collection(SPRINT_COLLECTION).document(sprint_id).delete()

def list_sprints() -> List[dict]:
    return [doc.to_dict() | {"id": doc.id} for doc in db.collection(SPRINT_COLLECTION).stream()]

# ---------- SPRINT PLANNING ----------

def add_tasks_to_sprint(sprint_id: str, task_ids: List[str]) -> None:
    """
    Add task IDs to a sprint's planned tasks list.
    
    Args:
        sprint_id: The ID of the sprint
        task_ids: List of task IDs to add to the sprint
    """
    sprint_ref = db.collection(SPRINT_COLLECTION).document(sprint_id)
    sprint_doc = sprint_ref.get()
    
    if not sprint_doc.exists:
        raise ValueError(f"Sprint with ID {sprint_id} not found")
    
    # Get current planned tasks
    current_data = sprint_doc.to_dict()
    current_planned_tasks = current_data.get("planned_task_ids", [])
    
    # Add new task IDs (avoid duplicates)
    updated_planned_tasks = list(set(current_planned_tasks + task_ids))
    
    # Update the sprint document
    sprint_ref.update({
        "planned_task_ids": updated_planned_tasks,
        "updated_at": datetime.now(timezone.utc)
    })

def remove_tasks_from_sprint(sprint_id: str, task_ids: List[str]) -> None:
    """
    Remove task IDs from a sprint's planned tasks list.
    
    Args:
        sprint_id: The ID of the sprint
        task_ids: List of task IDs to remove from the sprint
    """
    sprint_ref = db.collection(SPRINT_COLLECTION).document(sprint_id)
    sprint_doc = sprint_ref.get()
    
    if not sprint_doc.exists:
        raise ValueError(f"Sprint with ID {sprint_id} not found")
    
    # Get current planned tasks
    current_data = sprint_doc.to_dict()
    current_planned_tasks = current_data.get("planned_task_ids", [])
    
    # Remove task IDs
    updated_planned_tasks = [task_id for task_id in current_planned_tasks if task_id not in task_ids]
    
    # Update the sprint document
    sprint_ref.update({
        "planned_task_ids": updated_planned_tasks,
        "updated_at": datetime.now(timezone.utc)
    })

def get_sprint_tasks(sprint_id: str) -> List[dict]:
    """
    Get all tasks planned for a sprint.
    
    Args:
        sprint_id: The ID of the sprint
    
    Returns:
        List of task documents
    """
    sprint_doc = db.collection(SPRINT_COLLECTION).document(sprint_id).get()
    if not sprint_doc.exists:
        return []
    
    sprint_data = sprint_doc.to_dict()
    planned_task_ids = sprint_data.get("planned_task_ids", [])
    
    if not planned_task_ids:
        return []
    
    # Fetch task documents
    tasks = []
    for task_id in planned_task_ids:
        task_doc = db.collection("tasks").document(task_id).get()
        if task_doc.exists:
            task_data = task_doc.to_dict()
            task_data["id"] = task_id
            tasks.append(task_data)
    
    return tasks

def update_task_assignments(sprint_id: str, task_assignments: Dict[str, str]) -> None:
    """
    Update task assignments for tasks in a sprint.
    
    Args:
        sprint_id: The ID of the sprint
        task_assignments: Dictionary mapping task_id to assigned developer name
    """
    batch = db.batch()
    
    for task_id, assigned_to in task_assignments.items():
        task_ref = db.collection("tasks").document(task_id)
        batch.update(task_ref, {
            "assigned_to": assigned_to,
            "sprint_id": sprint_id,
            "updated_at": datetime.now(timezone.utc)
        })
    
    batch.commit()

# ---------- COMMENTS ----------

def add_comment(sprint_id: str, comment: dict) -> str:
    comment["created_at"] = datetime.now(timezone.utc)
    doc_ref = db.collection(SPRINT_COLLECTION).document(sprint_id).collection("comments").add(comment)
    return doc_ref[1].id

def get_comments(sprint_id: str) -> List[dict]:
    comments_ref = db.collection(SPRINT_COLLECTION).document(sprint_id).collection("comments")
    return [doc.to_dict() | {"id": doc.id} for doc in comments_ref.stream()]

# ---------- ACTIVITY LOG ----------

def log_activity(sprint_id: str, activity: dict) -> str:
    activity["timestamp"] = datetime.now(timezone.utc)
    doc_ref = db.collection(SPRINT_COLLECTION).document(sprint_id).collection("activity").add(activity)
    return doc_ref[1].id

def get_activity_log(sprint_id: str) -> List[dict]:
    activity_ref = db.collection(SPRINT_COLLECTION).document(sprint_id).collection("activity")
    return [doc.to_dict() | {"id": doc.id} for doc in activity_ref.order_by("timestamp").stream()]
