from dotenv import load_dotenv
from firestore.firestore_client import db
from datetime import datetime, timezone
from typing import List
from google.cloud import firestore

load_dotenv()

TASK_COLLECTION = "tasks"
DEVELOPER_COLLECTION = "developers"

# ---------- TASK CRUD ----------

def create_task(data: dict) -> str:
    data["created_at"] = datetime.now(timezone.utc)
    doc_ref = db.collection(TASK_COLLECTION).add(data)
    return doc_ref[1].id

def get_task(task_id: str):
    doc = db.collection(TASK_COLLECTION).document(task_id).get()
    return doc.to_dict() | {"id": doc.id} if doc.exists else None

def update_task(task_id: str, updates: dict):
    updates["updated_at"] = datetime.now(timezone.utc)
    db.collection(TASK_COLLECTION).document(task_id).update(updates)

def delete_task(task_id: str):
    db.collection(TASK_COLLECTION).document(task_id).delete()

def list_tasks() -> List[dict]:
    return [doc.to_dict() | {"id": doc.id} for doc in db.collection(TASK_COLLECTION).stream()]

# ---------- COMMENTS ----------

def add_comment(task_id: str, comment: dict) -> str:
    comment["created_at"] = datetime.now(timezone.utc)
    doc_ref = db.collection(TASK_COLLECTION).document(task_id).collection("comments").add(comment)
    return doc_ref[1].id

def get_comments(task_id: str) -> List[dict]:
    comments_ref = db.collection(TASK_COLLECTION).document(task_id).collection("comments")
    return [doc.to_dict() | {"id": doc.id} for doc in comments_ref.stream()]

# ---------- ACTIVITY LOG ----------

def log_activity(task_id: str, activity: dict) -> str:
    activity["timestamp"] = datetime.now(timezone.utc)
    doc_ref = db.collection(TASK_COLLECTION).document(task_id).collection("activity").add(activity)
    return doc_ref[1].id

def get_activity_log(task_id: str) -> List[dict]:
    activity_ref = db.collection(TASK_COLLECTION).document(task_id).collection("activity")
    return [doc.to_dict() | {"id": doc.id} for doc in activity_ref.order_by("timestamp").stream()]

async def assign_developers_to_task(task_id: str, developer_ids: List[str]) -> None:
    """
    Assign developers to a task and update their assigned_tasks lists.
    """
    # Get task reference
    task_ref = db.collection(TASK_COLLECTION).document(task_id)
    task_doc = task_ref.get()
    if not task_doc.exists:
        raise ValueError(f"Task with ID {task_id} not found")

    # Start a batch
    batch = db.batch()

    # Update task's assignees
    task_data = task_doc.to_dict()
    current_assignees = set(task_data.get('assignees', []))
    new_assignees = current_assignees.union(set(developer_ids))
    batch.update(task_ref, {'assignees': list(new_assignees)})

    # Update each developer's assigned_tasks
    for dev_id in developer_ids:
        dev_ref = db.collection(DEVELOPER_COLLECTION).document(dev_id)
        dev_doc = dev_ref.get()
        if not dev_doc.exists:
            raise ValueError(f"Developer with ID {dev_id} not found")
        
        dev_data = dev_doc.to_dict()
        current_tasks = set(dev_data.get('assigned_tasks', []))
        current_tasks.add(task_id)
        batch.update(dev_ref, {'assigned_tasks': list(current_tasks)})

    # Commit the batch
    batch.commit()

async def unassign_developers_from_task(task_id: str, developer_ids: List[str]) -> None:
    """
    Remove developers from a task and update their assigned_tasks lists.
    """
    # Get task reference
    task_ref = db.collection(TASK_COLLECTION).document(task_id)
    task_doc = task_ref.get()
    if not task_doc.exists:
        raise ValueError(f"Task with ID {task_id} not found")

    # Start a batch
    batch = db.batch()

    # Update task's assignees
    task_data = task_doc.to_dict()
    current_assignees = set(task_data.get('assignees', []))
    updated_assignees = current_assignees - set(developer_ids)
    batch.update(task_ref, {'assignees': list(updated_assignees)})

    # Update each developer's assigned_tasks
    for dev_id in developer_ids:
        dev_ref = db.collection(DEVELOPER_COLLECTION).document(dev_id)
        dev_doc = dev_ref.get()
        if not dev_doc.exists:
            raise ValueError(f"Developer with ID {dev_id} not found")
        
        dev_data = dev_doc.to_dict()
        current_tasks = set(dev_data.get('assigned_tasks', []))
        current_tasks.discard(task_id)
        batch.update(dev_ref, {'assigned_tasks': list(current_tasks)})
