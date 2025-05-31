from dotenv import load_dotenv
from firestore.firestore_client import db
from datetime import datetime, timezone
from typing import List

load_dotenv()

TASK_COLLECTION = "tasks"

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
